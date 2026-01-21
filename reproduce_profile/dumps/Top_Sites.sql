-- TABLE: meta
CREATE TABLE meta(key LONGVARCHAR NOT NULL UNIQUE PRIMARY KEY, value LONGVARCHAR);

-- TABLE: top_sites
CREATE TABLE top_sites(url TEXT NOT NULL PRIMARY KEY,url_rank INTEGER NOT NULL,title TEXT NOT NULL);

-- DATA: meta
INSERT INTO meta (key, value) VALUES ('mmap_status', '-1');
INSERT INTO meta (key, value) VALUES ('version', '5');
INSERT INTO meta (key, value) VALUES ('last_compatible_version', '5');

