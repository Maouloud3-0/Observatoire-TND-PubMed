"""Classification lexicale explicable des troubles et des angles de recherche."""

from __future__ import annotations

import re
import unicodedata
from collections.abc import Mapping

LEXIQUE_TROUBLES: dict[str, tuple[str, ...]] = {
    "Troubles du spectre de l'autisme": ("autism", "autistic", "asperger"),
    "TDAH": ("adhd", "attention deficit hyperactivity"),
    "Trouble du développement intellectuel": (
        "intellectual disability",
        "intellectual developmental disorder",
    ),
    "Troubles neurodéveloppementaux": ("neurodevelopmental disorder",),
    "Trouble spécifique des apprentissages": (
        "specific learning disorder",
        "dyslexia",
        "dyscalculia",
    ),
    "Troubles moteurs": ("motor disorder", "developmental coordination disorder"),
    "Troubles de la communication": ("communication disorder", "language disorder"),
}

LEXIQUE_SUJETS: dict[str, tuple[str, ...]] = {
    "Étude": ("study", "trial", "cohort"),
    "Traitement": ("treatment", "medication"),
    "Diagnostic": ("diagnosis", "diagnostic"),
    "Facteurs": ("factor", "risk factor", "predictor"),
    "Évaluation": ("assessment", "evaluation"),
    "Impact": ("impact", "effect", "outcome"),
    "Intervention": ("intervention",),
    "Thérapie": ("therapy", "therapeutic"),
    "Prise en charge": ("management", "care pathway"),
    "Comorbidité": ("comorbidity", "comorbid"),
    "Méta-analyse": ("meta-analysis", "systematic review"),
    "Évolution": ("evolution", "longitudinal", "trajectory"),
    "Cause": ("cause", "etiology", "aetiology"),
}


def _normaliser(texte: str) -> str:
    decomposed = unicodedata.normalize("NFKD", texte.casefold())
    return "".join(caractere for caractere in decomposed if not unicodedata.combining(caractere))


def _contient(expression: str, texte: str) -> bool:
    motif = rf"(?<![a-z0-9]){re.escape(_normaliser(expression))}(?![a-z0-9])"
    return bool(re.search(motif, _normaliser(texte)))


def classer(
    champs: Mapping[str, str], lexique: Mapping[str, tuple[str, ...]]
) -> list[dict[str, str]]:
    """Retourne toutes les classes trouvées avec le champ et le terme déclencheur."""

    resultats: list[dict[str, str]] = []
    for classe, expressions in lexique.items():
        trouve = False
        for champ, texte in champs.items():
            for expression in expressions:
                if _contient(expression, texte):
                    resultats.append({"classe": classe, "champ": champ, "terme": expression})
                    trouve = True
                    break
            if trouve:
                break
    return resultats


def classer_troubles(titre: str, resume: str, mots_cles: list[str]) -> list[dict[str, str]]:
    return classer(
        {"titre": titre, "mots_cles": " ".join(mots_cles), "resume": resume},
        LEXIQUE_TROUBLES,
    )


def classer_sujets(titre: str, resume: str, mots_cles: list[str]) -> list[dict[str, str]]:
    return classer(
        {"titre": titre, "resume": resume, "mots_cles": " ".join(mots_cles)},
        LEXIQUE_SUJETS,
    )
