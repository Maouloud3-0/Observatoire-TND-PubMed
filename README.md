# Observatoire TND PubMed

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![PubMed](https://img.shields.io/badge/Source-PubMed-326599?logo=pubmed&logoColor=white)](https://pubmed.ncbi.nlm.nih.gov/)
[![SQLite](https://img.shields.io/badge/Base-SQLite-003B57?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Power BI](https://img.shields.io/badge/Tableau_de_bord-Power_BI-F2C811?logo=powerbi&logoColor=000000)](https://www.microsoft.com/fr-fr/power-platform/products/power-bi)
[![Tests](https://img.shields.io/badge/Tests-6_r%C3%A9ussis-2EA44F?logo=pytest&logoColor=white)](tests)
[![Licence MIT](https://img.shields.io/badge/Licence-MIT-yellow.svg)](LICENSE)

Pipeline bibliométrique en Python et SQLite, accompagné d'un tableau de bord Power BI, pour explorer l'évolution de la recherche PubMed sur les troubles du neurodéveloppement (TND).

## Ce que montre le projet

Le projet collecte les **métadonnées bibliographiques** de PubMed — titre, résumé, date, auteurs, affiliations, mots-clés, DOI et références liées — sans télécharger le texte intégral des articles. Les notices sont nettoyées, enrichies par des catégories lexicales explicables, structurées dans SQLite puis explorées dans Power BI.

Le jeu académique fourni couvre principalement la période **1994–2024**. La base contient 86 741 articles et 338 126 contributions auteur-article. Le tableau de bord historique affiche environ 83 000 articles lorsque seules les publications reliées à un auteur sont comptées.

> Le périmètre réel est celui des troubles du neurodéveloppement : autisme, TDAH, développement intellectuel, apprentissages, communication et motricité. Il ne couvre pas tous les troubles du DSM-5.

## Architecture

```text
Observatoire-TND-PubMed/
├── src/observatoire_tnd_pubmed/  # collecte, parsing, classification et contrôles
├── sql/schema.sql                # schéma SQLite compatible et renforcé
├── tests/                        # tests unitaires sans appel réseau
├── donnees/
│   ├── base_complete/            # base académique compressée
│   └── extraits/                 # agrégats consultables sans Power BI
├── powerbi/                      # tableau de bord .pbix original
├── docs/                         # méthode, limites et rapport de modernisation
└── outils/                       # export reproductible des agrégats
```

## Démarrage rapide

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
pytest
```

Pour une collecte réelle, copiez `.env.example` vers `.env`, définissez `NCBI_EMAIL`, puis chargez les variables dans votre terminal. La clé `NCBI_API_KEY` reste facultative.

```powershell
$env:NCBI_EMAIL="votre.adresse@example.com"
observatoire-tnd --debut 2024 --fin 2024 --sortie sorties/notices_2024.jsonl
```

Le client impose une temporisation, réessaie les erreurs transitoires, récupère les notices XML par lots de 200 et refuse silencieusement aucune tranche dépassant la limite ESearch de 10 000 résultats.

## Ouvrir les livrables

- Décompresser [`ma_base_projet_dashboard.zip`](donnees/base_complete/ma_base_projet_dashboard.zip), puis ouvrir la base SQLite.
- Ouvrir [`Projet_tableau_de_bord.pbix`](powerbi/Projet_tableau_de_bord.pbix) avec Power BI Desktop.
- Si Power BI ne retrouve pas la base, modifier la source ODBC/SQLite pour pointer vers le fichier local décompressé, puis actualiser.
- Les quatre fichiers de [`donnees/extraits`](donnees/extraits) permettent de contrôler les principaux agrégats sans Power BI.

## Documentation

- [Méthodologie](docs/METHODOLOGIE.md)
- [Dictionnaire des données](docs/DICTIONNAIRE_DONNEES.md)
- [Modèle Power BI](docs/MODELE_POWER_BI.md)
- [Limites et interprétation](docs/LIMITES.md)
- [Rapport de modernisation](docs/RAPPORT_MODERNISATION.md)
- [Préparation à l'entretien](docs/NOTES_ENTRETIEN.md)
- [Sources techniques](docs/SOURCES.md)

## Cadre universitaire et attribution

Le travail initial a été réalisé en 2025 dans le cadre d'un projet universitaire de M1 SID, en binôme avec **Emeline Kleinhans**. Cette version de portfolio conserve les livrables académiques et ajoute une couche d'ingénierie, de tests et de documentation. Les apports de modernisation sont décrits précisément afin de distinguer l'existant du travail ultérieur.

L'assistance de Codex a été utilisée pour auditer, restructurer, documenter et tester cette version de portfolio. Les décisions et leurs justifications sont consignées dans le rapport de modernisation.

## Licence et données

Le code ajouté est distribué sous licence MIT. Les notices PubMed, résumés et autres métadonnées restent soumis aux politiques du NCBI et aux droits applicables à leurs sources. Le dépôt ne republie pas le texte intégral des articles.
