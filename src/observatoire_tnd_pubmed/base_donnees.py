"""Création d'une base SQLite documentée et compatible avec le modèle Power BI historique."""

from __future__ import annotations

import hashlib
import sqlite3
from pathlib import Path


def identifiant_auteur(nom: str, prenom: str = "", orcid: str = "") -> str:
    """Produit un identifiant stable, sans prétendre résoudre les homonymes."""

    cle = orcid.strip().lower() or f"{nom.strip().lower()}|{prenom.strip().lower()}"
    return hashlib.sha256(cle.encode("utf-8")).hexdigest()[:16]


def creer_base(destination: Path, schema: Path | None = None) -> sqlite3.Connection:
    """Crée une base vide avec clés, contraintes et index utiles au tableau de bord."""

    if schema is None:
        schema = Path(__file__).resolve().parents[2] / "sql" / "schema.sql"
    connexion = sqlite3.connect(destination)
    connexion.execute("PRAGMA foreign_keys = ON")
    connexion.executescript(schema.read_text(encoding="utf-8"))
    return connexion


def auditer_base(connexion: sqlite3.Connection) -> dict[str, int | str]:
    """Calcule les indicateurs minimaux de contrôle d'une base académique."""

    def valeur(requete: str) -> int | str:
        resultat = connexion.execute(requete).fetchone()
        return resultat[0] if resultat else 0

    return {
        "integrite": valeur("PRAGMA integrity_check"),
        "articles": valeur("SELECT COUNT(*) FROM article"),
        "auteurs_enregistres": valeur("SELECT COUNT(*) FROM auteurs"),
        "contributions": valeur("SELECT COUNT(*) FROM rediger"),
        "articles_sans_date": valeur(
            "SELECT COUNT(*) FROM article WHERE date IS NULL OR TRIM(date) = ''"
        ),
        "affiliations_non_specifiees": valeur(
            "SELECT COUNT(*) FROM auteurs WHERE pays = 'Non spécifié'"
        ),
    }
