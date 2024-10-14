CREATE DATABASE `db_banco_py`;

USE `db_banco_py`;

CREATE TABLE `tb_carros` (
	`id` int primary key not null auto_increment,
    `marca` varchar(100) not null,
    `modelo` varchar(100) not null,
    `ano` int not null
);

INSERT INTO `tb_carros` VALUES 
(1, 'Fiat', 'Marea', 1999), 
(2, 'Fiat', 'Uno', 1992), 
(3, 'Ford', 'Escort', 1985), 
(4, 'Chevrolet', 'Chevette', 1978), 
(5, 'Volkswagen', 'Fusca', 1962);

SELECT * FROM `tb_carros`; 