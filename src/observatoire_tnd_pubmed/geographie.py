"""Enrichissement géographique prudent à partir des affiliations textuelles."""

from __future__ import annotations

import re

PAYS_CONTINENTS = {
    "france": ("France", "Europe"),
    "germany": ("Allemagne", "Europe"),
    "italy": ("Italie", "Europe"),
    "spain": ("Espagne", "Europe"),
    "united kingdom": ("Royaume-Uni", "Europe"),
    "uk": ("Royaume-Uni", "Europe"),
    "united states": ("États-Unis", "Amérique du Nord"),
    "usa": ("États-Unis", "Amérique du Nord"),
    "canada": ("Canada", "Amérique du Nord"),
    "brazil": ("Brésil", "Amérique du Sud"),
    "australia": ("Australie", "Océanie"),
    "china": ("Chine", "Asie"),
    "japan": ("Japon", "Asie"),
    "india": ("Inde", "Asie"),
    "south africa": ("Afrique du Sud", "Afrique"),
}


def detecter_pays_continent(affiliation: str) -> tuple[str, str]:
    """Détecte un pays connu ; renvoie Non spécifié plutôt qu'une fausse certitude."""

    texte = affiliation.casefold()
    for terme, resultat in sorted(PAYS_CONTINENTS.items(), key=lambda x: -len(x[0])):
        if re.search(rf"(?<![a-z]){re.escape(terme)}(?![a-z])", texte):
            return resultat
    return "Non spécifié", "Non spécifié"
