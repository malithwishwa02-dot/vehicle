-- TABLE: meta
CREATE TABLE meta(key LONGVARCHAR NOT NULL UNIQUE PRIMARY KEY, value LONGVARCHAR);

-- TABLE: plus_addresses
CREATE TABLE plus_addresses (profile_id VARCHAR PRIMARY KEY, facet VARCHAR, plus_address VARCHAR);

-- TABLE: plus_address_sync_model_type_state
CREATE TABLE plus_address_sync_model_type_state (model_type INTEGER PRIMARY KEY, value BLOB);

-- TABLE: plus_address_sync_entity_metadata
CREATE TABLE plus_address_sync_entity_metadata (model_type INTEGER, storage_key VARCHAR, value BLOB, PRIMARY KEY (model_type, storage_key));

-- TABLE: token_service
CREATE TABLE token_service (service VARCHAR PRIMARY KEY NOT NULL,encrypted_token BLOB,binding_key BLOB);

-- TABLE: addresses
CREATE TABLE addresses (guid VARCHAR PRIMARY KEY, use_count INTEGER NOT NULL DEFAULT 0, use_date INTEGER NOT NULL DEFAULT 0, date_modified INTEGER NOT NULL DEFAULT 0, language_code VARCHAR, label VARCHAR, initial_creator_id INTEGER DEFAULT 0, last_modifier_id INTEGER DEFAULT 0, record_type INTEGER);

-- TABLE: address_type_tokens
CREATE TABLE address_type_tokens (guid VARCHAR, type INTEGER, value VARCHAR, verification_status INTEGER DEFAULT 0, observations BLOB, PRIMARY KEY (guid, type));

-- TABLE: autofill
CREATE TABLE autofill (name VARCHAR, value VARCHAR, value_lower VARCHAR, date_created INTEGER DEFAULT 0, date_last_used INTEGER DEFAULT 0, count INTEGER DEFAULT 1, PRIMARY KEY (name, value));

-- TABLE: autofill_sync_metadata
CREATE TABLE autofill_sync_metadata (model_type INTEGER NOT NULL, storage_key VARCHAR NOT NULL, value BLOB, PRIMARY KEY (model_type, storage_key));

-- TABLE: autofill_model_type_state
CREATE TABLE autofill_model_type_state (model_type INTEGER NOT NULL PRIMARY KEY, value BLOB);

-- TABLE: credit_cards
CREATE TABLE credit_cards (guid VARCHAR PRIMARY KEY, name_on_card VARCHAR, expiration_month INTEGER, expiration_year INTEGER, card_number_encrypted BLOB, date_modified INTEGER NOT NULL DEFAULT 0, origin VARCHAR DEFAULT '', use_count INTEGER NOT NULL DEFAULT 0, use_date INTEGER NOT NULL DEFAULT 0, billing_address_id VARCHAR, nickname VARCHAR);

-- TABLE: local_ibans
CREATE TABLE local_ibans (guid VARCHAR PRIMARY KEY, use_count INTEGER NOT NULL DEFAULT 0, use_date INTEGER NOT NULL DEFAULT 0, value_encrypted VARCHAR, nickname VARCHAR);

-- TABLE: masked_credit_cards
CREATE TABLE masked_credit_cards (id VARCHAR, name_on_card VARCHAR, network VARCHAR, last_four VARCHAR, exp_month INTEGER DEFAULT 0, exp_year INTEGER DEFAULT 0, bank_name VARCHAR, nickname VARCHAR, card_issuer INTEGER DEFAULT 0, instrument_id INTEGER DEFAULT 0, virtual_card_enrollment_state INTEGER DEFAULT 0, card_art_url VARCHAR, product_description VARCHAR, card_issuer_id VARCHAR, virtual_card_enrollment_type INTEGER DEFAULT 0, product_terms_url VARCHAR, card_info_retrieval_enrollment_state INTEGER DEFAULT 0, card_benefit_source INTEGER DEFAULT 0, card_creation_source INTEGER DEFAULT 0);

-- TABLE: server_card_metadata
CREATE TABLE server_card_metadata (id VARCHAR NOT NULL, use_count INTEGER NOT NULL DEFAULT 0, use_date INTEGER NOT NULL DEFAULT 0, billing_address_id VARCHAR);

