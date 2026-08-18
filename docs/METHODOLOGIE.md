# Méthodologie

## 1. Question étudiée

Le projet observe comment la recherche consacrée aux troubles du neurodéveloppement évolue dans le temps et se répartit par trouble, sujet, pays et continent. Il s'agit d'une étude bibliométrique descriptive, pas d'une étude clinique ni d'une démonstration causale.

## 2. Acquisition

La version modernisée interroge les E-utilities officielles du NCBI : ESearch obtient les PMID et EFetch retourne les notices PubMed XML. La requête est découpée par année, car PubMed limite ESearch aux 10 000 premiers résultats d'une recherche. Une tranche qui dépasse ce seuil provoque une erreur explicite et doit être subdivisée.

Chaque appel contient les paramètres `tool` et `email`. Le client reste sous trois requêtes par seconde sans clé API et sous dix avec clé, utilise des lots de 200 identifiants, un délai d'expiration et des reprises avec attente progressive.

## 3. Métadonnées conservées

Le parseur extrait le PMID, le titre, le résumé, la date, l'année, le DOI, la revue, la langue, les auteurs, leurs affiliations et ORCID éventuels, les mots-clés, les types de publication et les références PubMed liées. Le texte intégral n'est pas collecté.

## 4. Classification

Les catégories de troubles et de sujets reposent sur des lexiques publics dans le code. La recherche utilise des limites de mots et conserve, pour chaque attribution, le champ et le terme déclencheur. Cette trace rend le résultat contrôlable, mais la méthode reste une heuristique lexicale : elle ne comprend ni le contexte, ni la négation, ni les nuances cliniques.

Un article peut appartenir à plusieurs troubles ou sujets. Les mesures du tableau de bord ne doivent donc pas additionner naïvement les catégories pour retrouver le total d'articles.

## 5. Normalisation et stockage

SQLite sépare articles, auteurs, relations auteur-article, troubles et sujets. Le schéma modernisé ajoute des clés étrangères, des contraintes d'unicité et des index, ainsi que des tables supplémentaires pour résumés, DOI, mots-clés et articles liés. Les noms des sept tables historiques restent compatibles avec le modèle Power BI existant.

## 6. Contrôles

Les contrôles portent sur l'intégrité SQLite, les relations orphelines, les doublons de relations, les valeurs manquantes et la cohérence des agrégats. Les tests unitaires vérifient le parseur XML, les limites lexicales, la stabilité des identifiants techniques et les contraintes du schéma sans appeler PubMed.

