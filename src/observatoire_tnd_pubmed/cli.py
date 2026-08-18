"""Interface en ligne de commande du pipeline de collecte."""

from __future__ import annotations

import argparse
from collections.abc import Iterator
from pathlib import Path

from .collecte_pubmed import ClientPubMed, ecrire_jsonl
from .configuration import REQUETE_TND, ConfigurationNCBI, periodes_annuelles


def _collecter(client: ClientPubMed, requete: str, debut: int, fin: int) -> Iterator[dict]:
    deja_vus: set[str] = set()
    for annee_debut, annee_fin in periodes_annuelles(debut, fin):
        pmids = client.rechercher_pmids(requete, annee_debut, annee_fin)
        nouveaux = [pmid for pmid in pmids if pmid not in deja_vus]
        deja_vus.update(nouveaux)
        yield from client.recuperer_articles(nouveaux)


def main() -> None:
    analyseur = argparse.ArgumentParser(
        description="Collecter les métadonnées PubMed sur les TND au format JSON Lines."
    )
    analyseur.add_argument("--debut", type=int, default=1994)
    analyseur.add_argument("--fin", type=int, default=2024)
    analyseur.add_argument("--requete", default=REQUETE_TND)
    analyseur.add_argument("--sortie", type=Path, default=Path("sorties/notices_pubmed.jsonl"))
    arguments = analyseur.parse_args()

    configuration = ConfigurationNCBI.depuis_environnement()
    total = ecrire_jsonl(
        _collecter(
            ClientPubMed(configuration),
            arguments.requete,
            arguments.debut,
            arguments.fin,
        ),
        arguments.sortie,
    )
    print(f"{total} notices écrites dans {arguments.sortie}")


if __name__ == "__main__":
    main()
