-- TABLE: meta
CREATE TABLE meta(key LONGVARCHAR NOT NULL UNIQUE PRIMARY KEY, value LONGVARCHAR);

-- TABLE: public_sets
CREATE TABLE public_sets(version TEXT NOT NULL,site TEXT NOT NULL,primary_site TEXT NOT NULL,site_type INTEGER NOT NULL,PRIMARY KEY(version,site))WITHOUT ROWID;

-- TABLE: browser_context_sets_version
CREATE TABLE browser_context_sets_version(browser_context_id TEXT PRIMARY KEY NOT NULL,public_sets_version TEXT NOT NULL)WITHOUT ROWID;

-- TABLE: browser_context_sites_to_clear
CREATE TABLE browser_context_sites_to_clear(browser_context_id TEXT NOT NULL,site TEXT NOT NULL,marked_at_run INTEGER NOT NULL,PRIMARY KEY(browser_context_id,site))WITHOUT ROWID;

-- TABLE: browser_contexts_cleared
CREATE TABLE browser_contexts_cleared(browser_context_id TEXT PRIMARY KEY NOT NULL,cleared_at_run INTEGER NOT NULL)WITHOUT ROWID;

-- TABLE: policy_configurations
CREATE TABLE policy_configurations(browser_context_id TEXT NOT NULL,site TEXT NOT NULL,primary_site TEXT,PRIMARY KEY(browser_context_id,site))WITHOUT ROWID;

-- TABLE: manual_configurations
CREATE TABLE manual_configurations(browser_context_id TEXT NOT NULL,site TEXT NOT NULL,primary_site TEXT,site_type INTEGER,PRIMARY KEY(browser_context_id,site))WITHOUT ROWID;

-- DATA: meta
INSERT INTO meta (key, value) VALUES ('mmap_status', '-1');
INSERT INTO meta (key, value) VALUES ('version', '5');
INSERT INTO meta (key, value) VALUES ('last_compatible_version', '5');
INSERT INTO meta (key, value) VALUES ('run_count', '5');

