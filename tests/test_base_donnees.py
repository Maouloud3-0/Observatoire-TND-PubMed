import sqlite3
from pathlib import Path

import pytest

from observatoire_tnd_pubmed.base_donnees import creer_base, identifiant_auteur


def test_identifiant_auteur_est_stable() -> None:
    assert identifiant_auteur("Dupont", "Alice") == identifiant_auteur("dupont", "alice")
    assert identifiant_auteur("Dupont", "Alice", "0000-0001") != identifiant_auteur(
        "Dupont", "Alice"
    )


def test_schema_refuse_une_relation_dupliquee(tmp_path: Path) -> None:
    connexion = creer_base(tmp_path / "test.db")
    connexion.execute("INSERT INTO article VALUES ('1', 'Titre', '2024-01-01', 2024)")
    connexion.execute("INSERT INTO auteurs (id_auteur, nom) VALUES ('a1', 'Alice Dupont')")
    connexion.execute("INSERT INTO rediger VALUES ('1', 'a1', 1)")
    with pytest.raises(sqlite3.IntegrityError):
        connexion.execute("INSERT INTO rediger VALUES ('1', 'a1', 1)")
    connexion.close()


def test_schema_contient_les_index_attendus(tmp_path: Path) -> None:
    connexion = creer_base(tmp_path / "test.db")
    index = {
        ligne[0]
        for ligne in connexion.execute("SELECT name FROM sqlite_master WHERE type = 'index'")
    }
    assert {"idx_article_annee", "idx_auteurs_pays", "idx_traiter_trouble"} <= index
    connexion.close()
