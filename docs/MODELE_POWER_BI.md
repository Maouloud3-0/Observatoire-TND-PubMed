# Modèle Power BI

Le fichier PBIX historique contient deux pages.

## Page « Article »

- filtres par pays, continent, année et niveau de développement ;
- cartes de nombre d'articles et d'auteurs enregistrés ;
- carte géographique ;
- répartition des publications par sujet ;
- boutons de navigation et de réinitialisation.

## Page « Trouble et sujet »

- évolution annuelle par trouble ;
- évolution annuelle par sujet ;
- filtres sur les sept catégories de troubles et les treize catégories de sujets ;
- carte du nombre d'articles ;
- arbre de décomposition trouble/sujet ;
- répartition des contributions d'auteurs par continent.

## Actualisation locale

Le PBIX utilisait une connexion SQLite via ODBC. Après extraction de la base, le chemin local doit généralement être remplacé dans les paramètres de source Power BI. Cette contrainte est liée au format PBIX : le chemin absolu d'un poste ne peut pas être portable d'une machine à l'autre.

Pour éviter une formulation trompeuse, la mesure historiquement intitulée « nombre d'auteurs » doit être comprise comme un nombre d'enregistrements ou de contributions d'auteurs, et non comme un décompte garanti de personnes uniques.