-- TABLE: payments_customer_data
CREATE TABLE payments_customer_data (customer_id VARCHAR);

-- TABLE: server_card_cloud_token_data
CREATE TABLE server_card_cloud_token_data (id VARCHAR, suffix VARCHAR, exp_month INTEGER DEFAULT 0, exp_year INTEGER DEFAULT 0, card_art_url VARCHAR, instrument_token VARCHAR);

-- TABLE: offer_data
CREATE TABLE offer_data (offer_id UNSIGNED LONG, offer_reward_amount VARCHAR, expiry UNSIGNED LONG, offer_details_url VARCHAR, merchant_domain VARCHAR, promo_code VARCHAR, value_prop_text VARCHAR, see_details_text VARCHAR, usage_instructions_text VARCHAR);

-- TABLE: offer_eligible_instrument
CREATE TABLE offer_eligible_instrument (offer_id UNSIGNED LONG, instrument_id UNSIGNED LONG);

-- TABLE: offer_merchant_domain
CREATE TABLE offer_merchant_domain (offer_id UNSIGNED LONG, merchant_domain VARCHAR);

-- TABLE: virtual_card_usage_data
CREATE TABLE virtual_card_usage_data (id VARCHAR PRIMARY KEY, instrument_id INTEGER DEFAULT 0, merchant_domain VARCHAR, last_four VARCHAR);

-- TABLE: local_stored_cvc
CREATE TABLE local_stored_cvc (guid VARCHAR PRIMARY KEY NOT NULL, value_encrypted VARCHAR NOT NULL, last_updated_timestamp INTEGER NOT NULL);

-- TABLE: server_stored_cvc
CREATE TABLE server_stored_cvc (instrument_id INTEGER PRIMARY KEY NOT NULL, value_encrypted VARCHAR NOT NULL, last_updated_timestamp INTEGER NOT NULL);

-- TABLE: masked_bank_accounts
CREATE TABLE masked_bank_accounts (instrument_id INTEGER PRIMARY KEY NOT NULL, bank_name VARCHAR, account_number_suffix VARCHAR, account_type INTEGER DEFAULT 0, display_icon_url VARCHAR, nickname VARCHAR);

-- TABLE: masked_bank_accounts_metadata
CREATE TABLE masked_bank_accounts_metadata (instrument_id INTEGER NOT NULL, use_count INTEGER NOT NULL DEFAULT 0, use_date INTEGER NOT NULL DEFAULT 0);

-- TABLE: masked_ibans
CREATE TABLE masked_ibans (instrument_id VARCHAR PRIMARY KEY NOT NULL, prefix VARCHAR NOT NULL, suffix VARCHAR NOT NULL, nickname VARCHAR);

-- TABLE: masked_ibans_metadata
CREATE TABLE masked_ibans_metadata (instrument_id VARCHAR PRIMARY KEY NOT NULL, use_count INTEGER NOT NULL DEFAULT 0, use_date INTEGER NOT NULL DEFAULT 0);

-- TABLE: masked_credit_card_benefits
CREATE TABLE masked_credit_card_benefits (benefit_id VARCHAR PRIMARY KEY NOT NULL, instrument_id INTEGER NOT NULL DEFAULT 0, benefit_type INTEGER NOT NULL DEFAULT 0, benefit_category INTEGER NOT NULL DEFAULT 0, benefit_description VARCHAR NOT NULL, start_time INTEGER, end_time INTEGER);

-- TABLE: benefit_merchant_domains
CREATE TABLE benefit_merchant_domains (benefit_id VARCHAR NOT NULL, merchant_domain VARCHAR NOT NULL);

-- TABLE: generic_payment_instruments
CREATE TABLE generic_payment_instruments (instrument_id INTEGER PRIMARY KEY NOT NULL, serialized_value_encrypted VARCHAR NOT NULL);

-- TABLE: payment_instrument_creation_options
CREATE TABLE payment_instrument_creation_options (id VARCHAR PRIMARY KEY NOT NULL, serialized_value_encrypted VARCHAR NOT NULL);

