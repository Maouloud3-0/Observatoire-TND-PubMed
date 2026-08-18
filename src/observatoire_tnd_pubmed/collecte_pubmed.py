"""Collecte PubMed via les E-utilities officielles et analyse du XML retourné."""

from __future__ import annotations

import json
import time
import xml.etree.ElementTree as ET
from collections.abc import Iterable, Iterator
from pathlib import Path
from typing import Any

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .configuration import ConfigurationNCBI

BASE_EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"


def _texte(element: ET.Element | None) -> str:
    if element is None:
        return ""
    return " ".join("".join(element.itertext()).split())


def _premier_texte(element: ET.Element, chemins: Iterable[str]) -> str:
    for chemin in chemins:
        valeur = _texte(element.find(chemin))
        if valeur:
            return valeur
    return ""


def _date_publication(citation: ET.Element) -> tuple[str, int | None]:
    date = citation.find("Article/ArticleDate")
    if date is not None:
        annee = _texte(date.find("Year"))
        mois = _texte(date.find("Month")) or "01"
        jour = _texte(date.find("Day")) or "01"
        return f"{annee}-{mois.zfill(2)}-{jour.zfill(2)}", int(annee)

    date = citation.find("Article/Journal/JournalIssue/PubDate")
    annee = _texte(date.find("Year")) if date is not None else ""
    if not annee and date is not None:
        date_medline = _texte(date.find("MedlineDate"))
        annee = date_medline[:4] if date_medline[:4].isdigit() else ""
    return (f"{annee}-01-01", int(annee)) if annee else ("", None)


def analyser_xml_pubmed(contenu_xml: str | bytes) -> list[dict[str, Any]]:
    """Transforme un lot PubMed XML en objets sérialisables sans télécharger le texte intégral."""

    racine = ET.fromstring(contenu_xml)
    articles: list[dict[str, Any]] = []
    for entree in racine.findall(".//PubmedArticle"):
        citation = entree.find("MedlineCitation")
        if citation is None:
            continue

        pmid = _texte(citation.find("PMID"))
        article = citation.find("Article")
        if not pmid or article is None:
            continue

        date, annee = _date_publication(citation)
        resume = " ".join(
            filtre
            for filtre in (_texte(x) for x in article.findall("Abstract/AbstractText"))
            if filtre
        )
        auteurs: list[dict[str, Any]] = []
        for position, auteur in enumerate(article.findall("AuthorList/Author"), start=1):
            nom_collectif = _texte(auteur.find("CollectiveName"))
            nom = _texte(auteur.find("LastName")) or nom_collectif
            prenom = _texte(auteur.find("ForeName"))
            initiales = _texte(auteur.find("Initials"))
            orcid = ""
            for identifiant in auteur.findall("Identifier"):
                if identifiant.attrib.get("Source", "").upper() == "ORCID":
                    orcid = _texte(identifiant)
            auteurs.append(
                {
                    "nom": nom,
                    "prenom": prenom,
                    "initiales": initiales,
                    "orcid": orcid,
                    "position": position,
                    "affiliations": [
                        _texte(x)
                        for x in auteur.findall("AffiliationInfo/Affiliation")
                        if _texte(x)
                    ],
                }
            )

        identifiants = {
            x.attrib.get("IdType", "").lower(): _texte(x)
            for x in entree.findall("PubmedData/ArticleIdList/ArticleId")
        }
        articles_lies = [
            {
                "type_relation": x.attrib.get("RefType", ""),
                "pmid_lie": _texte(x.find("PMID")),
                "source": _texte(x.find("RefSource")),
            }
            for x in citation.findall("CommentsCorrectionsList/CommentsCorrections")
            if _texte(x.find("PMID"))
        ]
        articles.append(
            {
                "pmid": pmid,
                "titre": _texte(article.find("ArticleTitle")),
                "resume": resume,
                "date_publication": date,
                "annee": annee,
                "doi": identifiants.get("doi", ""),
                "revue": _premier_texte(article, ["Journal/Title", "Journal/ISOAbbreviation"]),
                "langue": _texte(article.find("Language")),
                "mots_cles": [
                    _texte(x) for x in citation.findall("KeywordList/Keyword") if _texte(x)
                ],
                "types_publication": [
                    _texte(x)
                    for x in article.findall("PublicationTypeList/PublicationType")
                    if _texte(x)
                ],
                "auteurs": auteurs,
                "articles_lies": articles_lies,
            }
        )
    return articles


