DROP DATABASE IF EXISTS `atm`;
CREATE DATABASE `atm`; 

USE atm;

CREATE TABLE `nasabah` (
  `id_nasabah` int(11) NOT NULL AUTO_INCREMENT,
  `no_rek` int(7) NOT NULL,
  `nama` varchar(50) NOT NULL,
  `no_telpon` varchar(20) DEFAULT NULL,
  `tgl_registrasi` timestamp DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_nasabah`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
INSERT INTO `nasabah` VALUES (1,'13200001','Admin',NULL, DEFAULT);
INSERT INTO `nasabah` VALUES (2,'13216072','Khudzaifah bin Zahid','0812-1111-1111',DEFAULT);
INSERT INTO `nasabah` VALUES (3,'13216073','Muhammad Rifqi Ariq','0812-2222-2222',DEFAULT);
INSERT INTO `nasabah` VALUES (4,'13216079','Arba Robbani','0812-3333-3333',DEFAULT);

CREATE TABLE `auth` (
  `id_nasabah` int(11) NOT NULL AUTO_INCREMENT,
  `magic_code` char(60) UNIQUE NOT NULL,
  PRIMARY KEY (`id_nasabah`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
INSERT INTO `auth` VALUES (1, '$2b$12$O4GGyQXRald97MZwuhurL.c4KLMyZfW2kPxtog8XAi5e8p326NXJy');
INSERT INTO `auth` VALUES (2, '$2b$12$O4GGyQXRald97MZwuhurL.vuTHfK8ULSoK.FX8EFtmtipWUB56jgy');
INSERT INTO `auth` VALUES (3, '$2b$12$O4GGyQXRald97MZwuhurL.p67nmJB7XiFfxAp2ObkK5.kGu7amdsO');
INSERT INTO `auth` VALUES (4, '$2b$12$O4GGyQXRald97MZwuhurL.VhfQ5/yrqlhlHWv6Wftyo/B3Gbi5JzG');

CREATE TABLE `saldo` (
  `id_nasabah` int(11) NOT NULL,
  `saldo` dec(15,2) NOT NULL DEFAULT '0.00',
  `last_change` timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_nasabah`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
INSERT INTO `saldo` VALUES (1, DEFAULT, DEFAULT);
INSERT INTO `saldo` VALUES (2, 5000000, DEFAULT);
INSERT INTO `saldo` VALUES (3, 5000000, DEFAULT);
INSERT INTO `saldo` VALUES (4, 5000000, DEFAULT);

CREATE TABLE `histori_transaksi` (
  `no_transaksi` int(11) NOT NULL AUTO_INCREMENT,
  `id_nasabah` int(11) NOT NULL,
  `timestamp` timestamp DEFAULT CURRENT_TIMESTAMP,
  `kode_transaksi` int(11) NOT NULL,
  `rek_asal_atau_tujuan` int (11) DEFAULT NULL,
  `jumlah_transaksi` dec(15,2) NOT NULL,
  PRIMARY KEY (`no_transaksi`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
INSERT INTO `histori_transaksi` VALUES (1, 1, DEFAULT, 1, DEFAULT, 0);
INSERT INTO `histori_transaksi` VALUES (2, 2, DEFAULT, 1, DEFAULT, 5000000);
INSERT INTO `histori_transaksi` VALUES (3, 3, DEFAULT, 1, DEFAULT, 5000000);
INSERT INTO `histori_transaksi` VALUES (4, 4, DEFAULT, 1, DEFAULT, 5000000);

CREATE TABLE `list_kode_transaksi` (
  `kode_transaksi` int(11) NOT NULL,
  `nama` varchar(50) NOT NULL,
  PRIMARY KEY (`kode_transaksi`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
INSERT INTO `list_kode_transaksi` VALUES (1, 'ISI SALDO');
INSERT INTO `list_kode_transaksi` VALUES (2, 'TRANSFER KELUAR');
INSERT INTO `list_kode_transaksi` VALUES (3, 'TRANSFER MASUK');

CREATE TABLE `server` (
  `id_server` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(60) NOT NULL,
  PRIMARY KEY (`kode_transaksi`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
INSERT INTO `auth` VALUES ('arba', '$2b$12$O4GGyQXRald97MZwuhurL.AOlkzbs9NrSbgzZumJs8qUOFtG1rYW2');