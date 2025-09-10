-- Merged initial creation script (Turnero + Usuarios/Roles) 
-- MySQL Workbench Forward Engineering (adaptado)
SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema Turnero
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `Turnero` DEFAULT CHARACTER SET utf8mb4;
USE `Turnero` ;

-- -----------------------------------------------------
-- Table `Turnero`.`Rol`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Turnero`.`Rol` (
  `id_rol` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(50) NOT NULL UNIQUE,
  PRIMARY KEY (`id_rol`)
) ENGINE=InnoDB;

-- -----------------------------------------------------
-- Table `Turnero`.`Usuario`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Turnero`.`Usuario` (
  `id_usuario` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(50) NOT NULL UNIQUE,
  `email` VARCHAR(120) UNIQUE,
  `password_hash` VARCHAR(255) NOT NULL,
  `dni` BIGINT NULL,
  `id_rol` INT NOT NULL,
  `creado_en` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_usuario`),
  CONSTRAINT `fk_usuario_rol`
    FOREIGN KEY (`id_rol`) REFERENCES `Turnero`.`Rol`(`id_rol`)
    ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;

-- -----------------------------------------------------
-- Table `Turnero`.`Acceso`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Turnero`.`Acceso` (
  `id_acceso` BIGINT NOT NULL AUTO_INCREMENT,
  `usuario_id` INT NOT NULL,
  `ingreso` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_acceso`),
  CONSTRAINT `fk_acceso_usuario`
    FOREIGN KEY (`usuario_id`) REFERENCES `Turnero`.`Usuario`(`id_usuario`)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

-- -----------------------------------------------------
-- Table `Turnero`.`Paciente`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Turnero`.`Paciente` (
  `id_paciente` INT NOT NULL AUTO_INCREMENT,
  `Nombre` VARCHAR(45) NOT NULL,
  `Apellido` VARCHAR(45) NOT NULL,
  `DNI` INT NOT NULL,
  `usuario_id` INT NULL,
  PRIMARY KEY (`id_paciente`),
  UNIQUE INDEX `id_paciente_UNIQUE` (`id_paciente` ASC) VISIBLE,
  UNIQUE INDEX `uq_paciente_usuario` (`usuario_id` ASC) VISIBLE,
  CONSTRAINT `fk_paciente_usuario`
    FOREIGN KEY (`usuario_id`) REFERENCES `Turnero`.`Usuario`(`id_usuario`)
    ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB;

-- -----------------------------------------------------
-- Table `Turnero`.`Departamento`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Turnero`.`Departamento` (
  `id_departamento` INT NOT NULL AUTO_INCREMENT,
  `Nombre` VARCHAR(45) NULL,
  PRIMARY KEY (`id_departamento`)
) ENGINE=InnoDB;

-- -----------------------------------------------------
-- Table `Turnero`.`Especialidad`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Turnero`.`Especialidad` (
  `id_especialidad` INT NOT NULL AUTO_INCREMENT,
  `Nombre` VARCHAR(45) NULL,
  `Departamento_id_departamento` INT NOT NULL,
  PRIMARY KEY (`id_especialidad`, `Departamento_id_departamento`),
  INDEX `fk_Especialidad_Departamento1_idx` (`Departamento_id_departamento` ASC) VISIBLE,
  CONSTRAINT `fk_Especialidad_Departamento1`
    FOREIGN KEY (`Departamento_id_departamento`)
    REFERENCES `Turnero`.`Departamento` (`id_departamento`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE=InnoDB;

-- -----------------------------------------------------
-- Table `Turnero`.`Horario`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Turnero`.`Horario` (
  `id_Horario` INT NOT NULL AUTO_INCREMENT,
  `hora_inicio` INT NOT NULL,
  `hora_fin` INT NOT NULL,
  PRIMARY KEY (`id_Horario`)
) ENGINE=InnoDB;

-- -----------------------------------------------------
-- Table `Turnero`.`Medico`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Turnero`.`Medico` (
  `id_medico` INT NOT NULL AUTO_INCREMENT,
  `Nombre` VARCHAR(45) NULL,
  `Apellido` VARCHAR(45) NULL,
  `Horario_id_Horario` INT NOT NULL,
  `usuario_id` INT NULL,
  PRIMARY KEY (`id_medico`, `Horario_id_Horario`),
  INDEX `fk_Medico_Horario1_idx` (`Horario_id_Horario` ASC) VISIBLE,
  UNIQUE INDEX `uq_medico_usuario` (`usuario_id` ASC) VISIBLE,
  CONSTRAINT `fk_Medico_Horario1`
    FOREIGN KEY (`Horario_id_Horario`)
    REFERENCES `Turnero`.`Horario` (`id_Horario`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_medico_usuario`
    FOREIGN KEY (`usuario_id`) REFERENCES `Turnero`.`Usuario`(`id_usuario`)
    ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB;

-- -----------------------------------------------------
-- Table `Turnero`.`Medico_has_Especialidad`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Turnero`.`Medico_has_Especialidad` (
  `Medico_id_medico` INT NOT NULL,
  `Especialidad_id_especialidad` INT NOT NULL,
  PRIMARY KEY (`Medico_id_medico`, `Especialidad_id_especialidad`),
  INDEX `fk_Medico_has_Especialidad_Especialidad1_idx` (`Especialidad_id_especialidad` ASC) VISIBLE,
  INDEX `fk_Medico_has_Especialidad_Medico1_idx` (`Medico_id_medico` ASC) VISIBLE,
  CONSTRAINT `fk_Medico_has_Especialidad_Medico1`
    FOREIGN KEY (`Medico_id_medico`)
    REFERENCES `Turnero`.`Medico` (`id_medico`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Medico_has_Especialidad_Especialidad1`
    FOREIGN KEY (`Especialidad_id_especialidad`)
    REFERENCES `Turnero`.`Especialidad` (`id_especialidad`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE=InnoDB;

-- -----------------------------------------------------
-- Table `Turnero`.`Turno`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Turnero`.`Turno` (
  `id_turno` INT NOT NULL AUTO_INCREMENT,
  `fecha` DATE NOT NULL,
  `hora` TIME NOT NULL,
  `Paciente_id_paciente` INT NOT NULL,
  `Especialidad_id_especialidad` INT NOT NULL,
  PRIMARY KEY (`id_turno`),
  INDEX `fk_Turno_Paciente1_idx` (`Paciente_id_paciente` ASC) VISIBLE,
  INDEX `fk_Turno_Especialidad1_idx` (`Especialidad_id_especialidad` ASC) VISIBLE,
  CONSTRAINT `fk_Turno_Paciente1`
    FOREIGN KEY (`Paciente_id_paciente`)
    REFERENCES `Turnero`.`Paciente` (`id_paciente`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Turno_Especialidad1`
    FOREIGN KEY (`Especialidad_id_especialidad`)
    REFERENCES `Turnero`.`Especialidad` (`id_especialidad`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE=InnoDB;

-- MySQL Workbench Rewind Engineering
SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
