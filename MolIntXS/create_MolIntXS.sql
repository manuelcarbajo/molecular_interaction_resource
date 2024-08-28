DROP DATABASE MolIntXS_11_Apr;
CREATE DATABASE IF NOT EXISTS MolIntXS_11_Apr;

use MolIntXS_11_Apr;

CREATE TABLE `interaction` (
	`interaction_id` INT NOT NULL AUTO_INCREMENT,
	`interactor_1` INT NOT NULL,
	`interactor_2` INT NOT NULL,
	`doi` VARCHAR(255) NOT NULL,
	`source_db_id` INT NOT NULL,
	`import_timestamp` TIMESTAMP NOT NULL,
	PRIMARY KEY (`interaction_id`),
	UNIQUE KEY `interaction_int1_int2_doi_db` (`interactor_1`,`interactor_2`,`doi`, `source_db_id`)
);

CREATE TABLE `predicted_interactor` (
	`predicted_interaction_id` INT NOT NULL AUTO_INCREMENT,
	`curated_interactor_id` INT NOT NULL,
	`interactor_type` ENUM('protein','gene','mRNA','synthetic') NOT NULL,
	`prediction_method_id` INT NOT NULL,
	`curies` VARCHAR(255),
	`name` VARCHAR(255) NOT NULL,
	`molecular_structure` VARCHAR(10000) ,
	`predicted_timestamp` TIMESTAMP NOT NULL,
	`ensembl_gene_id` INT NOT NULL,
	PRIMARY KEY (`predicted_interaction_id`)
);

CREATE TABLE `ensembl_gene` (
	`ensembl_gene_id` INT NOT NULL AUTO_INCREMENT,
	`species_id` INT,
	`ensembl_stable_id` VARCHAR(255),
	`import_timestamp` TIMESTAMP NOT NULL,
	PRIMARY KEY (`ensembl_gene_id`)
);

CREATE TABLE `curated_interactor` (
	`curated_interactor_id` INT NOT NULL AUTO_INCREMENT,
	`interactor_type` ENUM('protein','gene','mRNA','synthetic') NOT NULL,
	`curies` VARCHAR(255) UNIQUE,
	`name` VARCHAR(255),
	`molecular_structure` VARCHAR(10000) ,
	`import_timestamp` TIMESTAMP NOT NULL,
	`ensembl_gene_id` INT,
	PRIMARY KEY (`curated_interactor_id`)
);

CREATE TABLE `species` (
	`species_id` INT NOT NULL AUTO_INCREMENT,
	`ensembl_division` varchar(255) NOT NULL,
	`production_name` varchar(255) NOT NULL,
	`taxon_id` INT NOT NULL UNIQUE,
	PRIMARY KEY (`species_id`)
);

CREATE TABLE `key_value_pair` (
	`key_value_id` INT NOT NULL AUTO_INCREMENT,
    `interaction_id` INT NOT NULL,
	`meta_key_id` INT NOT NULL,
	`value` varchar(255) NOT NULL,
	`ontology_term_id` INT,
	PRIMARY KEY (`key_value_id`),
    UNIQUE KEY `key_value_pair_interaction_metakey_val` (`interaction_id`,`meta_key_id`,`value`)
);

CREATE TABLE `ontology` (
	`ontology_id` INT NOT NULL AUTO_INCREMENT,
	`name` VARCHAR(255) NOT NULL UNIQUE,
	`description` varchar(255) NOT NULL UNIQUE,
	PRIMARY KEY (`ontology_id`)
);

CREATE TABLE `source_db` (
	`source_db_id` INT NOT NULL AUTO_INCREMENT,
	`label` varchar(255) NOT NULL UNIQUE,
	`external_db` VARCHAR(255) NOT NULL,
	PRIMARY KEY (`source_db_id`)
);

CREATE TABLE `meta_key` (
	`meta_key_id` INT NOT NULL AUTO_INCREMENT,
	`name` VARCHAR(255) NOT NULL UNIQUE,
	`description` VARCHAR(255) NOT NULL UNIQUE,
	PRIMARY KEY (`meta_key_id`)
);

CREATE TABLE `prediction_method` (
	`prediction_method_id` INT NOT NULL AUTO_INCREMENT,
	`name` VARCHAR(255) NOT NULL,
	`parameters` VARCHAR(255) NOT NULL,
	PRIMARY KEY (`prediction_method_id`)
);

CREATE TABLE `ontology_term` (
	`ontology_term_id` INT NOT NULL AUTO_INCREMENT,
	`ontology_id` INT NOT NULL,
	`accession` VARCHAR(255) NOT NULL UNIQUE,
	`description` VARCHAR(255) NOT NULL UNIQUE,
	PRIMARY KEY (`ontology_term_id`)
);

ALTER TABLE `interaction` ADD CONSTRAINT `interaction_fk0` FOREIGN KEY (`interactor_1`) REFERENCES `curated_interactor`(`curated_interactor_id`);

ALTER TABLE `interaction` ADD CONSTRAINT `interaction_fk1` FOREIGN KEY (`interactor_2`) REFERENCES `curated_interactor`(`curated_interactor_id`);

ALTER TABLE `interaction` ADD CONSTRAINT `interaction_fk2` FOREIGN KEY (`source_db_id`) REFERENCES `source_db`(`source_db_id`);

ALTER TABLE `predicted_interactor` ADD CONSTRAINT `predicted_interactor_fk0` FOREIGN KEY (`curated_interactor_id`) REFERENCES `curated_interactor`(`curated_interactor_id`);

ALTER TABLE `predicted_interactor` ADD CONSTRAINT `predicted_interactor_fk1` FOREIGN KEY (`prediction_method_id`) REFERENCES `prediction_method`(`prediction_method_id`);

ALTER TABLE `predicted_interactor` ADD CONSTRAINT `predicted_interactor_fk2` FOREIGN KEY (`ensembl_gene_id`) REFERENCES `ensembl_gene`(`ensembl_gene_id`);

ALTER TABLE `ensembl_gene` ADD CONSTRAINT `ensembl_gene_fk0` FOREIGN KEY (`species_id`) REFERENCES `species`(`species_id`);

ALTER TABLE `curated_interactor` ADD CONSTRAINT `curated_interactor_fk0` FOREIGN KEY (`ensembl_gene_id`) REFERENCES `ensembl_gene`(`ensembl_gene_id`);

ALTER TABLE `key_value_pair` ADD CONSTRAINT `key_value_pair_fk0` FOREIGN KEY (`interaction_id`) REFERENCES `interaction`(`interaction_id`);

ALTER TABLE `key_value_pair` ADD CONSTRAINT `key_value_pair_fk1` FOREIGN KEY (`meta_key_id`) REFERENCES `meta_key`(`meta_key_id`);

ALTER TABLE `key_value_pair` ADD CONSTRAINT `key_value_pair_fk2` FOREIGN KEY (`ontology_term_id`) REFERENCES `ontology_term`(`ontology_term_id`);

ALTER TABLE `ontology_term` ADD CONSTRAINT `ontology_term_fk0` FOREIGN KEY (`ontology_id`) REFERENCES `ontology`(`ontology_id`);
