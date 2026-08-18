# Notes pour présenter le projet en entretien

## Résumé en 30 secondes

« Nous avons construit un observatoire bibliométrique des recherches PubMed sur les troubles du neurodéveloppement. J'ai travaillé sur la collecte et la transformation de métadonnées, leur structuration dans SQLite et leur visualisation dans Power BI. Pour la version portfolio, le scraping HTML fragile a été remplacé par un client fondé sur les E-utilities officielles, avec limites de débit, parsing XML, tests et documentation des biais. »

## Ce que je peux affirmer

- La base contient 86 741 articles et 338 126 relations auteur-article.
- Le tableau de bord comporte deux pages : géographie/publications, puis troubles/sujets.
- La collecte modernisée respecte la limite de 10 000 résultats ESearch en découpant par année.
- Les classifications sont lexicales et auditables ; elles ne sont pas présentées comme un modèle clinique.
- Le travail universitaire initial a été réalisé en binôme avec Emeline Kleinhans.

## Ce que je ne dois pas affirmer

- « Le projet couvre tout le DSM-5 » : faux, il se concentre sur les TND.
- « Il y a 338 115 chercheurs uniques » : non démontré, ce sont des enregistrements/contributions.
- « Le tableau de bord prouve une causalité » : il décrit des tendances.
- « J'ai entraîné un modèle d'intelligence artificielle » : la catégorisation repose sur des lexiques.
- « La base actuelle est parfaitement reproductible à l'identique » : PubMed évolue et l'instantané dépend de la date d'extraction.

## Question : pourquoi ne pas garder le scraping HTML ?

Les sélecteurs d'une page Web changent sans contrat de stabilité et rendent la pagination difficile. L'API E-utilities fournit une interface officielle, du XML structuré, des identifiants stables et des règles de débit documentées.

## Question : comment avez-vous traité plus de 10 000 résultats ?

PubMed limite ESearch aux 10 000 premiers PMID. Le pipeline segmente la recherche par année et arrête l'exécution si une tranche dépasse encore cette limite, au lieu de produire une base tronquée sans avertissement.

## Question : quelle est la principale limite des données ?

La résolution d'identité des auteurs. Les noms, initiales et affiliations varient, ORCID n'est pas toujours présent et la base historique créait un identifiant par occurrence. Je parle donc de contributions et je sépare clairement cette mesure du nombre de personnes uniques.

## Question : qu'avez-vous modernisé exactement ?

La couche portfolio ajoute un paquet Python installable, un client API temporisé avec reprises, un parseur XML testé, des catégories accompagnées de leur preuve lexicale, un schéma SQLite avec contraintes et index, des extraits contrôlables et une documentation des limites. Le PBIX et la base académique restent des livrables historiques conservés, pas des créations réécrites a posteriori.

