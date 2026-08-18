"""Exporte des agrégats légers depuis la base académique pour consultation sur GitHub."""

from __future__ import annotations

import argparse
import csv
import sqlite3
from pathlib import Path

REQUETES = {
    "articles_par_annee.csv": """
        SELECT substr(date, 1, 4) AS annee, COUNT(*) AS nombre_articles
        FROM article
        WHERE date IS NOT NULL AND trim(date) <> ''
        GROUP BY substr(date, 1, 4)
        ORDER BY annee
    """,
    "articles_par_trouble.csv": """
        SELECT t.type AS trouble, COUNT(DISTINCT r.pmid) AS nombre_articles
        FROM traiter AS r
        JOIN trouble AS t ON t.id_trouble = r.id_trouble
        GROUP BY t.type ORDER BY nombre_articles DESC
    """,
    "articles_par_sujet.csv": """
        SELECT s.mot AS sujet, COUNT(DISTINCT a.pmid) AS nombre_articles
        FROM aborder AS a
        JOIN sujet AS s ON s.id_sujet = a.id_sujet
        GROUP BY s.mot ORDER BY nombre_articles DESC
    """,
    "contributions_par_continent.csv": """
        SELECT continent, COUNT(*) AS nombre_contributions
        FROM auteurs GROUP BY continent ORDER BY nombre_contributions DESC
    """,
}


def exporter(base: Path, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    connexion = sqlite3.connect(f"file:{base.as_posix()}?mode=ro", uri=True)
    try:
        for nom, requete in REQUETES.items():
            curseur = connexion.execute(requete)
            with (destination / nom).open("w", encoding="utf-8-sig", newline="") as flux:
                ecrivain = csv.writer(flux)
                ecrivain.writerow([colonne[0] for colonne in curseur.description])
                ecrivain.writerows(curseur)
    finally:
        connexion.close()


if __name__ == "__main__":
    analyseur = argparse.ArgumentParser()
    analyseur.add_argument("base", type=Path)
    analyseur.add_argument("destination", type=Path)
    arguments = analyseur.parse_args()
    exporter(arguments.base, arguments.destination)
