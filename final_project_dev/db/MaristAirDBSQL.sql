-- MySQL Script generated by MySQL Workbench
-- Wed 29 Nov 2017 11:22:18 AM EST
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema MaristAir
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema MaristAir
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `MaristAir` DEFAULT CHARACTER SET utf8 ;
USE `MaristAir` ;

-- -----------------------------------------------------
-- Table `MaristAir`.`Airline`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `MaristAir`.`Airline` (
  `airline_id` INT NOT NULL AUTO_INCREMENT,
  `airline_name` VARCHAR(120) NOT NULL,
  `airline_addr` VARCHAR(120) NULL,
  `airline_phone` VARCHAR(16) NOT NULL,
  `airline_email` VARCHAR(120) NULL,
  PRIMARY KEY (`airline_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `MaristAir`.`User`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `MaristAir`.`User` (
  `user_id` INT NOT NULL AUTO_INCREMENT,
  `user_email` VARCHAR(120) NOT NULL,
  `user_password` VARCHAR(60) NOT NULL,
  `user_phone` VARCHAR(16) NULL,
  `user_createdate` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`));


-- -----------------------------------------------------
-- Table `MaristAir`.`Options`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `MaristAir`.`Options` (
  `option_id` INT NOT NULL AUTO_INCREMENT,
  `option_name` VARCHAR(60) NOT NULL,
  `option_price` FLOAT NOT NULL,
  PRIMARY KEY (`option_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `MaristAir`.`City`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `MaristAir`.`City` (
  `city_id` INT NOT NULL AUTO_INCREMENT,
  `city_name` VARCHAR(120) NOT NULL,
  `city_state` VARCHAR(120) NOT NULL,
  `city_lat` FLOAT NOT NULL,
  `city_long` FLOAT NOT NULL,
  PRIMARY KEY (`city_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `MaristAir`.`Plane`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `MaristAir`.`Plane` (
  `plane_id` INT NOT NULL AUTO_INCREMENT,
  `airline_id` INT NOT NULL,
  `plane_model` VARCHAR(60) NOT NULL,
  `plane_seats` INT NOT NULL,
  PRIMARY KEY (`plane_id`),
  INDEX `fk_airline_id_idx` (`airline_id` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `MaristAir`.`Flight`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `MaristAir`.`Flight` (
  `flight_id` INT NOT NULL AUTO_INCREMENT,
  `flight_source_city` INT NOT NULL,
  `flight_source_gate` VARCHAR(45) NULL,
  `flight_dest_city` INT NOT NULL,
  `flight_dest_gate` VARCHAR(45) NULL,
  `flight_rem_seats` INT NULL,
  `flight_depart` DATETIME NOT NULL,
  `flight_arrive` DATETIME NOT NULL,
  `flight_base_price` FLOAT NULL,
  `plane_id` INT NOT NULL,
  PRIMARY KEY (`flight_id`),
  INDEX `fk_flight_source_idx` (`flight_source_city` ASC),
  INDEX `fk_flight_dest_idx` (`flight_dest_city` ASC),
  INDEX `fk_plane_id_idx` (`plane_id` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `MaristAir`.`Billing`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `MaristAir`.`Billing` (
  `billing_id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `billing_card_num` DECIMAL(16,0) NOT NULL,
  `billing_card_expr` DATE NOT NULL,
  `billing_card_csv` DECIMAL(4,0) NOT NULL,
  `billing_firstname` VARCHAR(120) NOT NULL,
  `billing_lastname` VARCHAR(120) NOT NULL,
  `billing_address` VARCHAR(120) NOT NULL,
  `billing_city` VARCHAR(60) NOT NULL,
  `billing_state` VARCHAR(60) NOT NULL,
  `billing_zip` DECIMAL(5,0) NOT NULL,
  `billing_timestamp` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`billing_id`),
  INDEX `fk_user_id_idx` (`user_id` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `MaristAir`.`Reservation`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `MaristAir`.`Reservation` (
  `reservation_id` INT NOT NULL AUTO_INCREMENT,
  `flight_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  `billing_id` INT NOT NULL,
  `timestamp` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  `reservation_seat` VARCHAR(10) NULL,
  `reservation_total` FLOAT NULL,
  PRIMARY KEY (`reservation_id`),
  INDEX `fk_user_id_idx` (`user_id` ASC),
  INDEX `fk_flight_id_idx` (`flight_id` ASC),
  INDEX `fk_billing_id_idx` (`billing_id` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `MaristAir`.`Option_List`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `MaristAir`.`Option_List` (
  `reservation_id` INT NOT NULL,
  `option_id` INT NOT NULL,
  PRIMARY KEY (`reservation_id`, `option_id`),
  INDEX `fk_option_id_idx` (`option_id` ASC))
ENGINE = InnoDB;





CREATE USER 'readuser' IDENTIFIED BY 'readuser1';
GRANT SELECT ON TABLE `MaristAir`.* TO 'readuser';


CREATE USER 'insertuser' IDENTIFIED BY 'insertuser1';
GRANT SELECT, UPDATE, INSERT, TRIGGER ON TABLE `MaristAir`.* TO 'insertuser';

-- Comment out create admin user since created by AWS already --
-- CREATE USER 'admin' IDENTIFIED BY 'admin1';
-- GRANT ALL ON `MaristAir`.* TO 'admin';
-- GRANT SELECT, INSERT, TRIGGER, UPDATE, DELETE ON TABLE `MaristAir`.* TO 'admin';
-- GRANT EXECUTE ON ROUTINE `MaristAir`.* TO 'admin';
-- GRANT SELECT ON TABLE `MaristAir`.* TO 'admin';
-- 





SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
