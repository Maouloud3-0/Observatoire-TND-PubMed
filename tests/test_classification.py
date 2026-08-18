from observatoire_tnd_pubmed.classification import classer_sujets, classer_troubles


def test_classification_conserve_la_preuve() -> None:
    resultat = classer_troubles(
        "Autism spectrum disorder in children", "A clinical assessment.", []
    )
    assert resultat == [
        {
            "classe": "Troubles du spectre de l'autisme",
            "champ": "titre",
            "terme": "autism",
        }
    ]


def test_limites_de_mots_evitent_un_faux_positif() -> None:
    assert classer_sujets("A management tool", "The effect was measured.", [])
    assert not classer_sujets("A factorization method", "No research angle here.", [])