class ClientPubMed:
    """Client ESearch/EFetch avec temporisation, reprise et découpage contrôlé."""

    def __init__(self, configuration: ConfigurationNCBI) -> None:
        self.configuration = configuration
        self._dernier_appel = 0.0
        self.session = requests.Session()
        reprises = Retry(
            total=5,
            backoff_factor=0.8,
            status_forcelist=(429, 500, 502, 503, 504),
            allowed_methods=frozenset({"GET", "POST"}),
        )
        self.session.mount("https://", HTTPAdapter(max_retries=reprises))

    def _parametres_communs(self) -> dict[str, str]:
        parametres = {
            "tool": self.configuration.outil,
            "email": self.configuration.courriel,
        }
        if self.configuration.cle_api:
            parametres["api_key"] = self.configuration.cle_api
        return parametres

    def _attendre(self) -> None:
        ecoule = time.monotonic() - self._dernier_appel
        reste = self.configuration.delai_entre_requetes - ecoule
        if reste > 0:
            time.sleep(reste)

    def _get(self, chemin: str, parametres: dict[str, str]) -> requests.Response:
        self._attendre()
        reponse = self.session.get(
            f"{BASE_EUTILS}/{chemin}",
            params={**parametres, **self._parametres_communs()},
            timeout=self.configuration.delai_expiration,
        )
        self._dernier_appel = time.monotonic()
        reponse.raise_for_status()
        return reponse

    def rechercher_pmids(self, requete: str, debut: int, fin: int) -> list[str]:
        """Retourne les PMID d'une tranche et refuse toute troncature silencieuse."""

        reponse = self._get(
            "esearch.fcgi",
            {
                "db": "pubmed",
                "term": requete,
                "datetype": "pdat",
                "mindate": str(debut),
                "maxdate": str(fin),
                "retmode": "json",
                "retmax": "10000",
                "sort": "pub_date",
            },
        ).json()["esearchresult"]
        total = int(reponse["count"])
        if total > 10_000:
            raise RuntimeError(
                f"La tranche {debut}-{fin} contient {total} résultats. "
                "Découpez-la davantage pour éviter la limite ESearch de 10 000 PMID."
            )
        return list(reponse["idlist"])

    def recuperer_articles(
        self, pmids: Iterable[str], taille_lot: int = 200
    ) -> Iterator[dict[str, Any]]:
        """Télécharge les notices XML par lots, conformément aux recommandations NCBI."""

        identifiants = list(dict.fromkeys(pmids))
        if not 1 <= taille_lot <= 200:
            raise ValueError("La taille d'un lot doit être comprise entre 1 et 200.")
        for debut in range(0, len(identifiants), taille_lot):
            lot = identifiants[debut : debut + taille_lot]
            xml = self._get(
                "efetch.fcgi",
                {"db": "pubmed", "id": ",".join(lot), "retmode": "xml"},
            ).content
            yield from analyser_xml_pubmed(xml)


def ecrire_jsonl(articles: Iterable[dict[str, Any]], destination: Path) -> int:
    """Écrit les notices en JSON Lines afin de conserver les listes imbriquées."""

    destination.parent.mkdir(parents=True, exist_ok=True)
    total = 0
    with destination.open("w", encoding="utf-8") as flux:
        for article in articles:
            flux.write(json.dumps(article, ensure_ascii=False) + "\n")
            total += 1
    return total
