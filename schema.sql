-- Comments App Database Schema
-- Compatible with MySQL Workbench

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema comments_db
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `comments_db` DEFAULT CHARACTER SET utf8mb4;
USE `comments_db`;

-- -----------------------------------------------------
-- Table `comments_db`.`comments_comment`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `comments_db`.`comments_comment` (
  `id`         BIGINT        NOT NULL AUTO_INCREMENT,
  `username`   VARCHAR(100)  NOT NULL COMMENT 'Letters and digits only',
  `email`      VARCHAR(254)  NOT NULL COMMENT 'Valid email format',
  `homepage`   VARCHAR(200)  NOT NULL DEFAULT '' COMMENT 'Optional URL',
  `text`       LONGTEXT      NOT NULL COMMENT 'Sanitized HTML (bleach)',
  `created_at` DATETIME(6)   NOT NULL COMMENT 'Auto timestamp',
  `image`      VARCHAR(100)  NULL DEFAULT NULL COMMENT 'Path: images/, max 320x240px',
  `text_file`  VARCHAR(100)  NULL DEFAULT NULL COMMENT 'Path: txt/, max 100KB',
  `parent_id`  BIGINT        NULL DEFAULT NULL COMMENT 'Self-reference for nested replies',

  PRIMARY KEY (`id`),
  INDEX `comments_comment_parent_id_idx` (`parent_id` ASC),

  CONSTRAINT `fk_comments_comment_parent`
    FOREIGN KEY (`parent_id`)
    REFERENCES `comments_db`.`comments_comment` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COMMENT='Main comments table with self-referencing nested replies';

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
