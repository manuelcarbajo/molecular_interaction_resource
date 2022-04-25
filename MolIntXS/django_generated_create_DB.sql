--
-- Create model CuratedInteractor
--
CREATE TABLE `curated_interactor` (`curated_interactor_id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY
 `interactor_type` varchar(9) NOT NULL
 `curies` varchar(255) NULL UNIQUE
 `name` varchar(255) NULL
 `molecular_structure` varchar(10000) NULL
 `import_timestamp` datetime(6) NOT NULL);
--
-- Create model EnsemblGene
--
CREATE TABLE `ensembl_gene` (`ensembl_gene_id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY
 `ensembl_stable_id` varchar(255) NULL
 `import_timestamp` datetime(6) NOT NULL);
--
-- Create model MetaKey
--
CREATE TABLE `meta_key` (`meta_key_id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY
 `name` varchar(255) NOT NULL UNIQUE
  `description` varchar(255) NOT NULL UNIQUE);
--
-- Create model Ontology
--
CREATE TABLE `ontology` (`ontology_id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `name` varchar(255) NOT NULL UNIQUE, `description` varchar(255) NOT NULL UNIQUE);
--
-- Create model PredictionMethod
--
CREATE TABLE `prediction_method` (`prediction_method_id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `name` varchar(255) NOT NULL, `parameters` varchar(255) NOT NULL);
--
-- Create model SourceDb
--
CREATE TABLE `source_db` (`source_db_id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `label` varchar(255) NOT NULL, `external_db` varchar(255) NOT NULL);
--
-- Create model Species
--
CREATE TABLE `species` (`species_id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `ensembl_division` varchar(255) NOT NULL, `production_name` varchar(255) NOT NULL, `taxon_id` integer NOT NULL UNIQUE);
--
-- Create model PredictedInteractor
--
CREATE TABLE `predicted_interactor` (`predicted_interaction_id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `interactor_type` varchar(9) NOT NULL, `curies` varchar(255) NULL, `name` varchar(255) NOT NULL, `molecular_structure` varchar(10000) NULL, `predicted_timestamp` datetime(6) NOT NULL, `curated_interactor_id` integer NOT NULL, `ensembl_gene_id` integer NOT NULL, `prediction_method_id` integer NOT NULL);
--
-- Create model OntologyTerm
--
CREATE TABLE `ontology_term` (`ontology_term_id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `accession` varchar(255) NOT NULL UNIQUE, `description` varchar(255) NOT NULL UNIQUE, `ontology_id` integer NOT NULL);
--
-- Create model Interaction
--
CREATE TABLE `interaction` (`interaction_id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `doi` varchar(255) NOT NULL, `import_timestamp` datetime(6) NOT NULL, `interactor_1` integer NOT NULL, `interactor_2` integer NOT NULL, `source_db_id` integer NOT NULL);
--
-- Add field species to ensemblgene
--
ALTER TABLE `ensembl_gene` ADD COLUMN `species_id` integer NOT NULL , ADD CONSTRAINT `ensembl_gene_species_id_ed965144_fk_species_species_id` FOREIGN KEY (`species_id`) REFERENCES `species`(`species_id`);
--
-- Add field ensembl_gene to curatedinteractor
--
ALTER TABLE `curated_interactor` ADD COLUMN `ensembl_gene_id` integer NOT NULL , ADD CONSTRAINT `curated_interactor_ensembl_gene_id_759a37da_fk_ensembl_g` FOREIGN KEY (`ensembl_gene_id`) REFERENCES `ensembl_gene`(`ensembl_gene_id`);
--
-- Create model KeyValuePair
--
CREATE TABLE `key_value_pair` (`key_value_id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `value` varchar(255) NOT NULL, `interaction_id` integer NOT NULL, `meta_key_id` integer NOT NULL, `ontology_term_id` integer NULL);
ALTER TABLE `predicted_interactor` ADD CONSTRAINT `predicted_interactor_curated_interactor_i_b9789e31_fk_curated_i` FOREIGN KEY (`curated_interactor_id`) REFERENCES `curated_interactor` (`curated_interactor_id`);
ALTER TABLE `predicted_interactor` ADD CONSTRAINT `predicted_interactor_ensembl_gene_id_765b4167_fk_ensembl_g` FOREIGN KEY (`ensembl_gene_id`) REFERENCES `ensembl_gene` (`ensembl_gene_id`);
ALTER TABLE `predicted_interactor` ADD CONSTRAINT `predicted_interactor_prediction_method_id_93bdc71b_fk_predictio` FOREIGN KEY (`prediction_method_id`) REFERENCES `prediction_method` (`prediction_method_id`);
ALTER TABLE `ontology_term` ADD CONSTRAINT `ontology_term_ontology_id_e94b28e5_fk_ontology_ontology_id` FOREIGN KEY (`ontology_id`) REFERENCES `ontology` (`ontology_id`);
ALTER TABLE `interaction` ADD CONSTRAINT `interaction_interactor_1_interactor__e0795315_uniq` UNIQUE (`interactor_1`, `interactor_2`, `doi`, `source_db_id`);
ALTER TABLE `interaction` ADD CONSTRAINT `interaction_interactor_1_9d2cb0dc_fk_curated_i` FOREIGN KEY (`interactor_1`) REFERENCES `curated_interactor` (`curated_interactor_id`);
ALTER TABLE `interaction` ADD CONSTRAINT `interaction_interactor_2_138b703d_fk_curated_i` FOREIGN KEY (`interactor_2`) REFERENCES `curated_interactor` (`curated_interactor_id`);
ALTER TABLE `interaction` ADD CONSTRAINT `interaction_source_db_id_99a6e45e_fk_source_db_source_db_id` FOREIGN KEY (`source_db_id`) REFERENCES `source_db` (`source_db_id`);
ALTER TABLE `key_value_pair` ADD CONSTRAINT `key_value_pair_interaction_id_meta_key_id_value_1aafcb32_uniq` UNIQUE (`interaction_id`, `meta_key_id`, `value`);
ALTER TABLE `key_value_pair` ADD CONSTRAINT `key_value_pair_interaction_id_12148642_fk_interacti` FOREIGN KEY (`interaction_id`) REFERENCES `interaction` (`interaction_id`);
ALTER TABLE `key_value_pair` ADD CONSTRAINT `key_value_pair_meta_key_id_8d016413_fk_meta_key_meta_key_id` FOREIGN KEY (`meta_key_id`) REFERENCES `meta_key` (`meta_key_id`);
ALTER TABLE `key_value_pair` ADD CONSTRAINT `key_value_pair_ontology_term_id_f2fb4cf1_fk_ontology_` FOREIGN KEY (`ontology_term_id`) REFERENCES `ontology_term` (`ontology_term_id`);