-- TABLE: autofill_ai_attributes
CREATE TABLE autofill_ai_attributes (entity_guid TEXT NOT NULL, attribute_type TEXT NOT NULL, field_type INTEGER NOT NULL, value_encrypted BLOB NOT NULL, verification_status INTEGER NOT NULL, PRIMARY KEY (entity_guid, attribute_type, field_type));

-- TABLE: autofill_ai_entities
CREATE TABLE autofill_ai_entities (guid TEXT NOT NULL PRIMARY KEY, entity_type TEXT NOT NULL, nickname TEXT NOT NULL, record_type INTEGER DEFAULT 0, attributes_read_only INTEGER DEFAULT 0, frecency_override TEXT NOT NULL DEFAULT '');

-- TABLE: autofill_ai_entities_metadata
CREATE TABLE autofill_ai_entities_metadata (entity_guid TEXT NOT NULL PRIMARY KEY, use_count INTEGER DEFAULT 0, use_date INTEGER DEFAULT 0, date_modified INTEGER NOT NULL);

-- TABLE: keywords
CREATE TABLE keywords (id INTEGER PRIMARY KEY,short_name VARCHAR NOT NULL,keyword VARCHAR NOT NULL,favicon_url VARCHAR NOT NULL,url VARCHAR NOT NULL,safe_for_autoreplace INTEGER,originating_url VARCHAR,date_created INTEGER DEFAULT 0,usage_count INTEGER DEFAULT 0,input_encodings VARCHAR,suggest_url VARCHAR,prepopulate_id INTEGER DEFAULT 0,created_by_policy INTEGER DEFAULT 0,last_modified INTEGER DEFAULT 0,sync_guid VARCHAR,alternate_urls VARCHAR,image_url VARCHAR,search_url_post_params VARCHAR,suggest_url_post_params VARCHAR,image_url_post_params VARCHAR,new_tab_url VARCHAR,last_visited INTEGER DEFAULT 0, created_from_play_api INTEGER DEFAULT 0, is_active INTEGER DEFAULT 0, starter_pack_id INTEGER DEFAULT 0, enforced_by_policy INTEGER DEFAULT 0, featured_by_policy INTEGER DEFAULT 0, url_hash BLOB);

-- TABLE: web_app_manifest_section
CREATE TABLE web_app_manifest_section ( expire_date INTEGER NOT NULL DEFAULT 0, id VARCHAR, min_version INTEGER NOT NULL DEFAULT 0, fingerprints BLOB);

-- TABLE: payment_method_manifest
CREATE TABLE payment_method_manifest ( expire_date INTEGER NOT NULL DEFAULT 0, method_name VARCHAR, web_app_id VARCHAR);

-- TABLE: secure_payment_confirmation_instrument
CREATE TABLE secure_payment_confirmation_instrument ( credential_id BLOB NOT NULL PRIMARY KEY, relying_party_id VARCHAR NOT NULL, label VARCHAR NOT NULL, icon BLOB NOT NULL, date_created INTEGER NOT NULL DEFAULT 0, user_id BLOB);

-- TABLE: secure_payment_confirmation_browser_bound_key
CREATE TABLE secure_payment_confirmation_browser_bound_key ( credential_id BLOB NOT NULL, relying_party_id TEXT NOT NULL, browser_bound_key_id BLOB, last_used TIMESTAMP, PRIMARY KEY (credential_id, relying_party_id));

-- TABLE: loyalty_cards
CREATE TABLE loyalty_cards (loyalty_card_id TEXT PRIMARY KEY NOT NULL, merchant_name TEXT NOT NULL, program_name TEXT NOT NULL, program_logo TEXT NOT NULL, loyalty_card_number TEXT NOT NULL);

-- TABLE: loyalty_card_merchant_domain
CREATE TABLE loyalty_card_merchant_domain (loyalty_card_id VARCHAR, merchant_domain VARCHAR);

-- DATA: meta
INSERT INTO meta (key, value) VALUES ('mmap_status', '-1');
INSERT INTO meta (key, value) VALUES ('version', '147');
INSERT INTO meta (key, value) VALUES ('last_compatible_version', '147');
INSERT INTO meta (key, value) VALUES ('Builtin Keyword Version', '191');
INSERT INTO meta (key, value) VALUES ('Builtin Keyword Country', '21843');
INSERT INTO meta (key, value) VALUES ('Starter Pack Keyword Version', '13');

