# Rapport de modernisation

## Objet du rapport

Ce document distingue le projet académique de 2025 de la couche de modernisation ajoutée pour le portfolio. Chaque changement répond à un défaut observé et reste explicable en entretien.

## État initial audité

- Le téléchargement reposait sur le HTML de PubMed et des sélecteurs de page.
- Les scripts étaient liés à Google Colab et à des chemins Google Drive.
- Un fichier Python était incomplet et ne pouvait pas s'exécuter.
- Les mêmes notebooks existaient à deux emplacements.
- Les appels HTTP n'avaient ni délai d'expiration, ni reprise, ni temporisation documentée.
- La base SQLite ne possédait pas d'index sur les tables de relations.
- Les relations n'imposaient pas toutes l'unicité des couples métier.
- Les identifiants d'auteurs étaient des fragments d'UUID aléatoires par occurrence.
- La catégorisation reposait sur des sous-chaînes, sans limites de mots ni preuve conservée.
- Le fichier PBIX dépendait d'un chemin local vers la base SQLite.
- La base brute dépassait la limite GitHub de 100 Mo par fichier.

## Décisions et justifications

| Problème | Solution retenue | Pourquoi |
|---|---|---|
| Scraping HTML fragile | ESearch et EFetch officiels | Interface documentée et XML structuré |
| Plus de 10 000 résultats | Découpage annuel et arrêt explicite si une tranche dépasse 10 000 | Évite une troncature silencieuse |
| Risque de surcharge NCBI | 0,34 s sans clé, 0,11 s avec clé, lots de 200 | Respecte les plafonds de 3 et 10 requêtes/s |
| Erreurs réseau transitoires | Délai d'expiration et cinq reprises progressives | Rend une collecte longue moins fragile |
| Secrets dans le code | Variables `NCBI_EMAIL` et `NCBI_API_KEY`, fichier `.env` ignoré | Aucun courriel ni clé personnelle versionné |
| Notebooks dépendants de Colab | Paquet Python installable et CLI | Exécution locale reproductible |
| Script incomplet | Nouveau chemin d'exécution testé | Ne masque pas l'erreur historique et fournit une alternative opérationnelle |
| Catégories opaques | Lexiques centralisés, limites de mots, champ et terme conservés | Facilite l'audit sans prétendre à une validation clinique |
| Identifiants auteurs aléatoires | Empreinte déterministe fondée sur ORCID ou nom/prénom | Stabilité technique ; les homonymes restent documentés |
| Relations potentiellement dupliquées | Clés primaires composées | Empêche les doublons exacts |
| Requêtes lentes | Index sur année, pays, continent, auteur, trouble et sujet | Accélère les filtres du tableau de bord |
| Métadonnées perdues dans le modèle initial | Tables pour résumé, DOI, mots-clés et articles liés | Préserve les informations demandées sans renommer les sept tables historiques |
| Base de 108 Mo | Archive ZIP d'environ 30 Mo | Respecte la limite GitHub tout en conservant l'instantané complet |
| PBIX non consultable sur GitHub | Agrégats CSV légers et dictionnaire | Rend les résultats principaux inspectables sans Power BI |
| Mesures ambiguës | Terminologie « contributions auteur-article » | Évite de confondre occurrences et personnes uniques |

## Ce qui n'a pas été modifié

Le dossier source d'origine n'a pas été réécrit. Le PBIX, le rapport, la présentation et les résultats académiques sont conservés comme livrables historiques. La base incluse n'a pas été artificiellement corrigée : ses dates manquantes, affiliations non spécifiées et conventions d'identifiants sont décrites comme limites. Aucune nouvelle conclusion clinique n'a été ajoutée.

## Contrôles effectués sur l'instantané

- `PRAGMA integrity_check` : `ok` ;
- 86 741 articles ;
- 338 115 enregistrements d'auteurs ;
- 338 126 relations auteur-article ;
- aucune relation orpheline signalée par le contrôle des clés étrangères ;
- 5 146 articles sans date exploitable ;
- 45 805 affiliations avec géographie non spécifiée ;
- 3 497 articles sans relation auteur, ce qui explique l'écart entre 86 741 articles stockés et environ 83 000 articles affichés selon le chemin de filtre Power BI.

## Limites de la modernisation

Le pipeline modernisé est testé sur une notice XML de référence, mais une nouvelle collecte complète n'a pas été lancée : elle serait longue, produirait un instantané différent et nécessite l'adresse NCBI de l'exploitant. Le modèle PBIX historique n'a pas été redessiné ; ses sources doivent être repointées localement après extraction de la base.

## Traçabilité de l'assistance

Codex a été utilisé pour l'audit technique des fichiers, la proposition d'architecture, l'implémentation du paquet Python, la création des tests, l'export d'agrégats et la rédaction documentaire. Cette assistance ne change ni l'attribution du travail académique initial ni les limites des données.
