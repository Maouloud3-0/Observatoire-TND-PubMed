PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS article (
    pmid TEXT PRIMARY KEY,
    titre TEXT NOT NULL,
    date TEXT,
    annee INTEGER CHECK (annee IS NULL OR annee BETWEEN 1800 AND 2200)
);

CREATE TABLE IF NOT EXISTS auteurs (
    id_auteur TEXT PRIMARY KEY,
    nom TEXT NOT NULL,
    affiliation TEXT,
    pays TEXT NOT NULL DEFAULT 'Non spécifié',
    continent TEXT NOT NULL DEFAULT 'Non spécifié',
    developpement TEXT NOT NULL DEFAULT 'Non spécifié',
    orcid TEXT
);

CREATE TABLE IF NOT EXISTS rediger (
    pmid TEXT NOT NULL REFERENCES article(pmid) ON DELETE CASCADE,
    id_auteur TEXT NOT NULL REFERENCES auteurs(id_auteur) ON DELETE CASCADE,
    position INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (pmid, id_auteur, position)
);

CREATE TABLE IF NOT EXISTS trouble (
    id_trouble TEXT PRIMARY KEY,
    type TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS traiter (
    pmid TEXT NOT NULL REFERENCES article(pmid) ON DELETE CASCADE,
    id_trouble TEXT NOT NULL REFERENCES trouble(id_trouble),
    champ_source TEXT,
    terme_source TEXT,
    PRIMARY KEY (pmid, id_trouble)
);

CREATE TABLE IF NOT EXISTS sujet (
    id_sujet TEXT PRIMARY KEY,
    mot TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS aborder (
    pmid TEXT NOT NULL REFERENCES article(pmid) ON DELETE CASCADE,
    id_sujet TEXT NOT NULL REFERENCES sujet(id_sujet),
    champ_source TEXT,
    terme_source TEXT,
    PRIMARY KEY (pmid, id_sujet)
);

CREATE TABLE IF NOT EXISTS detail_article (
    pmid TEXT PRIMARY KEY REFERENCES article(pmid) ON DELETE CASCADE,
    resume TEXT,
    DOI TEXT,
    revue TEXT,
    langue TEXT
);

CREATE TABLE IF NOT EXISTS mot_cle (
    id_mot_cle INTEGER PRIMARY KEY AUTOINCREMENT,
    libelle TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS article_mot_cle (
    pmid TEXT NOT NULL REFERENCES article(pmid) ON DELETE CASCADE,
    id_mot_cle INTEGER NOT NULL REFERENCES mot_cle(id_mot_cle),
    PRIMARY KEY (pmid, id_mot_cle)
);

CREATE TABLE IF NOT EXISTS article_lie (
    pmid_source TEXT NOT NULL REFERENCES article(pmid) ON DELETE CASCADE,
    pmid_lie TEXT NOT NULL,
    type_relation TEXT NOT NULL DEFAULT '',
    source_bibliographique TEXT,
    PRIMARY KEY (pmid_source, pmid_lie, type_relation)
);

CREATE INDEX IF NOT EXISTS idx_article_annee ON article(annee);
CREATE INDEX IF NOT EXISTS idx_auteurs_pays ON auteurs(pays);
CREATE INDEX IF NOT EXISTS idx_auteurs_continent ON auteurs(continent);
CREATE INDEX IF NOT EXISTS idx_rediger_auteur ON rediger(id_auteur);
CREATE INDEX IF NOT EXISTS idx_traiter_trouble ON traiter(id_trouble);
CREATE INDEX IF NOT EXISTS idx_aborder_sujet ON aborder(id_sujet);
