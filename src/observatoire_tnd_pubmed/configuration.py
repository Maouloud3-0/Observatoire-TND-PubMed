"""Configuration du client NCBI et du périmètre bibliographique."""

from __future__ import annotations

import os
from dataclasses import dataclass

REQUETE_TND = (
    '"neurodevelopmental disorders"[Title/Abstract] OR '
    '"autism spectrum disorder"[Title/Abstract] OR '
    '"attention deficit hyperactivity disorder"[Title/Abstract] OR '
    '"intellectual disability"[Title/Abstract] OR '
    '"specific learning disorder"[Title/Abstract] OR '
    '"communication disorder"[Title/Abstract] OR '
    '"motor disorder"[Title/Abstract]'
)


@dataclass(frozen=True, slots=True)
class ConfigurationNCBI:
    """Paramètres exigés ou recommandés par les E-utilities du NCBI."""

    courriel: str
    cle_api: str | None = None
    outil: str = "observatoire_tnd_pubmed"
    delai_sans_cle: float = 0.34
    delai_avec_cle: float = 0.11
    delai_expiration: float = 30.0

    @classmethod
    def depuis_environnement(cls) -> ConfigurationNCBI:
        courriel = os.getenv("NCBI_EMAIL", "").strip()
        if not courriel or "@" not in courriel:
            raise ValueError("Définissez NCBI_EMAIL avec une adresse valide avant toute collecte.")
        return cls(courriel=courriel, cle_api=os.getenv("NCBI_API_KEY") or None)

    @property
    def delai_entre_requetes(self) -> float:
        return self.delai_avec_cle if self.cle_api else self.delai_sans_cle


def periodes_annuelles(debut: int = 1994, fin: int = 2024) -> list[tuple[int, int]]:
    """Produit des tranches annuelles pour rester sous la limite PubMed de 10 000 PMID."""

    if debut > fin:
        raise ValueError("L'année de début doit précéder l'année de fin.")
    return [(annee, annee) for annee in range(debut, fin + 1)]
