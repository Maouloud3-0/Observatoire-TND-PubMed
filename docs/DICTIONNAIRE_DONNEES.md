# Dictionnaire des données

## Tables historiques utilisées par Power BI

| Table | Grain | Champs principaux | Rôle |
|---|---|---|---|
| `article` | une publication | `pmid`, `titre`, `date` | Référentiel des publications |
| `auteurs` | un enregistrement d'auteur | `id_auteur`, `nom`, `affiliation`, `pays`, `continent`, `developpement` | Auteur et enrichissement géographique |
| `rediger` | une contribution | `pmid`, `id_auteur` | Relation article-auteur |
| `trouble` | une catégorie | `id_trouble`, `type` | Référentiel des TND |
| `traiter` | une attribution | `pmid`, `id_trouble` | Relation article-trouble |
| `sujet` | un angle de recherche | `id_sujet`, `mot` | Référentiel des sujets |
| `aborder` | une attribution | `pmid`, `id_sujet` | Relation article-sujet |

## Extensions du schéma modernisé

| Table | Contenu |
|---|---|
| `detail_article` | résumé, DOI, revue et langue |
| `mot_cle` / `article_mot_cle` | mots-clés normalisés et relations |
| `article_lie` | PMID cité ou relié et type de relation |

## Précautions de lecture

- `pmid` est l'identifiant stable d'une notice PubMed.
- `id_auteur` est un identifiant technique. Même avec ORCID lorsqu'il existe, il ne garantit pas l'identification unique d'une personne dans tous les cas.
- `rediger` mesure des **contributions auteur-article**. Un même chercheur peut apparaître plusieurs fois ou sous plusieurs variantes de nom.
- `Pays`, `Continent` et `Dev` proviennent d'une détection heuristique dans l'affiliation. `Non spécifié` signifie que le pays n'a pas été déterminé de façon suffisamment sûre.
- `TypeTrouble` et `TypeSujet` sont des catégories lexicales et non des annotations cliniques validées.
