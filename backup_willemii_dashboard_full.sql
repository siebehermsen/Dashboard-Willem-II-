-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: willemii_dashboard
-- ------------------------------------------------------
-- Server version	8.0.44

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `willemii_dashboard`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `willemii_dashboard` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `willemii_dashboard`;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=201 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add player',7,'add_player'),(26,'Can change player',7,'change_player'),(27,'Can delete player',7,'delete_player'),(28,'Can view player',7,'view_player'),(29,'Can add Dagprogramma',8,'add_dayprogram'),(30,'Can change Dagprogramma',8,'change_dayprogram'),(31,'Can delete Dagprogramma',8,'delete_dayprogram'),(32,'Can view Dagprogramma',8,'view_dayprogram'),(33,'Can add Blessure',9,'add_injury'),(34,'Can change Blessure',9,'change_injury'),(35,'Can delete Blessure',9,'delete_injury'),(36,'Can view Blessure',9,'view_injury'),(37,'Can add Testresultaat',10,'add_playertest'),(38,'Can change Testresultaat',10,'change_playertest'),(39,'Can delete Testresultaat',10,'delete_playertest'),(40,'Can view Testresultaat',10,'view_playertest'),(41,'Can add Trainingsdata',11,'add_trainingdata'),(42,'Can change Trainingsdata',11,'change_trainingdata'),(43,'Can delete Trainingsdata',11,'delete_trainingdata'),(44,'Can view Trainingsdata',11,'view_trainingdata'),(45,'Can add Oefening',12,'add_oefening'),(46,'Can change Oefening',12,'change_oefening'),(47,'Can delete Oefening',12,'delete_oefening'),(48,'Can view Oefening',12,'view_oefening'),(49,'Can add Wellnessinvoer',13,'add_wellnessentry'),(50,'Can change Wellnessinvoer',13,'change_wellnessentry'),(51,'Can delete Wellnessinvoer',13,'delete_wellnessentry'),(52,'Can view Wellnessinvoer',13,'view_wellnessentry'),(53,'Can add Veldrevalidatie sessie',14,'add_fieldrehabsession'),(54,'Can change Veldrevalidatie sessie',14,'change_fieldrehabsession'),(55,'Can delete Veldrevalidatie sessie',14,'delete_fieldrehabsession'),(56,'Can view Veldrevalidatie sessie',14,'view_fieldrehabsession'),(57,'Can add Individueel Programma',15,'add_programma'),(58,'Can change Individueel Programma',15,'change_programma'),(59,'Can delete Individueel Programma',15,'delete_programma'),(60,'Can view Individueel Programma',15,'view_programma'),(61,'Can add Programma Oefening',16,'add_programmaoefening'),(62,'Can change Programma Oefening',16,'change_programmaoefening'),(63,'Can delete Programma Oefening',16,'delete_programmaoefening'),(64,'Can view Programma Oefening',16,'view_programmaoefening'),(65,'Can add RPE Invoer',17,'add_rpeentry'),(66,'Can change RPE Invoer',17,'change_rpeentry'),(67,'Can delete RPE Invoer',17,'delete_rpeentry'),(68,'Can view RPE Invoer',17,'view_rpeentry'),(69,'Can add pop gesprek',18,'add_popgesprek'),(70,'Can change pop gesprek',18,'change_popgesprek'),(71,'Can delete pop gesprek',18,'delete_popgesprek'),(72,'Can view pop gesprek',18,'view_popgesprek'),(73,'Can add Dagprogramma',19,'add_dailyprogram'),(74,'Can change Dagprogramma',19,'change_dailyprogram'),(75,'Can delete Dagprogramma',19,'delete_dailyprogram'),(76,'Can view Dagprogramma',19,'view_dailyprogram'),(77,'Can add attendance',20,'add_attendance'),(78,'Can change attendance',20,'change_attendance'),(79,'Can delete attendance',20,'delete_attendance'),(80,'Can view attendance',20,'view_attendance'),(81,'Can add Aanwezigheid',21,'add_aanwezigheid'),(82,'Can change Aanwezigheid',21,'change_aanwezigheid'),(83,'Can delete Aanwezigheid',21,'delete_aanwezigheid'),(84,'Can view Aanwezigheid',21,'view_aanwezigheid'),(85,'Can add overig',22,'add_overig'),(86,'Can change overig',22,'change_overig'),(87,'Can delete overig',22,'delete_overig'),(88,'Can view overig',22,'view_overig'),(89,'Can add Staflid',23,'add_staff'),(90,'Can change Staflid',23,'change_staff'),(91,'Can delete Staflid',23,'delete_staff'),(92,'Can view Staflid',23,'view_staff'),(93,'Can add Wedstrijddata',24,'add_wedstrijddata'),(94,'Can change Wedstrijddata',24,'change_wedstrijddata'),(95,'Can delete Wedstrijddata',24,'delete_wedstrijddata'),(96,'Can view Wedstrijddata',24,'view_wedstrijddata'),(97,'Can add hit week planning',25,'add_hitweekplanning'),(98,'Can change hit week planning',25,'change_hitweekplanning'),(99,'Can delete hit week planning',25,'delete_hitweekplanning'),(100,'Can view hit week planning',25,'view_hitweekplanning'),(101,'Can add nutrition day',26,'add_nutritionday'),(102,'Can change nutrition day',26,'change_nutritionday'),(103,'Can delete nutrition day',26,'delete_nutritionday'),(104,'Can view nutrition day',26,'view_nutritionday'),(105,'Can add antropometry',27,'add_antropometry'),(106,'Can change antropometry',27,'change_antropometry'),(107,'Can delete antropometry',27,'delete_antropometry'),(108,'Can view antropometry',27,'view_antropometry'),(109,'Can add match',28,'add_match'),(110,'Can change match',28,'change_match'),(111,'Can delete match',28,'delete_match'),(112,'Can view match',28,'view_match'),(113,'Can add player intake',29,'add_playerintake'),(114,'Can change player intake',29,'change_playerintake'),(115,'Can delete player intake',29,'delete_playerintake'),(116,'Can view player intake',29,'view_playerintake'),(117,'Can add Verjaardag',30,'add_birthday'),(118,'Can change Verjaardag',30,'change_birthday'),(119,'Can delete Verjaardag',30,'delete_birthday'),(120,'Can view Verjaardag',30,'view_birthday'),(121,'Can add Meetrainer jeugd',31,'add_youthguest'),(122,'Can change Meetrainer jeugd',31,'change_youthguest'),(123,'Can delete Meetrainer jeugd',31,'delete_youthguest'),(124,'Can view Meetrainer jeugd',31,'view_youthguest'),(125,'Can add weight entry',32,'add_weightentry'),(126,'Can change weight entry',32,'change_weightentry'),(127,'Can delete weight entry',32,'delete_weightentry'),(128,'Can view weight entry',32,'view_weightentry'),(129,'Can add Vakantieprogramma item',33,'add_vakantieprogrammaentry'),(130,'Can change Vakantieprogramma item',33,'change_vakantieprogrammaentry'),(131,'Can delete Vakantieprogramma item',33,'delete_vakantieprogrammaentry'),(132,'Can view Vakantieprogramma item',33,'view_vakantieprogrammaentry'),(133,'Can add Vakantieplanning',34,'add_vakantieplanning'),(134,'Can change Vakantieplanning',34,'change_vakantieplanning'),(135,'Can delete Vakantieplanning',34,'delete_vakantieplanning'),(136,'Can view Vakantieplanning',34,'view_vakantieplanning'),(137,'Can add Groeimeetpunt',35,'add_growthmeasurement'),(138,'Can change Groeimeetpunt',35,'change_growthmeasurement'),(139,'Can delete Groeimeetpunt',35,'delete_growthmeasurement'),(140,'Can view Groeimeetpunt',35,'view_growthmeasurement'),(141,'Can add Groeiprofiel',36,'add_growthprofile'),(142,'Can change Groeiprofiel',36,'change_growthprofile'),(143,'Can delete Groeiprofiel',36,'delete_growthprofile'),(144,'Can view Groeiprofiel',36,'view_growthprofile'),(145,'Can add team',37,'add_team'),(146,'Can change team',37,'change_team'),(147,'Can delete team',37,'delete_team'),(148,'Can view team',37,'view_team'),(149,'Can add day program entry',38,'add_dayprogramentry'),(150,'Can change day program entry',38,'change_dayprogramentry'),(151,'Can delete day program entry',38,'delete_dayprogramentry'),(152,'Can view day program entry',38,'view_dayprogramentry'),(153,'Can add hit week plan',39,'add_hitweekplan'),(154,'Can change hit week plan',39,'change_hitweekplan'),(155,'Can delete hit week plan',39,'delete_hitweekplan'),(156,'Can view hit week plan',39,'view_hitweekplan'),(157,'Can add injury case',40,'add_injurycase'),(158,'Can change injury case',40,'change_injurycase'),(159,'Can delete injury case',40,'delete_injurycase'),(160,'Can view injury case',40,'view_injurycase'),(161,'Can add player team assignment',41,'add_playerteamassignment'),(162,'Can change player team assignment',41,'change_playerteamassignment'),(163,'Can delete player team assignment',41,'delete_playerteamassignment'),(164,'Can view player team assignment',41,'view_playerteamassignment'),(165,'Can add hit week plan entry',42,'add_hitweekplanentry'),(166,'Can change hit week plan entry',42,'change_hitweekplanentry'),(167,'Can delete hit week plan entry',42,'delete_hitweekplanentry'),(168,'Can view hit week plan entry',42,'view_hitweekplanentry'),(169,'Can add anthropometry measurement',43,'add_anthropometrymeasurement'),(170,'Can change anthropometry measurement',43,'change_anthropometrymeasurement'),(171,'Can delete anthropometry measurement',43,'delete_anthropometrymeasurement'),(172,'Can view anthropometry measurement',43,'view_anthropometrymeasurement'),(173,'Can add anthropometry session',44,'add_anthropometrysession'),(174,'Can change anthropometry session',44,'change_anthropometrysession'),(175,'Can delete anthropometry session',44,'delete_anthropometrysession'),(176,'Can view anthropometry session',44,'view_anthropometrysession'),(177,'Can add nutrition intake session',45,'add_nutritionintakesession'),(178,'Can change nutrition intake session',45,'change_nutritionintakesession'),(179,'Can delete nutrition intake session',45,'delete_nutritionintakesession'),(180,'Can view nutrition intake session',45,'view_nutritionintakesession'),(181,'Can add nutrition intake item',46,'add_nutritionintakeitem'),(182,'Can change nutrition intake item',46,'change_nutritionintakeitem'),(183,'Can delete nutrition intake item',46,'delete_nutritionintakeitem'),(184,'Can view nutrition intake item',46,'view_nutritionintakeitem'),(185,'Can add birthday record',47,'add_birthdayrecord'),(186,'Can change birthday record',47,'change_birthdayrecord'),(187,'Can delete birthday record',47,'delete_birthdayrecord'),(188,'Can view birthday record',47,'view_birthdayrecord'),(189,'Can add birthday profile',48,'add_birthdayprofile'),(190,'Can change birthday profile',48,'change_birthdayprofile'),(191,'Can delete birthday profile',48,'delete_birthdayprofile'),(192,'Can view birthday profile',48,'view_birthdayprofile'),(193,'Can add youth guest week',49,'add_youthguestweek'),(194,'Can change youth guest week',49,'change_youthguestweek'),(195,'Can delete youth guest week',49,'delete_youthguestweek'),(196,'Can view youth guest week',49,'view_youthguestweek'),(197,'Can add youth guest profile',50,'add_youthguestprofile'),(198,'Can change youth guest profile',50,'change_youthguestprofile'),(199,'Can delete youth guest profile',50,'delete_youthguestprofile'),(200,'Can view youth guest profile',50,'view_youthguestprofile');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$1000000$pbUij1JS694KI4dHqKXsKf$VeO4hJf7u/PEg8C4v1pa+uvVqd4GVM9yHBXakF7KcSU=','2025-11-18 16:56:00.272299',1,'SiebeHermsen','','','Hermsen.siebe@gmail.com',1,1,'2025-11-07 10:02:59.036236');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=99 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2025-11-18 16:58:51.412758','47','Amine Lachkar',1,'[{\"added\": {}}]',7,1),(2,'2025-11-18 17:03:06.563269','13','Amine Lachkar',2,'[{\"changed\": {\"fields\": [\"Profielfoto\"]}}]',7,1),(3,'2025-11-18 17:03:13.053300','47','Amine Lachkar',3,'',7,1),(4,'2025-11-19 06:41:03.623101','27','Pieter van Maarschalkerwaard',2,'[{\"changed\": {\"fields\": [\"Profielfoto\"]}}]',7,1),(5,'2025-11-19 06:41:28.315812','26','Finn Stams',2,'[{\"changed\": {\"fields\": [\"Profielfoto\"]}}]',7,1),(6,'2025-11-19 06:41:54.836593','25','Mounir el Allouchi',2,'[{\"changed\": {\"fields\": [\"Profielfoto\"]}}]',7,1),(7,'2025-11-19 06:42:25.835988','24','Anass Zarrouk',2,'[{\"changed\": {\"fields\": [\"Profielfoto\"]}}]',7,1),(8,'2025-11-19 06:42:52.422354','23','Samuel Bamba',2,'[{\"changed\": {\"fields\": [\"Profielfoto\"]}}]',7,1),(9,'2025-11-19 06:43:49.409965','22','Armin Cullum',2,'[{\"changed\": {\"fields\": [\"Profielfoto\"]}}]',7,1),(10,'2025-11-19 06:44:31.135574','21','Alessandro Curini',2,'[{\"changed\": {\"fields\": [\"Profielfoto\"]}}]',7,1),(11,'2025-11-19 06:44:58.671760','20','Gijs Bessselink',2,'[{\"changed\": {\"fields\": [\"Profielfoto\"]}}]',7,1),(12,'2025-11-19 06:45:20.588044','19','Emilio Kehrer',2,'[{\"changed\": {\"fields\": [\"Profielfoto\"]}}]',7,1),(13,'2025-11-19 06:45:56.773968','18','Karst de Leeuw',2,'[{\"changed\": {\"fields\": [\"Profielfoto\"]}}]',7,1),(14,'2025-11-19 06:46:23.597944','17','Thomas Didilion Hödl',2,'[{\"changed\": {\"fields\": [\"Profielfoto\"]}}]',7,1),(15,'2025-11-19 06:46:51.587376','16','Per van Loon',2,'[{\"changed\": {\"fields\": [\"Profielfoto\"]}}]',7,1),(16,'2025-11-19 06:47:35.014905','14','Uriël van Aalst',2,'[{\"changed\": {\"fields\": [\"Profielfoto\"]}}]',7,1),(17,'2025-11-19 06:48:06.455699','12','Max de Waal',2,'[{\"changed\": {\"fields\": [\"Profielfoto\"]}}]',7,1),(18,'2025-11-19 06:49:01.251325','11','Nathan Tjoe-A-On',2,'[{\"changed\": {\"fields\": [\"Profielfoto\"]}}]',7,1),(19,'2025-11-19 06:49:30.751653','10','Thomas Verheydt',2,'[{\"changed\": {\"fields\": [\"Profielfoto\"]}}]',7,1),(20,'2025-11-19 06:51:04.590125','9','Siegert Baartmans',2,'[{\"changed\": {\"fields\": [\"Profielfoto\"]}}]',7,1),(21,'2025-11-19 06:51:31.594260','8','Wouter van der Steen',2,'[{\"changed\": {\"fields\": [\"Profielfoto\"]}}]',7,1),(22,'2025-11-19 06:52:37.207039','7','Devin Haen',2,'[{\"changed\": {\"fields\": [\"Profielfoto\"]}}]',7,1),(23,'2025-11-19 06:53:09.583889','6','Jens Mathijsen',2,'[{\"changed\": {\"fields\": [\"Profielfoto\", \"Voedingsaandachtspunt\"]}}]',7,1),(24,'2025-11-19 06:53:33.787392','5','Niels van Berkel',2,'[{\"changed\": {\"fields\": [\"Profielfoto\"]}}]',7,1),(25,'2025-11-19 06:54:01.601902','4','Jari Schuurman',2,'[{\"changed\": {\"fields\": [\"Profielfoto\"]}}]',7,1),(26,'2025-11-19 06:54:42.862346','3','Justin Hoogma',2,'[{\"changed\": {\"fields\": [\"Profielfoto\"]}}]',7,1),(27,'2025-11-19 06:55:09.066450','2','Raffael Behounek',2,'[{\"changed\": {\"fields\": [\"Profielfoto\"]}}]',7,1),(28,'2025-11-19 06:55:35.396047','1','Nick Doodeman',2,'[{\"changed\": {\"fields\": [\"Profielfoto\"]}}]',7,1),(29,'2025-11-19 08:30:55.894272','46','El Allouchi',3,'',7,1),(30,'2025-11-19 08:31:16.079852','45','Ciranni',3,'',7,1),(31,'2025-11-19 08:31:21.495707','44','Bamba',3,'',7,1),(32,'2025-11-19 08:31:25.133306','43','Zarrouk',3,'',7,1),(33,'2025-11-19 08:31:28.553505','42','Culum',3,'',7,1),(34,'2025-11-19 08:31:32.252787','41','Stam',3,'',7,1),(35,'2025-11-19 08:31:35.407650','40','Besselink',3,'',7,1),(36,'2025-11-19 08:31:38.823919','39','Maarschalkerwaard',3,'',7,1),(37,'2025-11-19 08:31:43.481545','38','Tjoe-A-On',3,'',7,1),(38,'2025-11-19 08:31:47.106630','37','Doodeman',3,'',7,1),(39,'2025-11-19 08:31:50.057186','36','Baartmans',3,'',7,1),(40,'2025-11-19 08:31:52.818777','35','Kehrer',3,'',7,1),(41,'2025-11-19 08:31:56.267334','34','Van Loon',3,'',7,1),(42,'2025-11-19 08:31:59.339336','33','Schuurman',3,'',7,1),(43,'2025-11-19 08:32:03.470360','32','Van Aalst',3,'',7,1),(44,'2025-11-19 08:32:06.542836','31','Hoogma',3,'',7,1),(45,'2025-11-19 08:32:09.885528','30','Mathijsen',3,'',7,1),(46,'2025-11-19 08:32:14.918991','29','Behounek',3,'',7,1),(47,'2025-11-21 11:48:32.814620','15','Junior Poortvliet',2,'[{\"changed\": {\"fields\": [\"Profielfoto\"]}}]',7,1),(48,'2025-11-21 11:49:47.012031','28','Boet van der Linden',2,'[{\"changed\": {\"fields\": [\"Profielfoto\"]}}]',7,1),(49,'2025-11-25 06:32:58.082365','1','John Stegeman',1,'[{\"added\": {}}]',23,1),(50,'2025-11-25 06:33:08.022302','2','Freek Heerkens',1,'[{\"added\": {}}]',23,1),(51,'2025-11-25 06:33:14.870856','3','Merijn Goris',1,'[{\"added\": {}}]',23,1),(52,'2025-11-25 06:33:37.862215','4','Sam Strijbosch',1,'[{\"added\": {}}]',23,1),(53,'2025-11-25 06:33:57.992484','5','Kristof Aalbrecht',1,'[{\"added\": {}}]',23,1),(54,'2025-11-25 06:34:09.372356','6','Pascal Diender',1,'[{\"added\": {}}]',23,1),(55,'2025-11-25 06:34:16.649441','7','Peter den Otter',1,'[{\"added\": {}}]',23,1),(56,'2025-11-25 06:34:22.582375','8','Ilse Driessen',1,'[{\"added\": {}}]',23,1),(57,'2025-11-25 06:34:51.266649','9','Henry van Amelsfoort',1,'[{\"added\": {}}]',23,1),(58,'2025-11-25 06:35:05.639408','10','Nils Thörner',1,'[{\"added\": {}}]',23,1),(59,'2025-11-25 06:35:18.054194','11','Jos de Kruijf',1,'[{\"added\": {}}]',23,1),(60,'2025-11-25 06:35:31.992411','12','Martin van den Heuvel',1,'[{\"added\": {}}]',23,1),(61,'2025-11-25 06:35:46.788911','13','Adrie Koster',1,'[{\"added\": {}}]',23,1),(62,'2025-11-25 06:35:59.760178','14','Steven Aptroot',1,'[{\"added\": {}}]',23,1),(63,'2025-11-25 06:36:14.123626','15','Pieter Vioen',1,'[{\"added\": {}}]',23,1),(64,'2025-11-25 06:36:26.369699','16','Sep Bierkens',1,'[{\"added\": {}}]',23,1),(65,'2025-11-25 06:36:36.968119','17','Michel de Gruijter',1,'[{\"added\": {}}]',23,1),(66,'2025-11-25 06:36:44.074546','18','Jasper de Langen',1,'[{\"added\": {}}]',23,1),(67,'2025-11-25 06:36:57.242449','19','Jos van Nieuwstadt',1,'[{\"added\": {}}]',23,1),(68,'2025-11-26 14:01:18.357255','83','El Allouchi (Dynamische middenvelder)',2,'[{\"changed\": {\"fields\": [\"Positie\"]}}]',7,1),(69,'2025-11-26 14:01:33.510942','27','Pieter van Maarschalkerwaard (Dynamische middenvelder)',2,'[{\"changed\": {\"fields\": [\"Positie\"]}}]',7,1),(70,'2025-11-26 14:01:38.789862','26','Finn Stams (Centrale verdediger)',2,'[{\"changed\": {\"fields\": [\"Positie\"]}}]',7,1),(71,'2025-11-26 14:01:47.908899','25','Mounir el Allouchi (Dynamische middenvelder)',2,'[{\"changed\": {\"fields\": [\"Positie\"]}}]',7,1),(72,'2025-11-26 14:01:56.533093','24','Anass Zarrouk (Dynamische middenvelder)',2,'[{\"changed\": {\"fields\": [\"Positie\"]}}]',7,1),(73,'2025-11-26 14:02:03.843922','23','Samuel Bamba (Buitenspeler)',2,'[{\"changed\": {\"fields\": [\"Positie\"]}}]',7,1),(74,'2025-11-26 14:02:10.547845','22','Armin Cullum (Buitenspeler)',2,'[{\"changed\": {\"fields\": [\"Positie\"]}}]',7,1),(75,'2025-11-26 14:02:16.978030','21','Alessandro Curini (Vleugelverdediger)',2,'[{\"changed\": {\"fields\": [\"Positie\"]}}]',7,1),(76,'2025-11-26 14:02:27.316031','20','Gijs Bessselink (Controlerende middenvelder)',2,'[{\"changed\": {\"fields\": [\"Positie\"]}}]',7,1),(77,'2025-11-26 14:02:34.199865','19','Emilio Kehrer (Buitenspeler)',2,'[{\"changed\": {\"fields\": [\"Positie\"]}}]',7,1),(78,'2025-11-26 14:02:43.011014','16','Per van Loon (Buitenspeler)',2,'[{\"changed\": {\"fields\": [\"Positie\"]}}]',7,1),(79,'2025-11-26 14:02:50.769041','15','Junior Poortvliet (Centrale verdediger)',2,'[{\"changed\": {\"fields\": [\"Positie\"]}}]',7,1),(80,'2025-11-26 14:02:59.075217','14','Uriël van Aalst (Dynamische middenvelder)',2,'[{\"changed\": {\"fields\": [\"Positie\"]}}]',7,1),(81,'2025-11-26 14:03:09.522132','13','Amine Lachkar (Controlerende middenvelder)',2,'[{\"changed\": {\"fields\": [\"Positie\"]}}]',7,1),(82,'2025-11-26 14:03:27.076044','12','Max de Waal (Controlerende middenvelder)',2,'[{\"changed\": {\"fields\": [\"Positie\"]}}]',7,1),(83,'2025-11-26 14:03:34.379195','11','Nathan Tjoe-A-On (Vleugelverdediger)',2,'[{\"changed\": {\"fields\": [\"Positie\"]}}]',7,1),(84,'2025-11-26 14:03:43.176529','10','Thomas Verheydt (Spits)',2,'[{\"changed\": {\"fields\": [\"Positie\"]}}]',7,1),(85,'2025-11-26 14:03:50.303151','9','Siegert Baartmans (Spits)',2,'[{\"changed\": {\"fields\": [\"Positie\"]}}]',7,1),(86,'2025-11-26 14:03:58.307092','7','Devin Haen (Spits)',2,'[{\"changed\": {\"fields\": [\"Positie\"]}}]',7,1),(87,'2025-11-26 14:04:05.769177','9','Siegert Baartmans (Targetman)',2,'[{\"changed\": {\"fields\": [\"Positie\"]}}]',7,1),(88,'2025-11-26 14:04:13.970205','6','Jens Mathijsen (Centrale verdediger)',2,'[{\"changed\": {\"fields\": [\"Positie\"]}}]',7,1),(89,'2025-11-26 14:04:20.595539','5','Niels van Berkel (Vleugelverdediger)',2,'[{\"changed\": {\"fields\": [\"Positie\"]}}]',7,1),(90,'2025-11-26 14:04:28.394650','3','Justin Hoogma (Centrale verdediger)',2,'[{\"changed\": {\"fields\": [\"Positie\"]}}]',7,1),(91,'2025-11-26 14:04:35.413434','4','Jari Schuurman (Dynamische middenvelder)',2,'[{\"changed\": {\"fields\": [\"Positie\"]}}]',7,1),(92,'2025-11-26 14:04:43.073208','2','Raffael Behounek (Centrale verdediger)',2,'[{\"changed\": {\"fields\": [\"Positie\"]}}]',7,1),(93,'2025-11-26 14:04:50.019045','1','Nick Doodeman (Buitenspeler)',2,'[{\"changed\": {\"fields\": [\"Positie\"]}}]',7,1),(94,'2025-11-27 17:24:23.308812','21','Alessandro Ciranni (Vleugelverdediger)',2,'[{\"changed\": {\"fields\": [\"Naam speler\"]}}]',7,1),(95,'2025-11-28 09:50:23.691607','2','Freek Heerkens',2,'[]',23,1),(96,'2025-11-28 17:33:43.949146','22','Armin Culum (Buitenspeler)',2,'[{\"changed\": {\"fields\": [\"Naam speler\"]}}]',7,1),(97,'2025-11-28 17:33:54.759619','20','Gijs Besselink (Controlerende middenvelder)',2,'[{\"changed\": {\"fields\": [\"Naam speler\"]}}]',7,1),(98,'2025-12-02 14:11:21.208265','83','El Allouchi (Dynamische middenvelder)',3,'',7,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(21,'main','aanwezigheid'),(43,'main','anthropometrymeasurement'),(44,'main','anthropometrysession'),(27,'main','antropometry'),(20,'main','attendance'),(30,'main','birthday'),(48,'main','birthdayprofile'),(47,'main','birthdayrecord'),(19,'main','dailyprogram'),(8,'main','dayprogram'),(38,'main','dayprogramentry'),(14,'main','fieldrehabsession'),(35,'main','growthmeasurement'),(36,'main','growthprofile'),(39,'main','hitweekplan'),(42,'main','hitweekplanentry'),(25,'main','hitweekplanning'),(9,'main','injury'),(40,'main','injurycase'),(28,'main','match'),(26,'main','nutritionday'),(46,'main','nutritionintakeitem'),(45,'main','nutritionintakesession'),(12,'main','oefening'),(22,'main','overig'),(7,'main','player'),(29,'main','playerintake'),(41,'main','playerteamassignment'),(10,'main','playertest'),(18,'main','popgesprek'),(15,'main','programma'),(16,'main','programmaoefening'),(17,'main','rpeentry'),(23,'main','staff'),(37,'main','team'),(11,'main','trainingdata'),(34,'main','vakantieplanning'),(33,'main','vakantieprogrammaentry'),(24,'main','wedstrijddata'),(32,'main','weightentry'),(13,'main','wellnessentry'),(31,'main','youthguest'),(50,'main','youthguestprofile'),(49,'main','youthguestweek'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=100 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-11-07 09:59:01.273167'),(2,'auth','0001_initial','2025-11-07 09:59:02.215760'),(3,'admin','0001_initial','2025-11-07 09:59:02.447028'),(4,'admin','0002_logentry_remove_auto_add','2025-11-07 09:59:02.456437'),(5,'admin','0003_logentry_add_action_flag_choices','2025-11-07 09:59:02.467737'),(6,'contenttypes','0002_remove_content_type_name','2025-11-07 09:59:02.621807'),(7,'auth','0002_alter_permission_name_max_length','2025-11-07 09:59:02.716331'),(8,'auth','0003_alter_user_email_max_length','2025-11-07 09:59:02.775961'),(9,'auth','0004_alter_user_username_opts','2025-11-07 09:59:02.791752'),(10,'auth','0005_alter_user_last_login_null','2025-11-07 09:59:02.871605'),(11,'auth','0006_require_contenttypes_0002','2025-11-07 09:59:02.884029'),(12,'auth','0007_alter_validators_add_error_messages','2025-11-07 09:59:02.899310'),(13,'auth','0008_alter_user_username_max_length','2025-11-07 09:59:03.011237'),(14,'auth','0009_alter_user_last_name_max_length','2025-11-07 09:59:03.123927'),(15,'auth','0010_alter_group_name_max_length','2025-11-07 09:59:03.165424'),(16,'auth','0011_update_proxy_permissions','2025-11-07 09:59:03.171094'),(17,'auth','0012_alter_user_first_name_max_length','2025-11-07 09:59:03.273236'),(20,'sessions','0001_initial','2025-11-07 09:59:03.567841'),(41,'main','0001_initial','2025-11-21 10:26:31.000000'),(42,'main','0002_alter_oefening_options_alter_playertest_options_and_more','2025-11-21 10:28:51.645062'),(43,'main','0003_alter_dailyprogram_date_alter_dailyprogram_player_and_more','2025-11-21 11:32:01.489138'),(44,'main','0004_attendance','2025-11-21 13:27:07.523018'),(45,'main','0005_aanwezigheid_delete_attendance','2025-11-21 14:01:40.362043'),(46,'main','0006_overig_delete_popgesprek','2025-11-24 06:20:04.240248'),(47,'main','0007_remove_overig_player','2025-11-24 06:34:34.367408'),(48,'main','0002_alter_oefening_player','2025-11-25 06:27:04.162291'),(49,'main','0003_wellnessentry','2025-11-25 06:28:06.992208'),(50,'main','0004_alter_wellnessentry_player','2025-11-25 06:28:06.994243'),(51,'main','0005_alter_oefening_player','2025-11-25 06:28:07.003158'),(52,'main','0006_injury_phase','2025-11-25 06:28:07.008121'),(53,'main','0007_player_nutrition_focus','2025-11-25 06:28:07.012159'),(54,'main','0008_playertest_created_at_playertest_curr_weight_and_more','2025-11-25 06:28:07.018541'),(55,'main','0009_alter_oefening_options_alter_playertest_options','2025-11-25 06:28:07.024414'),(56,'main','0010_oefening_focus_point','2025-11-25 06:28:07.029403'),(57,'main','0011_fieldrehabsession','2025-11-25 06:28:07.038012'),(58,'main','0012_programma_programmaoefening','2025-11-25 06:28:07.042317'),(59,'main','0013_player_image','2025-11-25 06:28:07.042317'),(60,'main','0014_rpeentry','2025-11-25 06:28:07.052228'),(61,'main','0015_remove_wellnessentry_rpe_alter_wellnessentry_date_and_more','2025-11-25 06:28:07.055014'),(62,'main','0016_rename_aandachtspunten_popgesprek_belangrijk_and_more','2025-11-25 06:28:07.060922'),(63,'main','0016_auto_20251121_0833','2025-11-25 06:28:07.064206'),(64,'main','0017_merge_20251125_0726','2025-11-25 06:28:07.072393'),(65,'main','0018_staff','2025-11-25 06:28:59.267270'),(66,'main','0019_alter_trainingdata_options_trainingdata_session_date_and_more','2025-11-26 09:46:43.921205'),(67,'main','0020_wedstrijddata','2025-11-26 11:13:45.999164'),(68,'main','0021_player_position_alter_player_name','2025-11-26 13:46:39.739792'),(69,'main','0022_wedstrijddata_accelerations_and_more','2025-11-28 17:22:31.887792'),(70,'main','0023_hitweekplanning','2025-12-05 10:33:11.411195'),(71,'main','0024_alter_hitweekplanning_trainer','2025-12-08 08:23:45.426953'),(72,'main','0025_alter_playertest_options_remove_playertest_name_and_more','2025-12-09 05:33:39.854146'),(73,'main','0026_playertest_length_alter_playertest_cmj_and_more','2025-12-09 05:53:36.457064'),(74,'main','0027_alter_playertest_options_playertest_test_date','2025-12-10 11:59:03.650026'),(75,'main','0028_nutritionday','2025-12-15 15:51:06.934847'),(76,'main','0029_antropometry','2025-12-17 09:27:34.189236'),(77,'main','0030_antropometry_fat_average_antropometry_fat_carter_and_more','2025-12-18 05:47:44.702329'),(78,'main','0031_match','2026-01-20 15:27:40.591848'),(79,'main','0032_alter_nutritionday_color_alter_nutritionday_meal_and_more','2026-02-05 06:22:34.823267'),(80,'main','0033_birthday','2026-02-06 14:45:13.432759'),(81,'main','0034_youthguest_playerintake_supplements','2026-02-06 16:02:29.408290'),(82,'main','0035_youthguest_days','2026-02-06 16:10:44.228043'),(83,'main','0036_remove_youthguest_days_weightentry','2026-02-07 07:02:28.758144'),(84,'main','0037_vakantieprogrammaentry','2026-02-07 11:04:04.258039'),(85,'main','0038_vakantieplanning','2026-02-07 11:22:39.014480'),(86,'main','0039_growthprofile_growthmeasurement','2026-02-17 17:22:29.514620'),(87,'main','0040_3nf_phase1_foundation','2026-02-18 09:15:06.573042'),(88,'main','0041_rename_main_injuryc_player__8c0f5b_idx_main_injury_player__4e7bb7_idx_and_more','2026-02-18 09:15:06.643435'),(89,'main','0042_backfill_3nf_phase1_data','2026-02-18 10:31:10.993447'),(90,'main','0043_backfill_dayprogramentry','2026-02-18 10:39:15.777882'),(91,'main','0044_anthropometrysession_anthropometrymeasurement','2026-02-18 11:00:27.939597'),(92,'main','0045_backfill_anthropometry_v2','2026-02-18 11:00:28.079186'),(93,'main','0046_nutritionintakesession_nutritionintakeitem','2026-02-18 11:47:42.681687'),(94,'main','0047_backfill_nutrition_intake_v2','2026-02-18 11:47:42.695563'),(95,'main','0046_rename_main_anthro_category_3366cb_idx_main_anthro_categor_c3426b_idx','2026-02-18 11:47:42.714992'),(96,'main','0048_merge_0046_rename_and_0047_nutrition','2026-02-18 11:47:42.714992'),(97,'main','0049_deprecate_legacy_tables_preflight','2026-02-18 12:45:31.696773'),(98,'main','0050_birthdayprofile_birthdayrecord_youthguestprofile_youthguestweek','2026-02-18 13:16:17.101707'),(99,'main','0051_backfill_birthday_youthguest_v2','2026-02-18 13:16:17.111766');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('47axpa2unj9fyhfitu3kbh2sasij3hnp','.eJxVjDsOwjAQBe_iGln-yjElPWewdu1dHEC2FCcV4u4QKQW0b2beSyTY1pq2QUuaizgLLU6_G0J-UNtBuUO7dZl7W5cZ5a7Igw557YWel8P9O6gw6rfOQIhI3kWlomGDQaNnbzIYhTZYA-SyIh0dT5QtT8AmakZUPnjWRbw_BHQ4qw:1vLOzo:3nkqSwaLua0EhVgNPjp3j4L0LAOmtYXxTBX_pLNOoTI','2025-12-02 16:56:00.280423');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_aanwezigheid`
--

DROP TABLE IF EXISTS `main_aanwezigheid`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_aanwezigheid` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `status` varchar(30) NOT NULL,
  `completed` tinyint(1) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `player_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `main_aanwezigheid_player_id_date_6ad848f1_uniq` (`player_id`,`date`),
  CONSTRAINT `main_aanwezigheid_player_id_0782175e_fk_main_player_id` FOREIGN KEY (`player_id`) REFERENCES `main_player` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=722 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_aanwezigheid`
--

LOCK TABLES `main_aanwezigheid` WRITE;
/*!40000 ALTER TABLE `main_aanwezigheid` DISABLE KEYS */;
INSERT INTO `main_aanwezigheid` VALUES (1,'2025-11-21','overig',0,'2025-11-21 14:01:57.457449',21),(2,'2025-11-21','overig',0,'2025-11-21 14:01:57.466042',13),(3,'2025-11-21','overig',0,'2025-11-21 14:01:57.474465',24),(4,'2025-11-21','overig',0,'2025-11-21 14:19:45.600459',22),(5,'2025-11-21','overig',0,'2025-11-21 14:01:57.492558',28),(6,'2025-11-21','overig',0,'2025-11-21 14:01:57.501126',7),(7,'2025-11-21','overig',0,'2025-11-21 14:01:57.511178',19),(8,'2025-11-21','overig',0,'2025-11-21 14:01:57.519332',26),(9,'2025-11-21','overig',0,'2025-11-21 14:01:57.526898',20),(10,'2025-11-21','overig',0,'2025-11-21 14:01:57.535245',4),(11,'2025-11-21','overig',0,'2025-11-21 14:01:57.544272',6),(12,'2025-11-21','overig',0,'2025-11-21 14:01:57.552362',15),(13,'2025-11-21','overig',0,'2025-11-21 14:01:57.560772',3),(14,'2025-11-21','overig',0,'2025-11-21 14:01:57.569527',18),(15,'2025-11-21','overig',0,'2025-11-21 14:01:57.577485',12),(16,'2025-11-21','overig',0,'2025-11-21 14:01:57.585663',25),(17,'2025-11-21','overig',0,'2025-11-21 14:01:57.594675',11),(18,'2025-11-21','overig',0,'2025-11-21 14:01:57.604425',1),(19,'2025-11-21','overig',0,'2025-11-21 14:01:57.611580',5),(20,'2025-11-21','overig',0,'2025-11-21 14:01:57.620954',16),(21,'2025-11-21','overig',0,'2025-11-21 14:01:57.629569',27),(22,'2025-11-21','overig',0,'2025-11-21 14:01:57.636871',2),(23,'2025-11-21','overig',0,'2025-11-21 14:01:57.645922',23),(24,'2025-11-21','overig',0,'2025-11-21 14:01:57.654875',9),(25,'2025-11-21','overig',0,'2025-11-21 14:01:57.664077',17),(26,'2025-11-21','overig',0,'2025-11-21 14:01:57.674731',10),(27,'2025-11-21','overig',0,'2025-11-21 14:01:57.682508',14),(28,'2025-11-21','overig',0,'2025-11-21 14:01:57.692319',8),(29,'2025-11-22','overig',0,'2025-11-22 19:55:56.633534',21),(30,'2025-11-22','overig',0,'2025-11-21 14:24:51.939395',13),(31,'2025-11-22','overig',0,'2025-11-21 14:24:51.944393',24),(32,'2025-11-22','overig',0,'2025-11-21 14:24:51.947396',22),(33,'2025-11-22','overig',0,'2025-11-21 14:24:51.954524',28),(34,'2025-11-22','overig',0,'2025-11-21 14:24:51.958540',7),(35,'2025-11-22','overig',0,'2025-11-21 14:24:51.966523',19),(36,'2025-11-22','overig',0,'2025-11-21 14:24:51.969863',26),(37,'2025-11-22','overig',0,'2025-11-21 14:24:51.973489',20),(38,'2025-11-22','overig',0,'2025-11-21 14:24:51.973489',4),(39,'2025-11-22','overig',0,'2025-11-21 14:24:51.981063',6),(40,'2025-11-22','overig',0,'2025-11-21 14:24:51.984762',15),(41,'2025-11-22','overig',0,'2025-11-21 14:24:51.986628',3),(42,'2025-11-22','overig',0,'2025-11-21 14:24:51.986628',18),(43,'2025-11-22','overig',0,'2025-11-21 14:24:51.986628',12),(44,'2025-11-22','overig',0,'2025-11-21 14:24:51.986628',25),(45,'2025-11-22','overig',0,'2025-11-21 14:24:52.001455',11),(46,'2025-11-22','overig',0,'2025-11-21 14:24:52.003463',1),(47,'2025-11-22','overig',0,'2025-11-21 14:24:52.003463',5),(48,'2025-11-22','overig',0,'2025-11-21 14:24:52.003463',16),(49,'2025-11-22','overig',0,'2025-11-21 14:24:52.003463',27),(50,'2025-11-22','overig',0,'2025-11-21 14:24:52.019655',2),(51,'2025-11-22','overig',0,'2025-11-21 14:24:52.024409',23),(52,'2025-11-22','overig',0,'2025-11-21 14:24:52.026418',9),(53,'2025-11-22','overig',0,'2025-11-21 14:24:52.026418',17),(54,'2025-11-22','overig',0,'2025-11-21 14:24:52.034737',10),(55,'2025-11-22','overig',0,'2025-11-21 14:24:52.035807',14),(56,'2025-11-22','overig',0,'2025-11-21 14:24:52.035807',8),(57,'2025-11-24','overig',0,'2025-11-24 16:39:51.851757',21),(58,'2025-11-24','overig',0,'2025-11-24 06:08:25.878502',13),(59,'2025-11-24','overig',0,'2025-11-24 06:08:25.886668',24),(60,'2025-11-24','overig',0,'2025-11-24 06:08:25.895004',22),(61,'2025-11-24','overig',0,'2025-11-24 06:08:25.901078',28),(62,'2025-11-24','overig',0,'2025-11-24 06:08:25.901078',7),(63,'2025-11-24','overig',0,'2025-11-24 06:08:25.916573',19),(64,'2025-11-24','overig',0,'2025-11-24 06:08:25.924630',26),(65,'2025-11-24','overig',0,'2025-11-24 06:08:25.930105',20),(66,'2025-11-24','overig',0,'2025-11-24 06:08:25.930105',4),(67,'2025-11-24','overig',0,'2025-11-24 06:08:25.946833',6),(68,'2025-11-24','overig',0,'2025-11-24 06:08:25.946833',15),(69,'2025-11-24','overig',0,'2025-11-24 06:08:25.963405',3),(70,'2025-11-24','overig',0,'2025-11-24 06:08:25.964748',18),(71,'2025-11-24','overig',0,'2025-11-24 06:08:25.974488',12),(72,'2025-11-24','overig',0,'2025-11-24 06:08:25.980051',25),(73,'2025-11-24','overig',0,'2025-11-24 06:08:25.990234',11),(74,'2025-11-24','overig',0,'2025-11-24 06:08:25.999961',1),(75,'2025-11-24','overig',0,'2025-11-24 06:08:26.008023',5),(76,'2025-11-24','overig',0,'2025-11-24 06:08:26.015650',16),(77,'2025-11-24','overig',0,'2025-11-24 06:08:26.022841',27),(78,'2025-11-24','overig',0,'2025-11-24 06:08:26.029758',2),(79,'2025-11-24','overig',0,'2025-11-24 06:08:26.037502',23),(80,'2025-11-24','overig',0,'2025-11-24 06:08:26.046801',9),(81,'2025-11-24','overig',0,'2025-11-24 06:08:26.046801',17),(82,'2025-11-24','overig',0,'2025-11-24 06:08:26.061730',10),(83,'2025-11-24','overig',0,'2025-11-24 06:08:26.063334',14),(84,'2025-11-24','overig',0,'2025-11-24 06:08:26.078350',8),(85,'2025-11-25','overig',0,'2025-11-25 17:04:27.216320',21),(86,'2025-11-25','overig',0,'2025-11-25 05:59:48.914130',13),(87,'2025-11-25','overig',0,'2025-11-25 05:59:48.924192',24),(88,'2025-11-25','overig',0,'2025-11-25 05:59:48.931505',22),(89,'2025-11-25','overig',0,'2025-11-25 05:59:48.937654',28),(90,'2025-11-25','overig',0,'2025-11-25 05:59:48.943836',7),(91,'2025-11-25','overig',0,'2025-11-25 05:59:48.954211',19),(92,'2025-11-25','overig',0,'2025-11-25 05:59:48.958379',26),(93,'2025-11-25','overig',0,'2025-11-25 05:59:48.969160',20),(94,'2025-11-25','overig',0,'2025-11-25 05:59:48.974965',4),(95,'2025-11-25','overig',0,'2025-11-25 05:59:48.982998',6),(96,'2025-11-25','overig',0,'2025-11-25 05:59:48.988196',15),(97,'2025-11-25','overig',0,'2025-11-25 05:59:48.993881',3),(98,'2025-11-25','overig',0,'2025-11-25 05:59:49.004292',18),(99,'2025-11-25','overig',0,'2025-11-25 05:59:49.010474',12),(100,'2025-11-25','overig',0,'2025-11-25 05:59:49.017918',25),(101,'2025-11-25','overig',0,'2025-11-25 05:59:49.024134',11),(102,'2025-11-25','overig',0,'2025-11-25 05:59:49.025264',1),(103,'2025-11-25','overig',0,'2025-11-25 05:59:49.036366',5),(104,'2025-11-25','overig',0,'2025-11-25 05:59:49.044014',16),(105,'2025-11-25','overig',0,'2025-11-25 05:59:49.048242',27),(106,'2025-11-25','overig',0,'2025-11-25 05:59:49.054045',2),(107,'2025-11-25','overig',0,'2025-11-25 05:59:49.054045',23),(108,'2025-11-25','overig',0,'2025-11-25 05:59:49.070284',9),(109,'2025-11-25','overig',0,'2025-11-25 05:59:49.073941',17),(110,'2025-11-25','overig',0,'2025-11-25 05:59:49.084081',10),(111,'2025-11-25','overig',0,'2025-11-25 05:59:49.088380',14),(112,'2025-11-25','overig',0,'2025-11-25 05:59:49.094155',8),(113,'2025-11-26','overig',0,'2025-11-26 08:40:10.033869',21),(114,'2025-11-26','overig',0,'2025-11-26 08:40:10.041102',13),(115,'2025-11-26','overig',0,'2025-11-26 08:40:10.050992',24),(116,'2025-11-26','overig',0,'2025-11-26 08:40:10.056316',22),(121,'2025-11-26','overig',0,'2025-11-26 08:40:10.092419',28),(124,'2025-11-26','overig',0,'2025-11-26 08:40:10.110465',7),(127,'2025-11-26','overig',0,'2025-11-26 08:40:10.126887',19),(128,'2025-11-26','overig',0,'2025-11-26 08:40:10.131087',26),(129,'2025-11-26','overig',0,'2025-11-26 08:40:10.141209',20),(131,'2025-11-26','overig',0,'2025-11-26 08:40:10.153786',4),(132,'2025-11-26','overig',0,'2025-11-26 08:40:10.162063',6),(133,'2025-11-26','overig',0,'2025-11-26 08:40:10.167930',15),(134,'2025-11-26','overig',0,'2025-11-26 08:40:10.172067',3),(135,'2025-11-26','overig',0,'2025-11-26 08:40:10.175816',18),(139,'2025-11-26','overig',0,'2025-11-26 08:40:10.201343',12),(140,'2025-11-26','overig',0,'2025-11-26 08:40:10.205674',25),(141,'2025-11-26','overig',0,'2025-11-26 08:40:10.215099',11),(142,'2025-11-26','overig',0,'2025-11-26 08:40:10.223307',1),(143,'2025-11-26','overig',0,'2025-11-26 08:40:10.231200',5),(144,'2025-11-26','overig',0,'2025-11-26 08:40:10.236864',16),(145,'2025-11-26','overig',0,'2025-11-26 08:40:10.240993',27),(146,'2025-11-26','overig',0,'2025-11-26 08:40:10.248007',2),(147,'2025-11-26','overig',0,'2025-11-26 08:40:10.251183',23),(149,'2025-11-26','overig',0,'2025-11-26 08:40:10.263241',9),(151,'2025-11-26','overig',0,'2025-11-26 08:40:10.282162',17),(152,'2025-11-26','overig',0,'2025-11-26 08:40:10.282162',10),(154,'2025-11-26','overig',0,'2025-11-26 08:40:10.302186',14),(157,'2025-11-26','overig',0,'2025-11-26 08:40:10.321141',8),(159,'2025-11-28','overig',0,'2025-11-28 09:46:16.099426',21),(160,'2025-11-28','overig',0,'2025-11-28 09:46:16.099426',13),(161,'2025-11-28','overig',0,'2025-11-28 09:46:16.113772',24),(162,'2025-11-28','overig',0,'2025-11-28 09:46:16.115853',22),(163,'2025-11-28','overig',0,'2025-11-28 09:46:16.129622',28),(164,'2025-11-28','overig',0,'2025-11-28 09:46:16.132541',7),(166,'2025-11-28','overig',0,'2025-11-28 09:46:16.152879',19),(167,'2025-11-28','overig',0,'2025-11-28 09:46:16.163132',26),(168,'2025-11-28','overig',0,'2025-11-28 09:46:16.169032',20),(169,'2025-11-28','overig',0,'2025-11-28 09:46:16.169032',4),(170,'2025-11-28','overig',0,'2025-11-28 09:46:16.181171',6),(171,'2025-11-28','overig',0,'2025-11-28 09:46:16.185475',15),(172,'2025-11-28','overig',0,'2025-11-28 09:46:16.196188',3),(173,'2025-11-28','overig',0,'2025-11-28 09:46:16.200920',18),(174,'2025-11-28','overig',0,'2025-11-28 09:46:16.209215',12),(175,'2025-11-28','overig',0,'2025-11-28 09:46:16.219716',25),(176,'2025-11-28','overig',0,'2025-11-28 09:46:16.225264',11),(177,'2025-11-28','overig',0,'2025-11-28 09:46:16.230960',1),(178,'2025-11-28','overig',0,'2025-11-28 09:46:16.241553',5),(179,'2025-11-28','overig',0,'2025-11-28 09:46:16.241553',16),(180,'2025-11-28','overig',0,'2025-11-28 09:46:16.249593',27),(181,'2025-11-28','overig',0,'2025-11-28 09:46:16.259725',2),(182,'2025-11-28','overig',0,'2025-11-28 09:46:16.264063',23),(183,'2025-11-28','overig',0,'2025-11-28 09:46:16.275787',9),(184,'2025-11-28','overig',0,'2025-11-28 09:46:16.280995',17),(185,'2025-11-28','overig',0,'2025-11-28 09:46:16.280995',10),(186,'2025-11-28','overig',0,'2025-11-28 09:46:16.296226',14),(187,'2025-11-28','overig',0,'2025-11-28 09:46:16.297451',8),(188,'2025-11-29','overig',0,'2025-11-28 09:46:49.880836',21),(189,'2025-11-29','overig',0,'2025-11-28 09:46:49.888978',13),(190,'2025-11-29','overig',0,'2025-11-28 09:46:49.897208',24),(191,'2025-11-29','overig',0,'2025-11-28 09:46:49.903153',22),(192,'2025-11-29','overig',0,'2025-11-28 09:46:49.913376',28),(193,'2025-11-29','overig',0,'2025-11-28 09:46:49.918887',7),(195,'2025-11-29','overig',0,'2025-11-28 09:46:49.934903',19),(196,'2025-11-29','overig',0,'2025-11-28 09:46:49.936352',26),(197,'2025-11-29','overig',0,'2025-11-28 09:46:49.945857',20),(198,'2025-11-29','overig',0,'2025-11-28 09:46:49.954162',4),(199,'2025-11-29','overig',0,'2025-11-28 09:46:49.962304',6),(200,'2025-11-29','overig',0,'2025-11-28 09:46:49.968150',15),(201,'2025-11-29','overig',0,'2025-11-28 09:46:49.969726',3),(202,'2025-11-29','overig',0,'2025-11-28 09:46:49.978419',18),(203,'2025-11-29','overig',0,'2025-11-28 09:46:49.986696',12),(204,'2025-11-29','overig',0,'2025-11-28 09:46:49.986696',25),(205,'2025-11-29','overig',0,'2025-11-28 09:46:50.003489',11),(206,'2025-11-29','overig',0,'2025-11-28 09:46:50.010188',1),(207,'2025-11-29','overig',0,'2025-11-28 09:46:50.022934',5),(208,'2025-11-29','overig',0,'2025-11-28 09:46:50.031169',16),(209,'2025-11-29','overig',0,'2025-11-28 09:46:50.038478',27),(210,'2025-11-29','overig',0,'2025-11-28 09:46:50.038478',2),(211,'2025-11-29','overig',0,'2025-11-28 09:46:50.052093',23),(212,'2025-11-29','overig',0,'2025-11-28 09:46:50.054294',9),(213,'2025-11-29','overig',0,'2025-11-28 09:46:50.068217',17),(214,'2025-11-29','overig',0,'2025-11-28 09:46:50.072700',10),(215,'2025-11-29','overig',0,'2025-11-28 09:46:50.081219',14),(216,'2025-11-29','overig',0,'2025-11-28 09:46:50.089826',8),(217,'2025-12-01','overig',0,'2025-12-01 16:13:46.493087',21),(218,'2025-12-01','overig',0,'2025-12-01 16:13:46.510901',13),(219,'2025-12-01','overig',0,'2025-12-01 16:13:46.518134',24),(220,'2025-12-01','overig',0,'2025-12-01 16:13:46.526277',22),(221,'2025-12-01','overig',0,'2025-12-01 16:13:46.534289',28),(222,'2025-12-01','overig',0,'2025-12-01 16:13:46.534289',7),(224,'2025-12-01','overig',0,'2025-12-01 16:13:46.544482',19),(225,'2025-12-01','overig',0,'2025-12-01 16:13:46.560506',26),(226,'2025-12-01','overig',0,'2025-12-01 16:13:46.566714',20),(227,'2025-12-01','overig',0,'2025-12-01 16:13:46.575199',4),(228,'2025-12-01','overig',0,'2025-12-01 16:13:46.577767',6),(229,'2025-12-01','overig',0,'2025-12-01 16:13:46.577767',15),(230,'2025-12-01','overig',0,'2025-12-01 16:13:46.592980',3),(231,'2025-12-01','overig',0,'2025-12-01 16:13:46.594274',18),(232,'2025-12-01','overig',0,'2025-12-01 16:13:46.594274',12),(233,'2025-12-01','overig',0,'2025-12-01 16:13:46.611065',25),(234,'2025-12-01','overig',0,'2025-12-01 16:13:46.611065',11),(235,'2025-12-01','overig',0,'2025-12-01 16:13:46.624998',1),(236,'2025-12-01','overig',0,'2025-12-01 16:13:46.630773',5),(237,'2025-12-01','overig',0,'2025-12-01 16:13:46.640324',16),(238,'2025-12-01','overig',0,'2025-12-01 16:13:46.646730',27),(239,'2025-12-01','overig',0,'2025-12-01 16:13:46.654873',2),(240,'2025-12-01','overig',0,'2025-12-01 16:13:46.661742',23),(241,'2025-12-01','overig',0,'2025-12-01 16:13:46.670222',9),(242,'2025-12-01','overig',0,'2025-12-01 16:13:46.677713',17),(243,'2025-12-01','overig',0,'2025-12-01 16:13:46.686145',10),(244,'2025-12-01','overig',0,'2025-12-01 16:13:46.692988',14),(245,'2025-12-01','overig',0,'2025-12-01 16:13:46.694479',8),(246,'2025-12-02','overig',0,'2025-12-02 14:11:36.296205',21),(247,'2025-12-02','overig',0,'2025-12-02 14:11:36.301584',13),(248,'2025-12-02','overig',0,'2025-12-02 14:11:36.304605',24),(249,'2025-12-02','overig',0,'2025-12-02 14:11:36.307604',22),(250,'2025-12-02','overig',0,'2025-12-02 14:11:36.310608',28),(251,'2025-12-02','overig',0,'2025-12-02 14:11:36.312606',7),(252,'2025-12-02','overig',0,'2025-12-02 14:11:36.316295',19),(253,'2025-12-02','overig',0,'2025-12-02 14:11:36.320302',26),(254,'2025-12-02','overig',0,'2025-12-02 14:11:36.323303',20),(255,'2025-12-02','overig',0,'2025-12-02 14:11:36.326302',4),(256,'2025-12-02','overig',0,'2025-12-02 14:11:36.328301',6),(257,'2025-12-02','overig',0,'2025-12-02 14:11:36.331323',15),(258,'2025-12-02','overig',0,'2025-12-02 14:11:36.334329',3),(259,'2025-12-02','overig',0,'2025-12-02 14:11:36.336820',18),(260,'2025-12-02','overig',0,'2025-12-02 14:11:36.338820',12),(261,'2025-12-02','overig',0,'2025-12-02 14:11:36.340800',25),(262,'2025-12-02','overig',0,'2025-12-02 14:11:36.342801',11),(263,'2025-12-02','overig',0,'2025-12-02 14:11:36.345822',1),(264,'2025-12-02','overig',0,'2025-12-02 14:11:36.348623',5),(265,'2025-12-02','overig',0,'2025-12-02 14:11:36.351294',16),(266,'2025-12-02','overig',0,'2025-12-02 14:11:36.353685',27),(267,'2025-12-02','overig',0,'2025-12-02 14:11:36.355682',2),(268,'2025-12-02','overig',0,'2025-12-02 14:11:36.358167',23),(269,'2025-12-02','overig',0,'2025-12-02 14:11:36.361187',9),(270,'2025-12-02','overig',0,'2025-12-02 14:11:36.363189',17),(271,'2025-12-02','overig',0,'2025-12-02 14:11:36.366234',10),(272,'2025-12-02','overig',0,'2025-12-02 14:11:36.368694',14),(273,'2025-12-02','overig',0,'2025-12-02 14:11:36.371695',8),(274,'2025-12-05','overig',0,'2025-12-05 10:38:49.709010',21),(275,'2025-12-05','overig',0,'2025-12-05 10:38:49.714010',13),(276,'2025-12-05','overig',0,'2025-12-05 10:38:49.718091',24),(277,'2025-12-05','overig',0,'2025-12-05 10:38:49.722078',22),(278,'2025-12-05','overig',0,'2025-12-05 10:38:49.725460',28),(279,'2025-12-05','overig',0,'2025-12-05 10:38:49.728460',7),(280,'2025-12-05','overig',0,'2025-12-05 10:38:49.732481',19),(281,'2025-12-05','overig',0,'2025-12-05 10:38:49.736109',26),(282,'2025-12-05','overig',0,'2025-12-05 10:38:49.737161',20),(283,'2025-12-05','overig',0,'2025-12-05 10:38:49.742739',4),(284,'2025-12-05','overig',0,'2025-12-05 10:38:49.742739',6),(285,'2025-12-05','overig',0,'2025-12-05 10:38:49.742739',15),(286,'2025-12-05','overig',0,'2025-12-05 10:38:49.754153',3),(287,'2025-12-05','overig',0,'2025-12-05 10:38:49.758152',18),(288,'2025-12-05','overig',0,'2025-12-05 10:38:49.762170',12),(289,'2025-12-05','overig',0,'2025-12-05 10:38:49.765151',25),(290,'2025-12-05','overig',0,'2025-12-05 10:38:49.769151',11),(291,'2025-12-05','overig',0,'2025-12-05 10:38:49.773249',1),(292,'2025-12-05','overig',0,'2025-12-05 10:38:49.775256',5),(293,'2025-12-05','overig',0,'2025-12-05 10:38:49.779272',16),(294,'2025-12-05','overig',0,'2025-12-05 10:38:49.783287',27),(295,'2025-12-05','overig',0,'2025-12-05 10:38:49.786987',2),(296,'2025-12-05','overig',0,'2025-12-05 10:38:49.791109',23),(297,'2025-12-05','overig',0,'2025-12-05 10:38:49.795144',9),(298,'2025-12-05','overig',0,'2025-12-05 10:38:49.797152',17),(299,'2025-12-05','overig',0,'2025-12-05 10:38:49.797152',10),(300,'2025-12-05','overig',0,'2025-12-05 10:38:49.805017',14),(301,'2025-12-05','overig',0,'2025-12-05 10:38:49.807025',8),(302,'2025-12-06','overig',0,'2025-12-06 12:56:02.048704',21),(303,'2025-12-06','overig',0,'2025-12-06 12:56:02.052223',13),(304,'2025-12-06','overig',0,'2025-12-06 12:56:02.052223',24),(305,'2025-12-06','overig',0,'2025-12-06 12:56:02.052223',22),(306,'2025-12-06','overig',0,'2025-12-06 12:56:02.052223',28),(307,'2025-12-06','overig',0,'2025-12-06 12:56:02.068929',7),(308,'2025-12-06','overig',0,'2025-12-06 12:56:02.068929',19),(309,'2025-12-06','overig',0,'2025-12-06 12:56:02.068929',26),(310,'2025-12-06','overig',0,'2025-12-06 12:56:02.068929',20),(311,'2025-12-06','overig',0,'2025-12-06 12:56:02.068929',4),(312,'2025-12-06','overig',0,'2025-12-06 12:56:02.068929',6),(313,'2025-12-06','overig',0,'2025-12-06 12:56:02.084894',15),(314,'2025-12-06','overig',0,'2025-12-06 12:56:02.085631',3),(315,'2025-12-06','overig',0,'2025-12-06 12:56:02.085631',18),(316,'2025-12-06','overig',0,'2025-12-06 12:56:02.085631',12),(317,'2025-12-06','overig',0,'2025-12-06 12:56:02.085631',25),(318,'2025-12-06','overig',0,'2025-12-06 12:56:02.085631',11),(319,'2025-12-06','overig',0,'2025-12-06 12:56:02.085631',1),(320,'2025-12-06','overig',0,'2025-12-06 12:56:02.102200',5),(321,'2025-12-06','overig',0,'2025-12-06 12:56:02.105070',16),(322,'2025-12-06','overig',0,'2025-12-06 12:56:02.105070',27),(323,'2025-12-06','overig',0,'2025-12-06 12:56:02.105070',2),(324,'2025-12-06','overig',0,'2025-12-06 12:56:02.105070',23),(325,'2025-12-06','overig',0,'2025-12-06 12:56:02.105070',9),(326,'2025-12-06','overig',0,'2025-12-06 12:56:02.105070',17),(327,'2025-12-06','overig',0,'2025-12-06 12:56:02.118820',10),(328,'2025-12-06','overig',0,'2025-12-06 12:56:02.118820',14),(329,'2025-12-06','overig',0,'2025-12-06 12:56:02.118820',8),(330,'2025-12-08','overig',0,'2025-12-08 12:02:34.373235',21),(331,'2025-12-08','overig',0,'2025-12-08 12:02:34.381231',13),(332,'2025-12-08','overig',0,'2025-12-08 12:02:34.385246',24),(333,'2025-12-08','overig',0,'2025-12-08 12:02:34.390335',22),(334,'2025-12-08','overig',0,'2025-12-08 12:02:34.393325',28),(335,'2025-12-08','overig',0,'2025-12-08 12:02:34.395325',7),(336,'2025-12-08','overig',0,'2025-12-08 12:02:34.398325',19),(337,'2025-12-08','overig',0,'2025-12-08 12:02:34.401329',26),(338,'2025-12-08','overig',0,'2025-12-08 12:02:34.405411',20),(339,'2025-12-08','overig',0,'2025-12-08 12:02:34.408458',4),(340,'2025-12-08','overig',0,'2025-12-08 12:02:34.411441',6),(341,'2025-12-08','overig',0,'2025-12-08 12:02:34.414444',15),(342,'2025-12-08','overig',0,'2025-12-08 12:02:34.416442',3),(343,'2025-12-08','overig',0,'2025-12-08 12:02:34.419387',18),(344,'2025-12-08','overig',0,'2025-12-08 12:02:34.423130',12),(345,'2025-12-08','overig',0,'2025-12-08 12:02:34.426121',25),(346,'2025-12-08','overig',0,'2025-12-08 12:02:34.428126',11),(347,'2025-12-08','overig',0,'2025-12-08 12:02:34.431105',1),(348,'2025-12-08','overig',0,'2025-12-08 12:02:34.434104',5),(349,'2025-12-08','overig',0,'2025-12-08 12:02:34.437778',16),(350,'2025-12-08','overig',0,'2025-12-08 12:02:34.440465',27),(351,'2025-12-08','overig',0,'2025-12-08 12:02:34.443480',2),(352,'2025-12-08','overig',0,'2025-12-08 12:02:34.445463',23),(353,'2025-12-08','overig',0,'2025-12-08 12:02:34.448461',9),(354,'2025-12-08','overig',0,'2025-12-08 12:02:34.451462',17),(355,'2025-12-08','overig',0,'2025-12-08 12:02:34.454720',10),(356,'2025-12-08','overig',0,'2025-12-08 12:02:34.458579',14),(357,'2025-12-08','overig',0,'2025-12-08 12:02:34.461579',8),(358,'2025-12-10','overig',0,'2025-12-10 10:58:08.290517',21),(359,'2025-12-10','overig',0,'2025-12-10 10:58:08.297629',13),(360,'2025-12-10','overig',0,'2025-12-10 10:58:08.300606',24),(361,'2025-12-10','overig',0,'2025-12-10 10:58:08.304621',22),(362,'2025-12-10','overig',0,'2025-12-10 10:58:08.307626',28),(363,'2025-12-10','overig',0,'2025-12-10 10:58:08.310625',7),(364,'2025-12-10','overig',0,'2025-12-10 10:58:08.311480',19),(365,'2025-12-10','overig',0,'2025-12-10 10:58:08.311480',26),(366,'2025-12-10','overig',0,'2025-12-10 10:58:08.311480',20),(367,'2025-12-10','overig',0,'2025-12-10 10:58:08.311480',4),(368,'2025-12-10','overig',0,'2025-12-10 10:58:08.326609',6),(369,'2025-12-10','overig',0,'2025-12-10 10:58:08.329075',15),(370,'2025-12-10','overig',0,'2025-12-10 10:58:08.329075',3),(371,'2025-12-10','overig',0,'2025-12-10 10:58:08.329075',18),(372,'2025-12-10','overig',0,'2025-12-10 10:58:08.329075',12),(373,'2025-12-10','overig',0,'2025-12-10 10:58:08.329075',25),(374,'2025-12-10','overig',0,'2025-12-10 10:58:08.344804',11),(375,'2025-12-10','overig',0,'2025-12-10 10:58:08.344804',1),(376,'2025-12-10','overig',0,'2025-12-10 10:58:08.344804',5),(377,'2025-12-10','overig',0,'2025-12-10 10:58:08.344804',16),(378,'2025-12-10','overig',0,'2025-12-10 10:58:08.353628',27),(379,'2025-12-10','overig',0,'2025-12-10 10:58:08.353628',2),(380,'2025-12-10','overig',0,'2025-12-10 10:58:08.361679',23),(381,'2025-12-10','overig',0,'2025-12-10 10:58:08.361679',9),(382,'2025-12-10','overig',0,'2025-12-10 10:58:08.361679',17),(383,'2025-12-10','overig',0,'2025-12-10 10:58:08.361679',10),(384,'2025-12-10','overig',0,'2025-12-10 10:58:08.361679',14),(385,'2025-12-10','overig',0,'2025-12-10 10:58:08.378119',8),(386,'2025-12-11','overig',0,'2025-12-11 11:49:16.434740',21),(387,'2025-12-11','overig',0,'2025-12-11 11:49:16.444002',13),(388,'2025-12-11','overig',0,'2025-12-11 11:49:16.449424',24),(389,'2025-12-11','overig',0,'2025-12-11 11:49:16.449424',22),(390,'2025-12-11','overig',0,'2025-12-11 11:49:16.449424',28),(391,'2025-12-11','overig',0,'2025-12-11 11:49:16.449424',7),(392,'2025-12-11','overig',0,'2025-12-11 11:49:16.467559',19),(393,'2025-12-11','overig',0,'2025-12-11 11:49:16.470570',26),(394,'2025-12-11','overig',0,'2025-12-11 11:49:16.475588',20),(395,'2025-12-11','overig',0,'2025-12-11 11:49:16.479726',4),(396,'2025-12-11','overig',0,'2025-12-11 11:49:16.483193',6),(397,'2025-12-11','overig',0,'2025-12-11 11:49:16.487187',15),(398,'2025-12-11','overig',0,'2025-12-11 11:49:16.491190',3),(399,'2025-12-11','overig',0,'2025-12-11 11:49:16.495216',18),(400,'2025-12-11','overig',0,'2025-12-11 11:49:16.500333',12),(401,'2025-12-11','overig',0,'2025-12-11 11:49:16.500333',25),(402,'2025-12-11','overig',0,'2025-12-11 11:49:16.500333',11),(403,'2025-12-11','overig',0,'2025-12-11 11:49:16.515497',1),(404,'2025-12-11','overig',0,'2025-12-11 11:49:16.515497',5),(405,'2025-12-11','overig',0,'2025-12-11 11:49:16.515497',16),(406,'2025-12-11','overig',0,'2025-12-11 11:49:16.515497',27),(407,'2025-12-11','overig',0,'2025-12-11 11:49:16.531877',2),(408,'2025-12-11','overig',0,'2025-12-11 11:49:16.534823',23),(409,'2025-12-11','overig',0,'2025-12-11 11:49:16.538848',9),(410,'2025-12-11','overig',0,'2025-12-11 11:49:16.542881',17),(411,'2025-12-11','overig',0,'2025-12-11 11:49:16.548310',10),(412,'2025-12-11','overig',0,'2025-12-11 11:49:16.552910',14),(413,'2025-12-11','overig',0,'2025-12-11 11:49:16.556929',8),(414,'2025-12-12','overig',0,'2025-12-12 13:25:33.461530',21),(415,'2025-12-12','overig',0,'2025-12-12 13:25:33.511115',13),(416,'2025-12-12','overig',0,'2025-12-12 13:25:33.522774',24),(417,'2025-12-12','overig',0,'2025-12-12 13:25:33.527341',22),(418,'2025-12-12','overig',0,'2025-12-12 13:25:33.537429',28),(419,'2025-12-12','overig',0,'2025-12-12 13:25:33.539795',7),(420,'2025-12-12','overig',0,'2025-12-12 13:25:33.551773',19),(421,'2025-12-12','overig',0,'2025-12-12 13:25:33.560222',26),(422,'2025-12-12','overig',0,'2025-12-12 13:25:33.564511',20),(423,'2025-12-12','overig',0,'2025-12-12 13:25:33.573106',4),(424,'2025-12-12','overig',0,'2025-12-12 13:25:33.578180',6),(425,'2025-12-12','overig',0,'2025-12-12 13:25:33.585990',15),(426,'2025-12-12','overig',0,'2025-12-12 13:25:33.590581',3),(427,'2025-12-12','overig',0,'2025-12-12 13:25:33.595111',18),(428,'2025-12-12','overig',0,'2025-12-12 13:25:33.605522',12),(429,'2025-12-12','overig',0,'2025-12-12 13:25:33.610340',25),(430,'2025-12-12','overig',0,'2025-12-12 13:25:33.618405',11),(431,'2025-12-12','overig',0,'2025-12-12 13:25:33.622572',1),(432,'2025-12-12','overig',0,'2025-12-12 13:25:33.622572',5),(433,'2025-12-12','overig',0,'2025-12-12 13:25:33.639098',16),(434,'2025-12-12','overig',0,'2025-12-12 13:25:33.639098',27),(435,'2025-12-12','overig',0,'2025-12-12 13:25:33.652221',2),(436,'2025-12-12','overig',0,'2025-12-12 13:25:33.655686',23),(437,'2025-12-12','overig',0,'2025-12-12 13:25:33.655686',9),(438,'2025-12-12','overig',0,'2025-12-12 13:25:33.672113',17),(439,'2025-12-12','overig',0,'2025-12-12 13:25:33.672113',10),(440,'2025-12-12','overig',0,'2025-12-12 13:25:33.684299',14),(441,'2025-12-12','overig',0,'2025-12-12 13:25:33.690684',8),(442,'2025-12-13','training_aangepast',0,'2025-12-13 19:51:11.474317',21),(443,'2025-12-13','overig',0,'2025-12-13 14:41:22.388996',13),(444,'2025-12-13','overig',0,'2025-12-13 14:41:22.395999',24),(445,'2025-12-13','overig',0,'2025-12-13 14:41:22.402007',22),(446,'2025-12-13','overig',0,'2025-12-13 14:41:22.418527',28),(447,'2025-12-13','overig',0,'2025-12-13 14:41:22.425084',7),(448,'2025-12-13','overig',0,'2025-12-13 14:41:22.432068',19),(449,'2025-12-13','overig',0,'2025-12-13 14:41:22.445068',26),(450,'2025-12-13','overig',0,'2025-12-13 14:41:22.451069',20),(451,'2025-12-13','overig',0,'2025-12-13 14:41:22.457228',4),(452,'2025-12-13','overig',0,'2025-12-13 14:41:22.463226',6),(453,'2025-12-13','overig',0,'2025-12-13 14:41:22.470227',15),(454,'2025-12-13','overig',0,'2025-12-13 14:41:22.477225',3),(455,'2025-12-13','overig',0,'2025-12-13 14:41:22.483793',18),(456,'2025-12-13','overig',0,'2025-12-13 14:41:22.492125',12),(457,'2025-12-13','overig',0,'2025-12-13 14:41:22.499868',25),(458,'2025-12-13','overig',0,'2025-12-13 14:41:22.509032',11),(459,'2025-12-13','overig',0,'2025-12-13 14:41:22.516382',1),(460,'2025-12-13','overig',0,'2025-12-13 14:41:22.523419',5),(461,'2025-12-13','overig',0,'2025-12-13 14:41:22.530428',16),(462,'2025-12-13','overig',0,'2025-12-13 14:41:22.536427',27),(463,'2025-12-13','overig',0,'2025-12-13 14:41:22.542940',2),(464,'2025-12-13','overig',0,'2025-12-13 14:41:22.550275',23),(465,'2025-12-13','overig',0,'2025-12-13 14:41:22.556281',9),(466,'2025-12-13','overig',0,'2025-12-13 14:41:22.556281',17),(467,'2025-12-13','overig',0,'2025-12-13 14:41:22.568424',10),(468,'2025-12-13','overig',0,'2025-12-13 14:41:22.568424',14),(469,'2025-12-13','overig',0,'2025-12-13 14:41:22.568424',8),(470,'2025-12-15','overig',0,'2025-12-15 16:01:13.653048',21),(471,'2025-12-15','overig',0,'2025-12-15 16:01:13.661390',13),(472,'2025-12-15','overig',0,'2025-12-15 16:01:13.669776',24),(473,'2025-12-15','overig',0,'2025-12-15 16:01:13.677851',22),(474,'2025-12-15','overig',0,'2025-12-15 16:01:13.684349',28),(475,'2025-12-15','overig',0,'2025-12-15 16:01:13.691044',7),(476,'2025-12-15','overig',0,'2025-12-15 16:01:13.696476',19),(477,'2025-12-15','overig',0,'2025-12-15 16:01:13.703303',26),(478,'2025-12-15','overig',0,'2025-12-15 16:01:13.710850',20),(479,'2025-12-15','overig',0,'2025-12-15 16:01:13.717187',4),(480,'2025-12-15','overig',0,'2025-12-15 16:01:13.719278',6),(481,'2025-12-15','overig',0,'2025-12-15 16:01:13.719278',15),(482,'2025-12-15','overig',0,'2025-12-15 16:01:13.735477',3),(483,'2025-12-15','overig',0,'2025-12-15 16:01:13.742604',18),(484,'2025-12-15','overig',0,'2025-12-15 16:01:13.746644',12),(485,'2025-12-15','overig',0,'2025-12-15 16:01:13.753808',25),(486,'2025-12-15','overig',0,'2025-12-15 16:01:13.757230',11),(487,'2025-12-15','overig',0,'2025-12-15 16:01:13.766640',1),(488,'2025-12-15','overig',0,'2025-12-15 16:01:13.769941',5),(489,'2025-12-15','overig',0,'2025-12-15 16:01:13.769941',16),(490,'2025-12-15','overig',0,'2025-12-15 16:01:13.784365',27),(491,'2025-12-15','overig',0,'2025-12-15 16:01:13.786996',2),(492,'2025-12-15','overig',0,'2025-12-15 16:01:13.786996',23),(493,'2025-12-15','overig',0,'2025-12-15 16:01:13.798293',9),(494,'2025-12-15','overig',0,'2025-12-15 16:01:13.808260',17),(495,'2025-12-15','overig',0,'2025-12-15 16:01:13.814616',10),(496,'2025-12-15','overig',0,'2025-12-15 16:01:13.814616',14),(497,'2025-12-15','overig',0,'2025-12-15 16:01:13.822861',8),(498,'2025-12-17','overig',0,'2025-12-17 08:45:50.408012',21),(499,'2025-12-17','overig',0,'2025-12-17 08:45:50.429102',13),(500,'2025-12-17','overig',0,'2025-12-17 08:45:50.432100',24),(501,'2025-12-17','overig',0,'2025-12-17 08:45:50.435089',22),(502,'2025-12-17','overig',0,'2025-12-17 08:45:50.435784',28),(503,'2025-12-17','overig',0,'2025-12-17 08:45:50.435784',7),(504,'2025-12-17','overig',0,'2025-12-17 08:45:50.435784',19),(505,'2025-12-17','overig',0,'2025-12-17 08:45:50.435784',26),(506,'2025-12-17','overig',0,'2025-12-17 08:45:50.435784',20),(507,'2025-12-17','overig',0,'2025-12-17 08:45:50.451331',4),(508,'2025-12-17','overig',0,'2025-12-17 08:45:50.452025',6),(509,'2025-12-17','overig',0,'2025-12-17 08:45:50.452025',15),(510,'2025-12-17','overig',0,'2025-12-17 08:45:50.452025',3),(511,'2025-12-17','overig',0,'2025-12-17 08:45:50.452025',18),(512,'2025-12-17','overig',0,'2025-12-17 08:45:50.452025',12),(513,'2025-12-17','overig',0,'2025-12-17 08:45:50.467997',25),(514,'2025-12-17','overig',0,'2025-12-17 08:45:50.468801',11),(515,'2025-12-17','overig',0,'2025-12-17 08:45:50.468801',1),(516,'2025-12-17','overig',0,'2025-12-17 08:45:50.468801',5),(517,'2025-12-17','overig',0,'2025-12-17 08:45:50.468801',16),(518,'2025-12-17','overig',0,'2025-12-17 08:45:50.468801',27),(519,'2025-12-17','overig',0,'2025-12-17 08:45:50.468801',2),(520,'2025-12-17','overig',0,'2025-12-17 08:45:50.485351',23),(521,'2025-12-17','overig',0,'2025-12-17 08:45:50.485351',9),(522,'2025-12-17','overig',0,'2025-12-17 08:45:50.485351',17),(523,'2025-12-17','overig',0,'2025-12-17 08:45:50.485351',10),(524,'2025-12-17','overig',0,'2025-12-17 08:45:50.485351',14),(525,'2025-12-17','overig',0,'2025-12-17 08:45:50.485351',8),(526,'2025-12-18','overig',0,'2025-12-18 07:16:21.970733',21),(527,'2025-12-18','overig',0,'2025-12-18 07:16:21.977246',13),(528,'2025-12-18','overig',0,'2025-12-18 07:16:21.981246',24),(529,'2025-12-18','overig',0,'2025-12-18 07:16:21.985622',22),(530,'2025-12-18','overig',0,'2025-12-18 07:16:21.990529',28),(531,'2025-12-18','overig',0,'2025-12-18 07:16:21.994530',7),(532,'2025-12-18','overig',0,'2025-12-18 07:16:21.997554',19),(533,'2025-12-18','overig',0,'2025-12-18 07:16:22.000528',26),(534,'2025-12-18','overig',0,'2025-12-18 07:16:22.003767',20),(535,'2025-12-18','overig',0,'2025-12-18 07:16:22.006781',4),(536,'2025-12-18','overig',0,'2025-12-18 07:16:22.009784',6),(537,'2025-12-18','overig',0,'2025-12-18 07:16:22.013781',15),(538,'2025-12-18','overig',0,'2025-12-18 07:16:22.016793',3),(539,'2025-12-18','overig',0,'2025-12-18 07:16:22.019885',18),(540,'2025-12-18','overig',0,'2025-12-18 07:16:22.023439',12),(541,'2025-12-18','overig',0,'2025-12-18 07:16:22.026488',25),(542,'2025-12-18','overig',0,'2025-12-18 07:16:22.029489',11),(543,'2025-12-18','overig',0,'2025-12-18 07:16:22.031489',1),(544,'2025-12-18','overig',0,'2025-12-18 07:16:22.034493',5),(545,'2025-12-18','overig',0,'2025-12-18 07:16:22.038558',16),(546,'2025-12-18','overig',0,'2025-12-18 07:16:22.041581',27),(547,'2025-12-18','overig',0,'2025-12-18 07:16:22.043576',2),(548,'2025-12-18','overig',0,'2025-12-18 07:16:22.046596',23),(549,'2025-12-18','overig',0,'2025-12-18 07:16:22.049575',9),(550,'2025-12-18','overig',0,'2025-12-18 07:16:22.052267',17),(551,'2025-12-18','overig',0,'2025-12-18 07:16:22.054896',10),(552,'2025-12-18','overig',0,'2025-12-18 07:16:22.057957',14),(553,'2025-12-18','overig',0,'2025-12-18 07:16:22.060939',8),(554,'2026-01-20','overig',0,'2026-01-20 07:30:59.244670',21),(555,'2026-01-20','overig',0,'2026-01-20 07:30:49.009081',13),(556,'2026-01-20','overig',0,'2026-01-20 07:30:49.013098',24),(557,'2026-01-20','overig',0,'2026-01-20 07:30:49.016104',22),(558,'2026-01-20','overig',0,'2026-01-20 07:30:49.017532',28),(559,'2026-01-20','overig',0,'2026-01-20 07:30:49.023049',7),(560,'2026-01-20','overig',0,'2026-01-20 07:30:49.025473',19),(561,'2026-01-20','overig',0,'2026-01-20 07:30:49.033893',26),(562,'2026-01-20','overig',0,'2026-01-20 07:30:49.033893',20),(563,'2026-01-20','overig',0,'2026-01-20 07:30:49.040716',4),(564,'2026-01-20','overig',0,'2026-01-20 07:30:49.040716',6),(565,'2026-01-20','overig',0,'2026-01-20 07:30:49.046195',15),(566,'2026-01-20','overig',0,'2026-01-20 07:30:49.051739',3),(567,'2026-01-20','overig',0,'2026-01-20 07:30:49.056589',18),(568,'2026-01-20','overig',0,'2026-01-20 07:30:49.059437',12),(569,'2026-01-20','overig',0,'2026-01-20 07:30:49.062804',25),(570,'2026-01-20','overig',0,'2026-01-20 07:30:49.065803',11),(571,'2026-01-20','overig',0,'2026-01-20 07:30:49.069805',1),(572,'2026-01-20','overig',0,'2026-01-20 07:30:49.072804',5),(573,'2026-01-20','overig',0,'2026-01-20 07:30:49.074537',16),(574,'2026-01-20','overig',0,'2026-01-20 07:30:49.079249',27),(575,'2026-01-20','overig',0,'2026-01-20 07:30:49.082253',2),(576,'2026-01-20','overig',0,'2026-01-20 07:30:49.086387',23),(577,'2026-01-20','overig',0,'2026-01-20 07:30:49.090648',9),(578,'2026-01-20','overig',0,'2026-01-20 07:30:49.093077',17),(579,'2026-01-20','overig',0,'2026-01-20 07:30:49.093077',10),(580,'2026-01-20','overig',0,'2026-01-20 07:30:49.093077',14),(581,'2026-01-20','overig',0,'2026-01-20 07:30:49.093077',8),(582,'2026-01-26','overig',0,'2026-01-26 13:09:00.791988',21),(583,'2026-01-26','overig',0,'2026-01-26 13:09:00.804103',13),(584,'2026-01-26','overig',0,'2026-01-26 13:09:00.813319',24),(585,'2026-01-26','overig',0,'2026-01-26 13:09:00.820495',22),(586,'2026-01-26','overig',0,'2026-01-26 13:09:00.828607',28),(587,'2026-01-26','overig',0,'2026-01-26 13:09:00.828607',7),(588,'2026-01-26','overig',0,'2026-01-26 13:09:00.840753',19),(589,'2026-01-26','overig',0,'2026-01-26 13:09:00.844959',26),(590,'2026-01-26','overig',0,'2026-01-26 13:09:00.844959',20),(591,'2026-01-26','overig',0,'2026-01-26 13:09:00.859303',4),(592,'2026-01-26','overig',0,'2026-01-26 13:09:00.863616',6),(593,'2026-01-26','overig',0,'2026-01-26 13:09:00.870151',15),(594,'2026-01-26','overig',0,'2026-01-26 13:09:00.870802',3),(595,'2026-01-26','overig',0,'2026-01-26 13:09:00.878355',18),(596,'2026-01-26','overig',0,'2026-01-26 13:09:00.887682',12),(597,'2026-01-26','overig',0,'2026-01-26 13:09:00.894978',25),(598,'2026-01-26','overig',0,'2026-01-26 13:09:00.897041',11),(599,'2026-01-26','overig',0,'2026-01-26 13:09:00.903071',1),(600,'2026-01-26','overig',0,'2026-01-26 13:09:00.911162',5),(601,'2026-01-26','overig',0,'2026-01-26 13:09:00.920010',16),(602,'2026-01-26','overig',0,'2026-01-26 13:09:00.920650',27),(603,'2026-01-26','overig',0,'2026-01-26 13:09:00.927990',2),(604,'2026-01-26','overig',0,'2026-01-26 13:09:00.936712',23),(605,'2026-01-26','overig',0,'2026-01-26 13:09:00.943875',9),(606,'2026-01-26','overig',0,'2026-01-26 13:09:00.952075',17),(607,'2026-01-26','overig',0,'2026-01-26 13:09:00.953324',10),(608,'2026-01-26','overig',0,'2026-01-26 13:09:00.960139',14),(609,'2026-01-26','overig',0,'2026-01-26 13:09:00.968667',8),(610,'2026-02-06','overig',0,'2026-02-06 13:55:30.594075',21),(611,'2026-02-06','overig',0,'2026-02-06 13:55:30.605574',13),(612,'2026-02-06','overig',0,'2026-02-06 13:55:30.609784',24),(613,'2026-02-06','overig',0,'2026-02-06 13:55:30.612786',22),(614,'2026-02-06','overig',0,'2026-02-06 13:55:30.615234',28),(615,'2026-02-06','overig',0,'2026-02-06 13:55:30.617204',7),(616,'2026-02-06','overig',0,'2026-02-06 13:55:30.620530',19),(617,'2026-02-06','overig',0,'2026-02-06 13:55:30.623499',26),(618,'2026-02-06','overig',0,'2026-02-06 13:55:30.624111',20),(619,'2026-02-06','overig',0,'2026-02-06 13:55:30.624111',4),(620,'2026-02-06','overig',0,'2026-02-06 13:55:30.624111',6),(621,'2026-02-06','overig',0,'2026-02-06 13:55:30.624111',15),(622,'2026-02-06','overig',0,'2026-02-06 13:55:30.624111',3),(623,'2026-02-06','overig',0,'2026-02-06 13:55:30.624111',18),(624,'2026-02-06','overig',0,'2026-02-06 13:55:30.624111',12),(625,'2026-02-06','overig',0,'2026-02-06 13:55:30.640341',25),(626,'2026-02-06','overig',0,'2026-02-06 13:55:30.643226',11),(627,'2026-02-06','overig',0,'2026-02-06 13:55:30.645223',1),(628,'2026-02-06','overig',0,'2026-02-06 13:55:30.647245',5),(629,'2026-02-06','overig',0,'2026-02-06 13:55:30.649222',16),(630,'2026-02-06','overig',0,'2026-02-06 13:55:30.651244',27),(631,'2026-02-06','overig',0,'2026-02-06 13:55:30.653222',2),(632,'2026-02-06','overig',0,'2026-02-06 13:55:30.655245',23),(633,'2026-02-06','overig',0,'2026-02-06 13:55:30.657319',9),(634,'2026-02-06','overig',0,'2026-02-06 13:55:30.657319',17),(635,'2026-02-06','overig',0,'2026-02-06 13:55:30.657319',10),(636,'2026-02-06','overig',0,'2026-02-06 13:55:30.657319',14),(637,'2026-02-06','overig',0,'2026-02-06 13:55:30.657319',8),(638,'2026-02-07','overig',0,'2026-02-06 14:26:02.423308',21),(639,'2026-02-07','overig',0,'2026-02-06 14:26:02.425596',13),(640,'2026-02-07','overig',0,'2026-02-06 14:26:02.427615',24),(641,'2026-02-07','overig',0,'2026-02-06 14:26:02.429594',22),(642,'2026-02-07','overig',0,'2026-02-06 14:26:02.433258',28),(643,'2026-02-07','overig',0,'2026-02-06 14:26:02.436411',7),(644,'2026-02-07','overig',0,'2026-02-06 14:26:02.438603',19),(645,'2026-02-07','overig',0,'2026-02-06 14:26:02.440963',26),(646,'2026-02-07','overig',0,'2026-02-06 14:26:02.443071',20),(647,'2026-02-07','overig',0,'2026-02-06 14:26:02.445047',4),(648,'2026-02-07','overig',0,'2026-02-06 14:26:02.447047',6),(649,'2026-02-07','overig',0,'2026-02-06 14:26:02.449051',15),(650,'2026-02-07','overig',0,'2026-02-06 14:26:02.452063',3),(651,'2026-02-07','overig',0,'2026-02-06 14:26:02.454047',18),(652,'2026-02-07','overig',0,'2026-02-06 14:26:02.456069',12),(653,'2026-02-07','overig',0,'2026-02-06 14:26:02.458064',25),(654,'2026-02-07','overig',0,'2026-02-06 14:26:02.460541',11),(655,'2026-02-07','overig',0,'2026-02-06 14:26:02.463012',1),(656,'2026-02-07','overig',0,'2026-02-06 14:26:02.466442',5),(657,'2026-02-07','overig',0,'2026-02-06 14:26:02.468444',16),(658,'2026-02-07','overig',0,'2026-02-06 14:26:02.471439',27),(659,'2026-02-07','overig',0,'2026-02-06 14:26:02.473440',2),(660,'2026-02-07','overig',0,'2026-02-06 14:26:02.475444',23),(661,'2026-02-07','overig',0,'2026-02-06 14:26:02.478341',9),(662,'2026-02-07','overig',0,'2026-02-06 14:26:02.480362',17),(663,'2026-02-07','overig',0,'2026-02-06 14:26:02.483366',10),(664,'2026-02-07','overig',0,'2026-02-06 14:26:02.485358',14),(665,'2026-02-07','overig',0,'2026-02-06 14:26:02.487356',8),(666,'2026-02-12','overig',0,'2026-02-12 10:29:56.097723',21),(667,'2026-02-12','overig',0,'2026-02-12 10:29:56.114276',13),(668,'2026-02-12','overig',0,'2026-02-12 10:29:56.122632',24),(669,'2026-02-12','overig',0,'2026-02-12 10:29:56.122632',22),(670,'2026-02-12','overig',0,'2026-02-12 10:29:56.132713',28),(671,'2026-02-12','overig',0,'2026-02-12 10:29:56.141574',7),(672,'2026-02-12','overig',0,'2026-02-12 10:29:56.147227',19),(673,'2026-02-12','overig',0,'2026-02-12 10:29:56.156284',26),(674,'2026-02-12','overig',0,'2026-02-12 10:29:56.163024',20),(675,'2026-02-12','overig',0,'2026-02-12 10:29:56.163024',4),(676,'2026-02-12','overig',0,'2026-02-12 10:29:56.174368',6),(677,'2026-02-12','overig',0,'2026-02-12 10:29:56.179590',15),(678,'2026-02-12','overig',0,'2026-02-12 10:29:56.187963',3),(679,'2026-02-12','overig',0,'2026-02-12 10:29:56.195888',18),(680,'2026-02-12','overig',0,'2026-02-12 10:29:56.195888',12),(681,'2026-02-12','overig',0,'2026-02-12 10:29:56.206037',25),(682,'2026-02-12','overig',0,'2026-02-12 10:29:56.212020',11),(683,'2026-02-12','overig',0,'2026-02-12 10:29:56.221708',1),(684,'2026-02-12','overig',0,'2026-02-12 10:29:56.228127',5),(685,'2026-02-12','overig',0,'2026-02-12 10:29:56.228127',16),(686,'2026-02-12','overig',0,'2026-02-12 10:29:56.244355',27),(687,'2026-02-12','overig',0,'2026-02-12 10:29:56.252188',2),(688,'2026-02-12','overig',0,'2026-02-12 10:29:56.253210',23),(689,'2026-02-12','overig',0,'2026-02-12 10:29:56.260276',9),(690,'2026-02-12','overig',0,'2026-02-12 10:29:56.268392',17),(691,'2026-02-12','overig',0,'2026-02-12 10:29:56.271354',10),(692,'2026-02-12','overig',0,'2026-02-12 10:29:56.271354',14),(693,'2026-02-12','overig',0,'2026-02-12 10:29:56.286951',8),(694,'2026-02-18','overig',0,'2026-02-18 07:34:21.776348',21),(695,'2026-02-18','overig',0,'2026-02-18 07:34:21.787398',13),(696,'2026-02-18','overig',0,'2026-02-18 07:34:21.796398',24),(697,'2026-02-18','overig',0,'2026-02-18 07:34:21.803412',22),(698,'2026-02-18','overig',0,'2026-02-18 07:34:21.811157',28),(699,'2026-02-18','overig',0,'2026-02-18 07:34:21.818123',7),(700,'2026-02-18','overig',0,'2026-02-18 07:34:21.824386',19),(701,'2026-02-18','overig',0,'2026-02-18 07:34:21.832264',26),(702,'2026-02-18','overig',0,'2026-02-18 07:34:21.838885',20),(703,'2026-02-18','overig',0,'2026-02-18 07:34:21.845851',4),(704,'2026-02-18','overig',0,'2026-02-18 07:34:21.852998',6),(705,'2026-02-18','overig',0,'2026-02-18 07:34:21.859994',15),(706,'2026-02-18','overig',0,'2026-02-18 07:34:21.867011',3),(707,'2026-02-18','overig',0,'2026-02-18 07:34:21.874126',18),(708,'2026-02-18','overig',0,'2026-02-18 07:34:21.880454',12),(709,'2026-02-18','overig',0,'2026-02-18 07:34:21.886993',25),(710,'2026-02-18','overig',0,'2026-02-18 07:34:21.895910',11),(711,'2026-02-18','overig',0,'2026-02-18 07:34:21.903253',1),(712,'2026-02-18','overig',0,'2026-02-18 07:34:21.911159',5),(713,'2026-02-18','overig',0,'2026-02-18 07:34:21.918027',16),(714,'2026-02-18','overig',0,'2026-02-18 07:34:21.924355',27),(715,'2026-02-18','overig',0,'2026-02-18 07:34:21.933048',2),(716,'2026-02-18','overig',0,'2026-02-18 07:34:21.939561',23),(717,'2026-02-18','overig',0,'2026-02-18 07:34:21.948181',9),(718,'2026-02-18','overig',0,'2026-02-18 07:34:21.955192',17),(719,'2026-02-18','overig',0,'2026-02-18 07:34:21.961697',10),(720,'2026-02-18','overig',0,'2026-02-18 07:34:21.967605',14),(721,'2026-02-18','overig',0,'2026-02-18 07:34:21.975487',8);
/*!40000 ALTER TABLE `main_aanwezigheid` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_anthropometrymeasurement`
--

DROP TABLE IF EXISTS `main_anthropometrymeasurement`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_anthropometrymeasurement` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `category` varchar(20) NOT NULL,
  `site_code` varchar(50) NOT NULL,
  `repetition` smallint unsigned NOT NULL,
  `value` double NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `session_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_anthro_measurement_per_rep` (`session_id`,`category`,`site_code`,`repetition`),
  KEY `main_anthro_categor_c3426b_idx` (`category`,`site_code`),
  CONSTRAINT `main_anthropometryme_session_id_02685e41_fk_main_anth` FOREIGN KEY (`session_id`) REFERENCES `main_anthropometrysession` (`id`),
  CONSTRAINT `main_anthropometrymeasurement_chk_1` CHECK ((`repetition` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=151 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_anthropometrymeasurement`
--

LOCK TABLES `main_anthropometrymeasurement` WRITE;
/*!40000 ALTER TABLE `main_anthropometrymeasurement` DISABLE KEYS */;
INSERT INTO `main_anthropometrymeasurement` VALUES (1,'skinfold','triceps',1,7.4,'2026-02-18 11:00:27.962665',1),(2,'skinfold','triceps',2,7.4,'2026-02-18 11:00:27.963905',1),(3,'skinfold','biceps',1,4,'2026-02-18 11:00:27.964921',1),(4,'skinfold','biceps',2,3.2,'2026-02-18 11:00:27.964921',1),(5,'skinfold','biceps',3,4,'2026-02-18 11:00:27.966413',1),(6,'skinfold','subscapular',1,11.2,'2026-02-18 11:00:27.967432',1),(7,'skinfold','subscapular',2,11.2,'2026-02-18 11:00:27.967432',1),(8,'skinfold','iliac_crest',1,11.8,'2026-02-18 11:00:27.968442',1),(9,'skinfold','iliac_crest',2,11.3,'2026-02-18 11:00:27.969431',1),(10,'skinfold','supraspinale',1,6.2,'2026-02-18 11:00:27.969431',1),(11,'skinfold','supraspinale',2,7.2,'2026-02-18 11:00:27.970428',1),(12,'skinfold','supraspinale',3,7.2,'2026-02-18 11:00:27.971433',1),(13,'skinfold','abdominal',1,14.2,'2026-02-18 11:00:27.971433',1),(14,'skinfold','abdominal',2,15,'2026-02-18 11:00:27.972433',1),(15,'skinfold','abdominal',3,15.2,'2026-02-18 11:00:27.972433',1),(16,'skinfold','thigh',1,12.2,'2026-02-18 11:00:27.973430',1),(17,'skinfold','thigh',2,12.2,'2026-02-18 11:00:27.973430',1),(18,'skinfold','calf',1,6.6,'2026-02-18 11:00:27.974429',1),(19,'skinfold','calf',2,6,'2026-02-18 11:00:27.974429',1),(20,'skinfold','calf',3,6.3,'2026-02-18 11:00:27.975429',1),(21,'skinfold','triceps',1,8,'2026-02-18 11:00:27.981784',2),(22,'skinfold','triceps',2,8,'2026-02-18 11:00:27.981784',2),(23,'skinfold','biceps',1,8,'2026-02-18 11:00:27.982784',2),(24,'skinfold','biceps',2,8,'2026-02-18 11:00:27.982784',2),(25,'skinfold','subscapular',1,8,'2026-02-18 11:00:27.983782',2),(26,'skinfold','subscapular',2,8,'2026-02-18 11:00:27.984782',2),(27,'skinfold','iliac_crest',1,8,'2026-02-18 11:00:27.984782',2),(28,'skinfold','iliac_crest',2,8,'2026-02-18 11:00:27.985786',2),(29,'skinfold','supraspinale',1,8,'2026-02-18 11:00:27.985786',2),(30,'skinfold','supraspinale',2,8,'2026-02-18 11:00:27.986783',2),(31,'skinfold','abdominal',1,8,'2026-02-18 11:00:27.986783',2),(32,'skinfold','abdominal',2,8,'2026-02-18 11:00:27.987783',2),(33,'skinfold','thigh',1,8,'2026-02-18 11:00:27.987783',2),(34,'skinfold','thigh',2,8,'2026-02-18 11:00:27.988783',2),(35,'skinfold','calf',1,8,'2026-02-18 11:00:27.988783',2),(36,'skinfold','calf',2,8,'2026-02-18 11:00:27.989784',2),(37,'skinfold','triceps',1,8,'2026-02-18 11:00:27.993789',3),(38,'skinfold','triceps',2,8,'2026-02-18 11:00:27.995239',3),(39,'skinfold','biceps',1,9,'2026-02-18 11:00:27.996251',3),(40,'skinfold','biceps',2,9,'2026-02-18 11:00:27.997252',3),(41,'skinfold','subscapular',1,8,'2026-02-18 11:00:27.997252',3),(42,'skinfold','subscapular',2,8,'2026-02-18 11:00:27.998252',3),(43,'skinfold','iliac_crest',1,9,'2026-02-18 11:00:27.998252',3),(44,'skinfold','iliac_crest',2,9,'2026-02-18 11:00:27.999252',3),(45,'skinfold','supraspinale',1,9,'2026-02-18 11:00:27.999252',3),(46,'skinfold','supraspinale',2,9,'2026-02-18 11:00:28.000251',3),(47,'skinfold','abdominal',1,9,'2026-02-18 11:00:28.001251',3),(48,'skinfold','abdominal',2,9,'2026-02-18 11:00:28.001251',3),(49,'skinfold','thigh',1,9,'2026-02-18 11:00:28.002251',3),(50,'skinfold','thigh',2,9,'2026-02-18 11:00:28.003252',3),(51,'skinfold','calf',1,9,'2026-02-18 11:00:28.003252',3),(52,'skinfold','calf',2,9,'2026-02-18 11:00:28.004251',3),(53,'skinfold','triceps',1,8,'2026-02-18 11:00:28.009255',4),(54,'skinfold','triceps',2,8,'2026-02-18 11:00:28.009255',4),(55,'skinfold','biceps',1,8,'2026-02-18 11:00:28.010252',4),(56,'skinfold','biceps',2,8,'2026-02-18 11:00:28.011251',4),(57,'skinfold','subscapular',1,8,'2026-02-18 11:00:28.012254',4),(58,'skinfold','subscapular',2,8,'2026-02-18 11:00:28.012763',4),(59,'skinfold','iliac_crest',1,9,'2026-02-18 11:00:28.012763',4),(60,'skinfold','iliac_crest',2,9,'2026-02-18 11:00:28.013775',4),(61,'skinfold','supraspinale',1,6,'2026-02-18 11:00:28.013775',4),(62,'skinfold','supraspinale',2,6,'2026-02-18 11:00:28.014776',4),(63,'skinfold','abdominal',1,6,'2026-02-18 11:00:28.015783',4),(64,'skinfold','abdominal',2,6,'2026-02-18 11:00:28.015783',4),(65,'skinfold','thigh',1,6,'2026-02-18 11:00:28.016776',4),(66,'skinfold','thigh',2,6,'2026-02-18 11:00:28.016776',4),(67,'skinfold','calf',1,6,'2026-02-18 11:00:28.017776',4),(68,'skinfold','calf',2,6,'2026-02-18 11:00:28.017776',4),(69,'skinfold','triceps',1,9,'2026-02-18 11:00:28.022774',5),(70,'skinfold','triceps',2,9,'2026-02-18 11:00:28.023780',5),(71,'skinfold','biceps',1,6,'2026-02-18 11:00:28.023780',5),(72,'skinfold','biceps',2,6,'2026-02-18 11:00:28.024775',5),(73,'skinfold','subscapular',1,2,'2026-02-18 11:00:28.025977',5),(74,'skinfold','subscapular',2,2,'2026-02-18 11:00:28.025977',5),(75,'skinfold','iliac_crest',1,6,'2026-02-18 11:00:28.026984',5),(76,'skinfold','iliac_crest',2,6,'2026-02-18 11:00:28.027986',5),(77,'skinfold','supraspinale',1,6,'2026-02-18 11:00:28.027986',5),(78,'skinfold','supraspinale',2,6,'2026-02-18 11:00:28.028986',5),(79,'skinfold','abdominal',1,6,'2026-02-18 11:00:28.028986',5),(80,'skinfold','abdominal',2,6,'2026-02-18 11:00:28.029989',5),(81,'skinfold','thigh',1,6,'2026-02-18 11:00:28.030986',5),(82,'skinfold','thigh',2,6,'2026-02-18 11:00:28.031985',5),(83,'skinfold','calf',1,6,'2026-02-18 11:00:28.032986',5),(84,'skinfold','calf',2,6,'2026-02-18 11:00:28.032986',5),(85,'skinfold','triceps',1,8,'2026-02-18 11:00:28.037113',6),(86,'skinfold','triceps',2,8,'2026-02-18 11:00:28.037113',6),(87,'skinfold','biceps',1,10,'2026-02-18 11:00:28.037113',6),(88,'skinfold','biceps',2,10,'2026-02-18 11:00:28.041949',6),(89,'skinfold','subscapular',1,8,'2026-02-18 11:00:28.041949',6),(90,'skinfold','subscapular',2,8,'2026-02-18 11:00:28.041949',6),(91,'skinfold','iliac_crest',1,10,'2026-02-18 11:00:28.041949',6),(92,'skinfold','iliac_crest',2,10,'2026-02-18 11:00:28.043968',6),(93,'skinfold','supraspinale',1,10,'2026-02-18 11:00:28.044708',6),(94,'skinfold','supraspinale',2,10,'2026-02-18 11:00:28.044708',6),(95,'skinfold','abdominal',1,10,'2026-02-18 11:00:28.045727',6),(96,'skinfold','abdominal',2,10,'2026-02-18 11:00:28.046728',6),(97,'skinfold','thigh',1,10,'2026-02-18 11:00:28.046728',6),(98,'skinfold','thigh',2,10,'2026-02-18 11:00:28.047729',6),(99,'skinfold','calf',1,10,'2026-02-18 11:00:28.047729',6),(100,'skinfold','calf',2,10,'2026-02-18 11:00:28.048728',6),(101,'skinfold','triceps',1,9,'2026-02-18 11:00:28.053099',7),(102,'skinfold','triceps',2,9,'2026-02-18 11:00:28.054099',7),(103,'skinfold','biceps',1,8,'2026-02-18 11:00:28.054099',7),(104,'skinfold','biceps',2,9,'2026-02-18 11:00:28.055604',7),(105,'skinfold','biceps',3,9,'2026-02-18 11:00:28.055604',7),(106,'skinfold','subscapular',1,9,'2026-02-18 11:00:28.056610',7),(107,'skinfold','subscapular',2,9,'2026-02-18 11:00:28.056610',7),(108,'skinfold','iliac_crest',1,9,'2026-02-18 11:00:28.057610',7),(109,'skinfold','iliac_crest',2,9,'2026-02-18 11:00:28.057610',7),(110,'skinfold','supraspinale',1,6,'2026-02-18 11:00:28.058610',7),(111,'skinfold','supraspinale',2,6,'2026-02-18 11:00:28.058610',7),(112,'skinfold','abdominal',1,6,'2026-02-18 11:00:28.059610',7),(113,'skinfold','abdominal',2,6,'2026-02-18 11:00:28.059610',7),(114,'skinfold','thigh',1,6,'2026-02-18 11:00:28.060614',7),(115,'skinfold','thigh',2,6,'2026-02-18 11:00:28.060614',7),(116,'skinfold','calf',1,6,'2026-02-18 11:00:28.061727',7),(117,'skinfold','calf',2,6,'2026-02-18 11:00:28.062816',7),(118,'skinfold','triceps',1,6.8,'2026-02-18 11:00:28.066822',8),(119,'skinfold','triceps',2,7,'2026-02-18 11:00:28.066822',8),(120,'skinfold','biceps',1,3.3,'2026-02-18 11:00:28.067814',8),(121,'skinfold','biceps',2,3.2,'2026-02-18 11:00:28.068813',8),(122,'skinfold','subscapular',1,7.8,'2026-02-18 11:00:28.068813',8),(123,'skinfold','subscapular',2,8,'2026-02-18 11:00:28.069827',8),(124,'skinfold','iliac_crest',1,8.2,'2026-02-18 11:00:28.069827',8),(125,'skinfold','iliac_crest',2,8.8,'2026-02-18 11:00:28.070817',8),(126,'skinfold','iliac_crest',3,8.6,'2026-02-18 11:00:28.070817',8),(127,'skinfold','supraspinale',1,5.8,'2026-02-18 11:00:28.071818',8),(128,'skinfold','supraspinale',2,6,'2026-02-18 11:00:28.071818',8),(129,'skinfold','abdominal',1,9,'2026-02-18 11:00:28.072816',8),(130,'skinfold','abdominal',2,8.8,'2026-02-18 11:00:28.072816',8),(131,'skinfold','thigh',1,8.6,'2026-02-18 11:00:28.072816',8),(132,'skinfold','thigh',2,9,'2026-02-18 11:00:28.074814',8),(133,'skinfold','calf',1,4,'2026-02-18 11:00:28.075816',8),(134,'skinfold','calf',2,4,'2026-02-18 11:00:28.075816',8),(135,'skinfold','triceps',1,9,'2026-02-18 11:05:20.782076',9),(136,'skinfold','triceps',2,9,'2026-02-18 11:05:20.782076',9),(137,'skinfold','biceps',1,9,'2026-02-18 11:05:20.782076',9),(138,'skinfold','biceps',2,9,'2026-02-18 11:05:20.790387',9),(139,'skinfold','subscapular',1,9,'2026-02-18 11:05:20.792400',9),(140,'skinfold','subscapular',2,9,'2026-02-18 11:05:20.794412',9),(141,'skinfold','iliac_crest',1,9,'2026-02-18 11:05:20.795790',9),(142,'skinfold','iliac_crest',2,9,'2026-02-18 11:05:20.798720',9),(143,'skinfold','supraspinale',1,9,'2026-02-18 11:05:20.798720',9),(144,'skinfold','supraspinale',2,9,'2026-02-18 11:05:20.798720',9),(145,'skinfold','abdominal',1,9,'2026-02-18 11:05:20.798720',9),(146,'skinfold','abdominal',2,9,'2026-02-18 11:05:20.798720',9),(147,'skinfold','thigh',1,9,'2026-02-18 11:05:20.798720',9),(148,'skinfold','thigh',2,9,'2026-02-18 11:05:20.798720',9),(149,'skinfold','calf',1,9,'2026-02-18 11:05:20.814424',9),(150,'skinfold','calf',2,9,'2026-02-18 11:05:20.815209',9);
/*!40000 ALTER TABLE `main_anthropometrymeasurement` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_anthropometrysession`
--

DROP TABLE IF EXISTS `main_anthropometrysession`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_anthropometrysession` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `body_mass` double DEFAULT NULL,
  `length` double DEFAULT NULL,
  `fat_dw` double DEFAULT NULL,
  `fat_faulkner` double DEFAULT NULL,
  `fat_carter` double DEFAULT NULL,
  `fat_average` double DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `player_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_anthro_session_player_date` (`player_id`,`date`),
  CONSTRAINT `main_anthropometrysession_player_id_95e307a5_fk_main_player_id` FOREIGN KEY (`player_id`) REFERENCES `main_player` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_anthropometrysession`
--

LOCK TABLES `main_anthropometrysession` WRITE;
/*!40000 ALTER TABLE `main_anthropometrysession` DISABLE KEYS */;
INSERT INTO `main_anthropometrysession` VALUES (1,'2025-12-17',86.6,NULL,NULL,NULL,NULL,NULL,'2026-02-18 11:00:27.959311','2026-02-18 11:00:27.959311',12),(2,'2025-12-17',65,NULL,NULL,NULL,NULL,NULL,'2026-02-18 11:00:27.979311','2026-02-18 11:00:27.979311',21),(3,'2025-12-17',NULL,NULL,NULL,NULL,NULL,NULL,'2026-02-18 11:00:27.992785','2026-02-18 11:00:27.992785',13),(4,'2025-12-17',89,NULL,NULL,NULL,NULL,NULL,'2026-02-18 11:00:28.007251','2026-02-18 11:00:28.007251',28),(5,'2026-01-26',80,NULL,9.6,9.3,7.5,8.8,'2026-02-18 11:00:28.020776','2026-02-18 11:00:28.020776',18),(6,'2026-01-31',NULL,NULL,14.9,11.3,10.6,12.3,'2026-02-18 11:00:28.037113','2026-02-18 11:00:28.037113',18),(7,'2026-02-14',90,190,14.6,10.4,8.9,11.3,'2026-02-18 11:00:28.052103','2026-02-18 11:00:28.052103',18),(8,'2026-01-19',76,NULL,11.1,10.3,8.3,9.9,'2026-02-18 11:00:28.064821','2026-02-18 11:00:28.064821',20),(9,'2026-02-18',80,180,14.9,11.3,10.2,12.1,'2026-02-18 11:05:20.775821','2026-02-18 11:05:20.775821',19);
/*!40000 ALTER TABLE `main_anthropometrysession` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_antropometry`
--

DROP TABLE IF EXISTS `main_antropometry`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_antropometry` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `body_mass` double DEFAULT NULL,
  `length` double DEFAULT NULL,
  `triceps_m1` double DEFAULT NULL,
  `triceps_m2` double DEFAULT NULL,
  `triceps_m3` double DEFAULT NULL,
  `biceps_m1` double DEFAULT NULL,
  `biceps_m2` double DEFAULT NULL,
  `biceps_m3` double DEFAULT NULL,
  `subscapular_m1` double DEFAULT NULL,
  `subscapular_m2` double DEFAULT NULL,
  `subscapular_m3` double DEFAULT NULL,
  `iliac_crest_m1` double DEFAULT NULL,
  `iliac_crest_m2` double DEFAULT NULL,
  `iliac_crest_m3` double DEFAULT NULL,
  `supraspinale_m1` double DEFAULT NULL,
  `supraspinale_m2` double DEFAULT NULL,
  `supraspinale_m3` double DEFAULT NULL,
  `abdominal_m1` double DEFAULT NULL,
  `abdominal_m2` double DEFAULT NULL,
  `abdominal_m3` double DEFAULT NULL,
  `thigh_m1` double DEFAULT NULL,
  `thigh_m2` double DEFAULT NULL,
  `thigh_m3` double DEFAULT NULL,
  `calf_m1` double DEFAULT NULL,
  `calf_m2` double DEFAULT NULL,
  `calf_m3` double DEFAULT NULL,
  `arm_relaxed_m1` double DEFAULT NULL,
  `arm_relaxed_m2` double DEFAULT NULL,
  `arm_relaxed_m3` double DEFAULT NULL,
  `arm_flexed_m1` double DEFAULT NULL,
  `arm_flexed_m2` double DEFAULT NULL,
  `arm_flexed_m3` double DEFAULT NULL,
  `thigh_girth_m1` double DEFAULT NULL,
  `thigh_girth_m2` double DEFAULT NULL,
  `thigh_girth_m3` double DEFAULT NULL,
  `calf_girth_m1` double DEFAULT NULL,
  `calf_girth_m2` double DEFAULT NULL,
  `calf_girth_m3` double DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `player_id` bigint NOT NULL,
  `fat_average` double DEFAULT NULL,
  `fat_carter` double DEFAULT NULL,
  `fat_dw` double DEFAULT NULL,
  `fat_faulkner` double DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `main_antropometry_player_id_date_d6f0ba3b_uniq` (`player_id`,`date`),
  CONSTRAINT `main_antropometry_player_id_ecbaffc8_fk_main_player_id` FOREIGN KEY (`player_id`) REFERENCES `main_player` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_antropometry`
--

LOCK TABLES `main_antropometry` WRITE;
/*!40000 ALTER TABLE `main_antropometry` DISABLE KEYS */;
INSERT INTO `main_antropometry` VALUES (1,'2025-12-17',86.6,NULL,7.4,7.4,NULL,4,3.2,4,11.2,11.2,NULL,11.8,11.3,NULL,6.2,7.2,7.2,14.2,15,15.2,12.2,12.2,NULL,6.6,6,6.3,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2025-12-17 09:32:53.959923',12,NULL,NULL,NULL,NULL),(2,'2025-12-17',65,NULL,8,8,NULL,8,8,NULL,8,8,NULL,8,8,NULL,8,8,NULL,8,8,NULL,8,8,NULL,8,8,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2025-12-17 10:19:41.552230',21,NULL,NULL,NULL,NULL),(3,'2025-12-17',NULL,NULL,8,8,NULL,9,9,NULL,8,8,NULL,9,9,NULL,9,9,NULL,9,9,NULL,9,9,NULL,9,9,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2025-12-17 15:01:03.658744',13,NULL,NULL,NULL,NULL),(4,'2025-12-17',89,NULL,8,8,NULL,8,8,NULL,8,8,NULL,9,9,NULL,6,6,NULL,6,6,NULL,6,6,NULL,6,6,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2025-12-17 19:09:46.724770',28,NULL,NULL,NULL,NULL),(5,'2026-01-26',80,NULL,9,9,NULL,6,6,NULL,2,2,NULL,6,6,NULL,6,6,NULL,6,6,NULL,6,6,NULL,6,6,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-01-26 18:45:42.102711',18,8.8,7.5,9.6,9.3),(6,'2026-01-31',NULL,NULL,8,8,NULL,10,10,NULL,8,8,NULL,10,10,NULL,10,10,NULL,10,10,NULL,10,10,NULL,10,10,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-01-26 18:57:50.154778',18,12.3,10.6,14.9,11.3),(7,'2026-02-14',90,190,9,9,NULL,8,9,9,9,9,NULL,9,9,NULL,6,6,NULL,6,6,NULL,6,6,NULL,6,6,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-01-27 05:42:16.610247',18,11.3,8.9,14.6,10.4),(8,'2026-01-19',76,NULL,6.8,7,NULL,3.3,3.2,NULL,7.8,8,NULL,8.2,8.8,8.6,5.8,6,NULL,9,8.8,NULL,8.6,9,NULL,4,4,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-02-11 11:55:34.581814',20,9.9,8.3,11.1,10.3),(9,'2026-02-18',80,180,9,9,NULL,9,9,NULL,9,9,NULL,9,9,NULL,9,9,NULL,9,9,NULL,9,9,NULL,9,9,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-02-18 11:05:20.769636',19,12.1,10.2,14.9,11.3);
/*!40000 ALTER TABLE `main_antropometry` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_birthday`
--

DROP TABLE IF EXISTS `main_birthday`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_birthday` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `role` varchar(20) DEFAULT NULL,
  `date` date NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_birthday`
--

LOCK TABLES `main_birthday` WRITE;
/*!40000 ALTER TABLE `main_birthday` DISABLE KEYS */;
/*!40000 ALTER TABLE `main_birthday` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_birthdayprofile`
--

DROP TABLE IF EXISTS `main_birthdayprofile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_birthdayprofile` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `role` varchar(20) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_birthday_profile_name_role` (`name`,`role`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_birthdayprofile`
--

LOCK TABLES `main_birthdayprofile` WRITE;
/*!40000 ALTER TABLE `main_birthdayprofile` DISABLE KEYS */;
/*!40000 ALTER TABLE `main_birthdayprofile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_birthdayrecord`
--

DROP TABLE IF EXISTS `main_birthdayrecord`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_birthdayrecord` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `profile_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_birthday_profile_date` (`profile_id`,`date`),
  CONSTRAINT `main_birthdayrecord_profile_id_b8656fe6_fk_main_birt` FOREIGN KEY (`profile_id`) REFERENCES `main_birthdayprofile` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_birthdayrecord`
--

LOCK TABLES `main_birthdayrecord` WRITE;
/*!40000 ALTER TABLE `main_birthdayrecord` DISABLE KEYS */;
/*!40000 ALTER TABLE `main_birthdayrecord` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_dailyprogram`
--

DROP TABLE IF EXISTS `main_dailyprogram`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_dailyprogram` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `program_text` longtext,
  `player_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `main_dailyprogram_player_id_date_6e4ed151_uniq` (`player_id`,`date`),
  CONSTRAINT `main_dailyprogram_player_id_4f3f0824_fk_main_player_id` FOREIGN KEY (`player_id`) REFERENCES `main_player` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_dailyprogram`
--

LOCK TABLES `main_dailyprogram` WRITE;
/*!40000 ALTER TABLE `main_dailyprogram` DISABLE KEYS */;
INSERT INTO `main_dailyprogram` VALUES (1,'2025-11-21',NULL,21),(2,'2025-11-21','Werken aan schouder',28),(3,'2025-11-21',NULL,9),(4,'2025-11-21',NULL,6),(5,'2025-11-21',NULL,13),(6,'2025-11-21',NULL,24),(7,'2025-11-22',NULL,23),(8,'2025-11-22',NULL,21),(9,'2025-11-24',NULL,21),(10,'2025-11-25',NULL,7),(11,'2025-11-26',NULL,21),(12,'2025-11-28',NULL,21),(14,'2025-12-02',NULL,21),(15,'2025-12-06',NULL,21),(16,'2025-12-12',NULL,22),(17,'2025-12-13',NULL,21),(18,'2025-12-18',NULL,21),(19,'2026-02-06',NULL,23),(20,'2026-02-12',NULL,23);
/*!40000 ALTER TABLE `main_dailyprogram` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_dayprogram`
--

DROP TABLE IF EXISTS `main_dayprogram`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_dayprogram` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `date` varchar(100) NOT NULL,
  `activities` longtext NOT NULL,
  `notes` longtext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_dayprogram`
--

LOCK TABLES `main_dayprogram` WRITE;
/*!40000 ALTER TABLE `main_dayprogram` DISABLE KEYS */;
/*!40000 ALTER TABLE `main_dayprogram` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_dayprogramentry`
--

DROP TABLE IF EXISTS `main_dayprogramentry`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_dayprogramentry` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `title` varchar(120) DEFAULT NULL,
  `activities` longtext,
  `notes` longtext,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_dayprogram_date_title` (`date`,`title`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_dayprogramentry`
--

LOCK TABLES `main_dayprogramentry` WRITE;
/*!40000 ALTER TABLE `main_dayprogramentry` DISABLE KEYS */;
/*!40000 ALTER TABLE `main_dayprogramentry` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_fieldrehabsession`
--

DROP TABLE IF EXISTS `main_fieldrehabsession`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_fieldrehabsession` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `phase` varchar(50) NOT NULL,
  `onderdeel` varchar(100) NOT NULL,
  `afgevinkt` tinyint(1) NOT NULL,
  `duur` int unsigned DEFAULT NULL,
  `rpe` int unsigned DEFAULT NULL,
  `totale_afstand` int unsigned DEFAULT NULL,
  `afstand_20` int unsigned DEFAULT NULL,
  `afstand_25` int unsigned DEFAULT NULL,
  `acceleraties` int unsigned DEFAULT NULL,
  `deceleraties` int unsigned DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `player_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `main_fieldrehabsession_player_id_a4093375_fk_main_player_id` (`player_id`),
  CONSTRAINT `main_fieldrehabsession_player_id_a4093375_fk_main_player_id` FOREIGN KEY (`player_id`) REFERENCES `main_player` (`id`),
  CONSTRAINT `main_fieldrehabsession_chk_1` CHECK ((`duur` >= 0)),
  CONSTRAINT `main_fieldrehabsession_chk_2` CHECK ((`rpe` >= 0)),
  CONSTRAINT `main_fieldrehabsession_chk_3` CHECK ((`totale_afstand` >= 0)),
  CONSTRAINT `main_fieldrehabsession_chk_4` CHECK ((`afstand_20` >= 0)),
  CONSTRAINT `main_fieldrehabsession_chk_5` CHECK ((`afstand_25` >= 0)),
  CONSTRAINT `main_fieldrehabsession_chk_6` CHECK ((`acceleraties` >= 0)),
  CONSTRAINT `main_fieldrehabsession_chk_7` CHECK ((`deceleraties` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_fieldrehabsession`
--

LOCK TABLES `main_fieldrehabsession` WRITE;
/*!40000 ALTER TABLE `main_fieldrehabsession` DISABLE KEYS */;
INSERT INTO `main_fieldrehabsession` VALUES (1,'Fase 1','Slalom loop 100m met bal',1,45,NULL,NULL,NULL,NULL,NULL,NULL,'2025-11-13 06:29:56.198906',24),(2,'Fase 1','Hardlopen tot 12 km/u rechte stukken',1,45,8,4500,NULL,NULL,NULL,NULL,'2025-11-13 06:37:48.550663',13),(3,'Fase 1','Hardlopen tot 15 km/u rechte stukken',1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2025-11-13 06:37:48.566406',13),(4,'Fase 1','Slalom loop 100m zonder bal',1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2025-11-13 06:37:48.570737',13),(5,'Fase 1','Slalom loop 100m met bal',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2025-11-13 06:37:48.575610',13);
/*!40000 ALTER TABLE `main_fieldrehabsession` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_growthmeasurement`
--

DROP TABLE IF EXISTS `main_growthmeasurement`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_growthmeasurement` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `height_cm` double NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `profile_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `main_growthmeasurement_profile_id_date_3943ec9a_uniq` (`profile_id`,`date`),
  CONSTRAINT `main_growthmeasureme_profile_id_3aca0d62_fk_main_grow` FOREIGN KEY (`profile_id`) REFERENCES `main_growthprofile` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_growthmeasurement`
--

LOCK TABLES `main_growthmeasurement` WRITE;
/*!40000 ALTER TABLE `main_growthmeasurement` DISABLE KEYS */;
/*!40000 ALTER TABLE `main_growthmeasurement` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_growthprofile`
--

DROP TABLE IF EXISTS `main_growthprofile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_growthprofile` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `age` double DEFAULT NULL,
  `height` double DEFAULT NULL,
  `sitting_height` double DEFAULT NULL,
  `weight` double DEFAULT NULL,
  `maturity_offset` double DEFAULT NULL,
  `growth_complaints` tinyint(1) NOT NULL,
  `action` varchar(255) DEFAULT NULL,
  `updated_at` datetime(6) NOT NULL,
  `player_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `player_id` (`player_id`),
  CONSTRAINT `main_growthprofile_player_id_bd87e235_fk_main_player_id` FOREIGN KEY (`player_id`) REFERENCES `main_player` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_growthprofile`
--

LOCK TABLES `main_growthprofile` WRITE;
/*!40000 ALTER TABLE `main_growthprofile` DISABLE KEYS */;
/*!40000 ALTER TABLE `main_growthprofile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_hitweekplan`
--

DROP TABLE IF EXISTS `main_hitweekplan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_hitweekplan` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(120) NOT NULL,
  `week_start` date DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `trainer_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `main_hitweekplan_trainer_id_86e21ce2_fk_auth_user_id` (`trainer_id`),
  CONSTRAINT `main_hitweekplan_trainer_id_86e21ce2_fk_auth_user_id` FOREIGN KEY (`trainer_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_hitweekplan`
--

LOCK TABLES `main_hitweekplan` WRITE;
/*!40000 ALTER TABLE `main_hitweekplan` DISABLE KEYS */;
INSERT INTO `main_hitweekplan` VALUES (1,'Algemene HIT Weekplanning',NULL,'2026-02-18 10:31:10.960139',NULL);
/*!40000 ALTER TABLE `main_hitweekplan` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_hitweekplanentry`
--

DROP TABLE IF EXISTS `main_hitweekplanentry`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_hitweekplanentry` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `day_of_week` smallint unsigned NOT NULL,
  `content` varchar(255) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `plan_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_hitplan_day` (`plan_id`,`day_of_week`),
  CONSTRAINT `main_hitweekplanentry_plan_id_4a646e68_fk_main_hitweekplan_id` FOREIGN KEY (`plan_id`) REFERENCES `main_hitweekplan` (`id`),
  CONSTRAINT `main_hitweekplanentry_chk_1` CHECK ((`day_of_week` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_hitweekplanentry`
--

LOCK TABLES `main_hitweekplanentry` WRITE;
/*!40000 ALTER TABLE `main_hitweekplanentry` DISABLE KEYS */;
INSERT INTO `main_hitweekplanentry` VALUES (1,1,'','2026-02-18 10:31:10.978517',1),(2,2,'','2026-02-18 10:31:10.980517',1),(3,3,'','2026-02-18 10:31:10.982518',1),(4,4,'','2026-02-18 10:31:10.983925',1),(5,5,'','2026-02-18 10:31:10.985936',1),(6,6,'','2026-02-18 10:31:10.988403',1),(7,7,'','2026-02-18 10:31:10.989449',1);
/*!40000 ALTER TABLE `main_hitweekplanentry` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_hitweekplanning`
--

DROP TABLE IF EXISTS `main_hitweekplanning`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_hitweekplanning` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `monday` varchar(255) NOT NULL,
  `tuesday` varchar(255) NOT NULL,
  `wednesday` varchar(255) NOT NULL,
  `thursday` varchar(255) NOT NULL,
  `friday` varchar(255) NOT NULL,
  `saturday` varchar(255) NOT NULL,
  `sunday` varchar(255) NOT NULL,
  `trainer_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `main_hitweekplanning_trainer_id_0b4b6f8d_fk_auth_user_id` (`trainer_id`),
  CONSTRAINT `main_hitweekplanning_trainer_id_0b4b6f8d_fk_auth_user_id` FOREIGN KEY (`trainer_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_hitweekplanning`
--

LOCK TABLES `main_hitweekplanning` WRITE;
/*!40000 ALTER TABLE `main_hitweekplanning` DISABLE KEYS */;
INSERT INTO `main_hitweekplanning` VALUES (1,'2025-12-08 08:24:30.498576','','','','','','','',NULL);
/*!40000 ALTER TABLE `main_hitweekplanning` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_injury`
--

DROP TABLE IF EXISTS `main_injury`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_injury` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `injury_type` varchar(100) NOT NULL,
  `duration` varchar(100) DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `phase` varchar(10) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_injury`
--

LOCK TABLES `main_injury` WRITE;
/*!40000 ALTER TABLE `main_injury` DISABLE KEYS */;
INSERT INTO `main_injury` VALUES (1,'Thomas Verheydt','Kuitblessure (scheurtje) ','21','2025-10-25','early'),(2,'Amine Lachkar','Heup','24','2025-11-21','mid'),(3,'Niels van Berkel','Knieblessure ','25','2025-12-15','early');
/*!40000 ALTER TABLE `main_injury` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_injurycase`
--

DROP TABLE IF EXISTS `main_injurycase`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_injurycase` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `injury_type` varchar(100) NOT NULL,
  `phase` varchar(50) DEFAULT NULL,
  `status` varchar(30) NOT NULL,
  `started_on` date DEFAULT NULL,
  `expected_return_on` date DEFAULT NULL,
  `closed_on` date DEFAULT NULL,
  `notes` longtext,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `player_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `main_injury_player__4e7bb7_idx` (`player_id`,`status`),
  KEY `main_injury_started_738f54_idx` (`started_on`),
  CONSTRAINT `main_injurycase_player_id_8fdf68a6_fk_main_player_id` FOREIGN KEY (`player_id`) REFERENCES `main_player` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_injurycase`
--

LOCK TABLES `main_injurycase` WRITE;
/*!40000 ALTER TABLE `main_injurycase` DISABLE KEYS */;
INSERT INTO `main_injurycase` VALUES (1,'Kuitblessure (scheurtje) ','early','active','2025-10-25','2025-11-15',NULL,'Backfill vanuit legacy Injury','2026-02-18 10:31:10.932017','2026-02-18 10:31:10.932017',10),(2,'Heup','mid','active','2025-11-21','2025-12-15',NULL,'Backfill vanuit legacy Injury','2026-02-18 10:31:10.941690','2026-02-18 10:31:10.941690',13),(3,'Knieblessure ','early','active','2025-12-15','2026-01-09',NULL,'Backfill vanuit legacy Injury','2026-02-18 10:31:10.943690','2026-02-18 10:31:10.943690',5);
/*!40000 ALTER TABLE `main_injurycase` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_match`
--

DROP TABLE IF EXISTS `main_match`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_match` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `kickoff` datetime(6) NOT NULL,
  `home` varchar(100) NOT NULL,
  `away` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_match` (`kickoff`,`home`,`away`)
) ENGINE=InnoDB AUTO_INCREMENT=52 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_match`
--

LOCK TABLES `main_match` WRITE;
/*!40000 ALTER TABLE `main_match` DISABLE KEYS */;
INSERT INTO `main_match` VALUES (27,'2025-11-03 19:00:00.000000','Jong PSV','Willem II'),(28,'2025-11-07 19:00:00.000000','Willem II','TOP Oss'),(29,'2025-11-15 20:00:00.000000','Willem II','FC Emmen'),(30,'2025-11-21 19:00:00.000000','VVV-Venlo','Willem II'),(31,'2025-11-28 19:00:00.000000','FC Den Bosch','Willem II'),(32,'2025-12-06 15:30:00.000000','Willem II','FC Dordrecht'),(33,'2025-12-12 19:00:00.000000','Willem II','SC Cambuur'),(34,'2025-12-18 20:00:00.000000','Willem II','Sparta Rotterdam'),(35,'2025-12-21 13:30:00.000000','Helmond Sport','Willem II'),(36,'2026-01-09 19:00:00.000000','Willem II','ADO Den Haag'),(37,'2026-01-23 19:00:00.000000','Willem II','VVV-Venlo'),(38,'2026-02-02 19:00:00.000000','Jong Ajax','Willem II'),(39,'2026-02-08 13:30:00.000000','Willem II','RKC Waalwijk'),(40,'2026-02-16 19:00:00.000000','Jong FC Utrecht','Willem II'),(41,'2026-02-20 19:00:00.000000','Willem II','Vitesse'),(42,'2026-02-27 19:00:00.000000','FC Emmen','Willem II'),(43,'2026-03-08 13:30:00.000000','Willem II','FC Den Bosch'),(44,'2026-03-13 19:00:00.000000','TOP Oss','Willem II'),(45,'2026-03-22 15:45:00.000000','MVV','Willem II'),(46,'2026-03-27 11:00:00.000000','Willem II','De Graafschap'),(47,'2026-04-03 18:00:00.000000','Willem II','Jong PSV'),(48,'2026-04-06 14:45:00.000000','Roda JC','Willem II'),(49,'2026-04-12 14:45:00.000000','Willem II','Almere City FC'),(50,'2026-04-17 18:00:00.000000','Willem II','Jong AZ'),(51,'2026-04-24 18:00:00.000000','FC Dordrecht','Willem II');
/*!40000 ALTER TABLE `main_match` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_nutritionday`
--

DROP TABLE IF EXISTS `main_nutritionday`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_nutritionday` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `day` varchar(20) NOT NULL,
  `meal` varchar(255) DEFAULT NULL,
  `color` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `day` (`day`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_nutritionday`
--

LOCK TABLES `main_nutritionday` WRITE;
/*!40000 ALTER TABLE `main_nutritionday` DISABLE KEYS */;
INSERT INTO `main_nutritionday` VALUES (1,'Maandag',NULL,NULL),(2,'Dinsdag',NULL,NULL),(3,'Woensdag',NULL,NULL),(4,'Donderdag',NULL,NULL),(5,'Vrijdag',NULL,NULL),(6,'Zaterdag',NULL,NULL),(7,'Zondag',NULL,NULL);
/*!40000 ALTER TABLE `main_nutritionday` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_nutritionintakeitem`
--

DROP TABLE IF EXISTS `main_nutritionintakeitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_nutritionintakeitem` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `meal_key` varchar(30) NOT NULL,
  `value` varchar(255) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `session_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_nutrition_item_per_meal` (`session_id`,`meal_key`),
  CONSTRAINT `main_nutritionintake_session_id_74804472_fk_main_nutr` FOREIGN KEY (`session_id`) REFERENCES `main_nutritionintakesession` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_nutritionintakeitem`
--

LOCK TABLES `main_nutritionintakeitem` WRITE;
/*!40000 ALTER TABLE `main_nutritionintakeitem` DISABLE KEYS */;
INSERT INTO `main_nutritionintakeitem` VALUES (1,'breakfast','','2026-02-18 11:47:42.695563',1),(2,'snack1','','2026-02-18 11:47:42.695563',1),(3,'lunch','','2026-02-18 11:47:42.695563',1),(4,'snack2','','2026-02-18 11:47:42.695563',1),(5,'dinner','','2026-02-18 11:47:42.695563',1),(6,'snack3','','2026-02-18 11:47:42.695563',1),(7,'supplements','','2026-02-18 11:47:42.695563',1),(8,'breakfast','Fruit + yoghurt','2026-02-18 11:49:45.010002',2),(9,'snack1','Banaan','2026-02-18 11:49:45.013824',2),(10,'lunch','Pannenkoeken','2026-02-18 11:49:45.015701',2),(11,'snack2','Noten','2026-02-18 11:49:45.019147',2),(12,'dinner','Pasta met kip','2026-02-18 11:49:45.021492',2),(13,'snack3','Kwark','2026-02-18 11:49:45.023657',2),(14,'supplements','','2026-02-18 11:49:45.026403',2),(15,'breakfast','Fruit + yoghurt','2026-02-18 12:07:41.770433',3),(16,'snack1','Banaan','2026-02-18 12:07:41.773356',3),(17,'lunch','Pannenkoeken','2026-02-18 12:07:41.775713',3),(18,'snack2','Noten','2026-02-18 12:07:41.776722',3),(19,'dinner','Pasta met kip','2026-02-18 12:07:41.782342',3),(20,'snack3','Kwark','2026-02-18 12:07:41.784349',3),(21,'supplements','','2026-02-18 12:07:41.786357',3);
/*!40000 ALTER TABLE `main_nutritionintakeitem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_nutritionintakesession`
--

DROP TABLE IF EXISTS `main_nutritionintakesession`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_nutritionintakesession` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `date` date DEFAULT NULL,
  `goal` varchar(255) DEFAULT NULL,
  `next_meeting_goal` longtext,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `player_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `main_nutrit_player__b53571_idx` (`player_id`,`date`),
  CONSTRAINT `main_nutritionintakesession_player_id_5606b94f_fk_main_player_id` FOREIGN KEY (`player_id`) REFERENCES `main_player` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_nutritionintakesession`
--

LOCK TABLES `main_nutritionintakesession` WRITE;
/*!40000 ALTER TABLE `main_nutritionintakesession` DISABLE KEYS */;
INSERT INTO `main_nutritionintakesession` VALUES (1,NULL,'','','2026-02-18 11:47:42.692664','2026-02-18 11:47:42.692664',21),(2,NULL,'aankomen','','2026-02-18 11:49:45.010002','2026-02-18 11:49:45.010002',12),(3,NULL,'aankomen','','2026-02-18 12:07:41.766411','2026-02-18 12:07:41.766411',19);
/*!40000 ALTER TABLE `main_nutritionintakesession` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_oefening`
--

DROP TABLE IF EXISTS `main_oefening`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_oefening` (
  `id` int NOT NULL AUTO_INCREMENT,
  `oefening_naam` varchar(100) DEFAULT NULL,
  `categorie` varchar(50) DEFAULT NULL,
  `spiergroep` varchar(50) DEFAULT NULL,
  `moeilijkheidsgraad` varchar(50) DEFAULT NULL,
  `player_id` bigint DEFAULT NULL,
  `phase` varchar(100) DEFAULT NULL,
  `exercise` varchar(150) DEFAULT NULL,
  `description` text,
  `sets_reps` varchar(50) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `focus_point` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `main_oefening_player_id_fk` (`player_id`),
  CONSTRAINT `main_oefening_player_id_fk` FOREIGN KEY (`player_id`) REFERENCES `main_player` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_oefening`
--

LOCK TABLES `main_oefening` WRITE;
/*!40000 ALTER TABLE `main_oefening` DISABLE KEYS */;
INSERT INTO `main_oefening` VALUES (1,NULL,NULL,NULL,NULL,NULL,'Fase 1 – Pijnvrij bewegen','Nordic hamstring ','Rustig uitvoeren','3x8','2025-11-10 10:38:42',NULL);
/*!40000 ALTER TABLE `main_oefening` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_overig`
--

DROP TABLE IF EXISTS `main_overig`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_overig` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `text` longtext,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_overig`
--

LOCK TABLES `main_overig` WRITE;
/*!40000 ALTER TABLE `main_overig` DISABLE KEYS */;
/*!40000 ALTER TABLE `main_overig` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_player`
--

DROP TABLE IF EXISTS `main_player`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_player` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `prev_weight` double DEFAULT NULL,
  `curr_weight` double DEFAULT NULL,
  `sum_skinfolds` double DEFAULT NULL,
  `fat_perc` double DEFAULT NULL,
  `nutrition_focus` longtext,
  `image` varchar(100) DEFAULT NULL,
  `position` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=84 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_player`
--

LOCK TABLES `main_player` WRITE;
/*!40000 ALTER TABLE `main_player` DISABLE KEYS */;
INSERT INTO `main_player` VALUES (1,'Nick Doodeman',NULL,NULL,NULL,NULL,'','player_images/463449_nick_doodeman_20241202233119.jpg','Buitenspeler'),(2,'Raffael Behounek',NULL,NULL,NULL,NULL,'','player_images/552060_raffael_behounek_20241202131159.jpg','Centrale verdediger'),(3,'Justin Hoogma',NULL,NULL,NULL,NULL,'','player_images/432766.png','Centrale verdediger'),(4,'Jari Schuurman',NULL,NULL,NULL,NULL,'Eiwitten hoger','player_images/268333.jpg','Dynamische middenvelder'),(5,'Niels van Berkel',NULL,NULL,NULL,NULL,'Hij moet vooral aankomen','player_images/436789.jpg','Vleugelverdediger'),(6,'Jens Mathijsen',NULL,NULL,NULL,NULL,'Moet meer ruimte maken om te eten','player_images/1099155.jpg','Centrale verdediger'),(7,'Devin Haen',NULL,NULL,NULL,NULL,'','player_images/704771-1723629105.webp','Spits'),(8,'Wouter van der Steen',NULL,NULL,NULL,NULL,'','player_images/159896-1658911757.webp',NULL),(9,'Siegert Baartmans',NULL,NULL,NULL,NULL,'','player_images/images_6.jpg','Targetman'),(10,'Thomas Verheydt',NULL,NULL,NULL,NULL,'','player_images/images_5.jpg','Spits'),(11,'Nathan Tjoe-A-On',NULL,NULL,NULL,NULL,'','player_images/images_4.jpg','Vleugelverdediger'),(12,'Max de Waal',NULL,NULL,NULL,NULL,'','player_images/438732.jpg','Controlerende middenvelder'),(13,'Amine Lachkar',NULL,NULL,NULL,NULL,'','player_images/11637722_amine_lachkar_20241202221159_XTR8rXd.jpg','Controlerende middenvelder'),(14,'Uriël van Aalst',NULL,NULL,NULL,NULL,'','player_images/956285.png','Dynamische middenvelder'),(15,'Junior Poortvliet',NULL,NULL,NULL,NULL,'','player_images/junior-poortvliet-heeft-zijn-eerste-contract-getekend-bij-willem-ii.webp','Centrale verdediger'),(16,'Per van Loon',NULL,65,70,NULL,'','player_images/694201.jpg','Buitenspeler'),(17,'Thomas Didilion Hödl',NULL,NULL,NULL,NULL,'','player_images/302013_thomas_didillon_20241202012645.jpg',NULL),(18,'Karst de Leeuw',NULL,NULL,NULL,NULL,'','player_images/31._Karst_de_Leeuw.png.webp',NULL),(19,'Emilio Kehrer',NULL,NULL,NULL,NULL,'','player_images/396410.jpg','Buitenspeler'),(20,'Gijs Besselink',NULL,NULL,NULL,NULL,'','player_images/655248.png','Controlerende middenvelder'),(21,'Alessandro Ciranni',73,80,65,11,'','player_images/295662.jpg','Vleugelverdediger'),(22,'Armin Culum',NULL,NULL,NULL,NULL,'','player_images/56245-Fotoburo-Toin-Damen.jpg','Buitenspeler'),(23,'Samuel Bamba',NULL,NULL,NULL,NULL,'','player_images/424811.jpg','Buitenspeler'),(24,'Anass Zarrouk',NULL,NULL,NULL,NULL,'','player_images/55994-Geert-van-Erven.jpg','Dynamische middenvelder'),(25,'Mounir el Allouchi',NULL,NULL,NULL,NULL,'','player_images/267781.jpg','Dynamische middenvelder'),(26,'Finn Stams',NULL,NULL,NULL,NULL,'','player_images/531195.jpg','Centrale verdediger'),(27,'Pieter van Maarschalkerwaard',NULL,NULL,NULL,NULL,'','player_images/1797867.png','Dynamische middenvelder'),(28,'Boet van der Linden',NULL,NULL,NULL,NULL,'','player_images/2757282_boet_van_der_linden__20250901001022.png',NULL);
/*!40000 ALTER TABLE `main_player` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_playerintake`
--

DROP TABLE IF EXISTS `main_playerintake`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_playerintake` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `date` date DEFAULT NULL,
  `goal` varchar(255) DEFAULT NULL,
  `breakfast` varchar(255) DEFAULT NULL,
  `snack1` varchar(255) DEFAULT NULL,
  `lunch` varchar(255) DEFAULT NULL,
  `snack2` varchar(255) DEFAULT NULL,
  `dinner` varchar(255) DEFAULT NULL,
  `snack3` varchar(255) DEFAULT NULL,
  `next_meeting_goal` longtext,
  `updated_at` datetime(6) NOT NULL,
  `player_id` bigint NOT NULL,
  `supplements` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `player_id` (`player_id`),
  CONSTRAINT `main_playerintake_player_id_fbb1e5e7_fk_main_player_id` FOREIGN KEY (`player_id`) REFERENCES `main_player` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_playerintake`
--

LOCK TABLES `main_playerintake` WRITE;
/*!40000 ALTER TABLE `main_playerintake` DISABLE KEYS */;
INSERT INTO `main_playerintake` VALUES (1,NULL,'','','','','','','','','2026-02-05 07:06:11.635392',21,NULL),(2,NULL,'aankomen','Fruit + yoghurt','Banaan','Pannenkoeken','Noten','Pasta met kip','Kwark','','2026-02-18 11:49:45.005674',12,'');
/*!40000 ALTER TABLE `main_playerintake` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_playerteamassignment`
--

DROP TABLE IF EXISTS `main_playerteamassignment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_playerteamassignment` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `start_date` date NOT NULL,
  `end_date` date DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `player_id` bigint NOT NULL,
  `team_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_player_team_start` (`player_id`,`team_id`,`start_date`),
  KEY `main_playerteamassignment_team_id_07f1a32a_fk_main_team_id` (`team_id`),
  CONSTRAINT `main_playerteamassignment_player_id_83fbf81e_fk_main_player_id` FOREIGN KEY (`player_id`) REFERENCES `main_player` (`id`),
  CONSTRAINT `main_playerteamassignment_team_id_07f1a32a_fk_main_team_id` FOREIGN KEY (`team_id`) REFERENCES `main_team` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_playerteamassignment`
--

LOCK TABLES `main_playerteamassignment` WRITE;
/*!40000 ALTER TABLE `main_playerteamassignment` DISABLE KEYS */;
/*!40000 ALTER TABLE `main_playerteamassignment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_playertest`
--

DROP TABLE IF EXISTS `main_playertest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_playertest` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `sprint_10` double DEFAULT NULL,
  `sprint_30` double DEFAULT NULL,
  `cmj` double DEFAULT NULL,
  `squat_jump` double DEFAULT NULL,
  `isrt` double DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `curr_weight` double DEFAULT NULL,
  `sum_skinfolds` double DEFAULT NULL,
  `player_id` bigint NOT NULL,
  `submax` double DEFAULT NULL,
  `length` double DEFAULT NULL,
  `test_date` date NOT NULL,
  PRIMARY KEY (`id`),
  KEY `main_playertest_player_id_8ac5a403_fk_main_player_id` (`player_id`),
  CONSTRAINT `main_playertest_player_id_8ac5a403_fk_main_player_id` FOREIGN KEY (`player_id`) REFERENCES `main_player` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_playertest`
--

LOCK TABLES `main_playertest` WRITE;
/*!40000 ALTER TABLE `main_playertest` DISABLE KEYS */;
INSERT INTO `main_playertest` VALUES (1,3.8,4.5,34,34,22,'2025-11-11 06:40:23.468487',NULL,NULL,1,NULL,NULL,'2025-12-10'),(2,1.22,4,3,34,120,'2025-11-11 06:40:23.468487',NULL,NULL,1,NULL,NULL,'2025-12-10'),(3,1.72,4.35,41.2,NULL,122,'2025-12-09 05:58:08.298476',NULL,NULL,21,87.5,NULL,'2025-12-10'),(4,NULL,NULL,NULL,NULL,NULL,'2025-12-10 08:51:55.487862',72.4,55,21,NULL,NULL,'2025-12-10'),(5,1.72,4.35,41.2,NULL,1780,'2025-12-10 08:52:52.217402',72.4,52,21,87.5,NULL,'2025-12-10'),(6,NULL,NULL,NULL,NULL,NULL,'2025-12-10 11:51:03.790290',72.2,44,21,NULL,NULL,'2025-12-10'),(7,NULL,NULL,NULL,NULL,NULL,'2025-12-10 11:51:40.427526',72.8,63.5,21,NULL,NULL,'2025-12-10'),(8,NULL,NULL,NULL,NULL,NULL,'2025-12-10 11:52:37.227786',72,63.4,21,NULL,NULL,'2025-12-10'),(9,NULL,NULL,NULL,NULL,NULL,'2025-12-10 11:55:18.137352',72.2,64,21,NULL,NULL,'2025-12-10'),(10,NULL,NULL,NULL,NULL,NULL,'2025-12-10 12:10:13.575395',71.6,59,21,NULL,NULL,'2025-12-09'),(11,NULL,NULL,NULL,NULL,NULL,'2025-12-10 12:10:42.147059',72,60,21,NULL,NULL,'2025-12-10'),(12,1.72,4.25,41,NULL,122,'2025-12-11 09:52:23.981797',NULL,NULL,12,87.4,NULL,'2025-12-11');
/*!40000 ALTER TABLE `main_playertest` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_programma`
--

DROP TABLE IF EXISTS `main_programma`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_programma` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `doel` varchar(255) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `player_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `main_programma_player_id_5bc077f4_fk_main_player_id` (`player_id`),
  CONSTRAINT `main_programma_player_id_5bc077f4_fk_main_player_id` FOREIGN KEY (`player_id`) REFERENCES `main_player` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_programma`
--

LOCK TABLES `main_programma` WRITE;
/*!40000 ALTER TABLE `main_programma` DISABLE KEYS */;
/*!40000 ALTER TABLE `main_programma` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_programmaoefening`
--

DROP TABLE IF EXISTS `main_programmaoefening`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_programmaoefening` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `naam` varchar(150) NOT NULL,
  `duur` varchar(50) DEFAULT NULL,
  `rpe` varchar(20) DEFAULT NULL,
  `frequentie` varchar(50) DEFAULT NULL,
  `opmerkingen` longtext,
  `programma_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `main_programmaoefeni_programma_id_5c7695cf_fk_main_prog` (`programma_id`),
  CONSTRAINT `main_programmaoefeni_programma_id_5c7695cf_fk_main_prog` FOREIGN KEY (`programma_id`) REFERENCES `main_programma` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_programmaoefening`
--

LOCK TABLES `main_programmaoefening` WRITE;
/*!40000 ALTER TABLE `main_programmaoefening` DISABLE KEYS */;
/*!40000 ALTER TABLE `main_programmaoefening` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_rpeentry`
--

DROP TABLE IF EXISTS `main_rpeentry`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_rpeentry` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `training_type` varchar(50) NOT NULL,
  `rpe` int NOT NULL,
  `session_load` int DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `player_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `main_rpeentry_player_id_d9a3e014_fk_main_player_id` (`player_id`),
  CONSTRAINT `main_rpeentry_player_id_d9a3e014_fk_main_player_id` FOREIGN KEY (`player_id`) REFERENCES `main_player` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_rpeentry`
--

LOCK TABLES `main_rpeentry` WRITE;
/*!40000 ALTER TABLE `main_rpeentry` DISABLE KEYS */;
INSERT INTO `main_rpeentry` VALUES (1,'2025-11-22','Training',10,NULL,'2025-11-22 20:02:06.259262',21),(2,'2025-12-04','Training',10,NULL,'2025-12-05 10:52:38.709562',21),(3,'2025-12-05','Training',1,NULL,'2025-12-05 11:15:46.050787',21),(4,'2025-12-18','Training',8,NULL,'2025-12-18 06:27:46.109584',21);
/*!40000 ALTER TABLE `main_rpeentry` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_staff`
--

DROP TABLE IF EXISTS `main_staff`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_staff` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `role` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_staff`
--

LOCK TABLES `main_staff` WRITE;
/*!40000 ALTER TABLE `main_staff` DISABLE KEYS */;
INSERT INTO `main_staff` VALUES (1,'John Stegeman','Hoofdtrainer'),(2,'Freek Heerkens','Technisch directeur'),(3,'Merijn Goris','Algemeen directeur'),(4,'Sam Strijbosch','Recruitment coördinator'),(5,'Kristof Aalbrecht','Assistent trainer'),(6,'Pascal Diender','Assistent trainer'),(7,'Peter den Otter','Keeperstrainer'),(8,'Ilse Driessen','Kok'),(9,'Henry van Amelsfoort','Verzorger'),(10,'Nils Thörner','Head of Performance'),(11,'Jos de Kruijf','Commercieel manager'),(12,'Martin van den Heuvel','Financieel directeur'),(13,'Adrie Koster','Technisch adviseur'),(14,'Steven Aptroot','Hoofd scouting'),(15,'Pieter Vioen','Clubarts'),(16,'Sep Bierkens','Fysiotherapeut'),(17,'Michel de Gruijter','Hoofd medisch'),(18,'Jasper de Langen','Fysiotherapeut'),(19,'Jos van Nieuwstadt','Teammanager');
/*!40000 ALTER TABLE `main_staff` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_team`
--

DROP TABLE IF EXISTS `main_team`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_team` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `code` varchar(20) NOT NULL,
  `name` varchar(100) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_team`
--

LOCK TABLES `main_team` WRITE;
/*!40000 ALTER TABLE `main_team` DISABLE KEYS */;
/*!40000 ALTER TABLE `main_team` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_trainingdata`
--

DROP TABLE IF EXISTS `main_trainingdata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_trainingdata` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `week` int unsigned NOT NULL,
  `total_distance` double NOT NULL,
  `hsd` double NOT NULL,
  `sprints` int NOT NULL,
  `load` double NOT NULL,
  `player_id` bigint NOT NULL,
  `session_date` date NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `main_trainingdata_player_id_session_date_69f7cba2_uniq` (`player_id`,`session_date`),
  CONSTRAINT `main_trainingdata_player_id_ac09cbaf_fk_main_player_id` FOREIGN KEY (`player_id`) REFERENCES `main_player` (`id`),
  CONSTRAINT `main_trainingdata_chk_1` CHECK ((`week` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=286 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_trainingdata`
--

LOCK TABLES `main_trainingdata` WRITE;
/*!40000 ALTER TABLE `main_trainingdata` DISABLE KEYS */;
INSERT INTO `main_trainingdata` VALUES (274,46,4923.07,252.66,18,0,2,'2025-11-10'),(275,46,2562.99,107.92,7,0,6,'2025-11-10'),(276,46,5553.05,327.84,22,0,3,'2025-11-10'),(277,46,4539.43,319.49,21,0,4,'2025-11-10'),(278,46,4888.68,215.04,16,0,19,'2025-11-10'),(279,46,6059.09,196.09,16,0,9,'2025-11-10'),(280,46,5139.88,368.85,27,0,1,'2025-11-10'),(281,46,5063.12,260.89,22,0,11,'2025-11-10'),(282,46,2394.74,132.09,8,0,27,'2025-11-10'),(283,46,2585.49,87.45,6,0,24,'2025-11-10'),(284,46,4302.78,261.5,22,0,23,'2025-11-10'),(285,46,5306.3,251.13,17,0,21,'2025-11-10');
/*!40000 ALTER TABLE `main_trainingdata` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_vakantieplanning`
--

DROP TABLE IF EXISTS `main_vakantieplanning`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_vakantieplanning` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `loopvorm` varchar(255) DEFAULT NULL,
  `kracht` varchar(255) DEFAULT NULL,
  `visible_from` date NOT NULL,
  `is_visible` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_vakantieplanning`
--

LOCK TABLES `main_vakantieplanning` WRITE;
/*!40000 ALTER TABLE `main_vakantieplanning` DISABLE KEYS */;
/*!40000 ALTER TABLE `main_vakantieplanning` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_vakantieplanning_players`
--

DROP TABLE IF EXISTS `main_vakantieplanning_players`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_vakantieplanning_players` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `vakantieplanning_id` bigint NOT NULL,
  `player_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `main_vakantieplanning_pl_vakantieplanning_id_play_92cd09e8_uniq` (`vakantieplanning_id`,`player_id`),
  KEY `main_vakantieplannin_player_id_e64de42a_fk_main_play` (`player_id`),
  CONSTRAINT `main_vakantieplannin_player_id_e64de42a_fk_main_play` FOREIGN KEY (`player_id`) REFERENCES `main_player` (`id`),
  CONSTRAINT `main_vakantieplannin_vakantieplanning_id_d452549a_fk_main_vaka` FOREIGN KEY (`vakantieplanning_id`) REFERENCES `main_vakantieplanning` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_vakantieplanning_players`
--

LOCK TABLES `main_vakantieplanning_players` WRITE;
/*!40000 ALTER TABLE `main_vakantieplanning_players` DISABLE KEYS */;
/*!40000 ALTER TABLE `main_vakantieplanning_players` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_vakantieprogrammaentry`
--

DROP TABLE IF EXISTS `main_vakantieprogrammaentry`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_vakantieprogrammaentry` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `loopvorm` varchar(255) DEFAULT NULL,
  `kracht` varchar(255) DEFAULT NULL,
  `completed` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `player_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `main_vakantieprogrammaentry_player_id_ade3415b_fk_main_player_id` (`player_id`),
  CONSTRAINT `main_vakantieprogrammaentry_player_id_ade3415b_fk_main_player_id` FOREIGN KEY (`player_id`) REFERENCES `main_player` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_vakantieprogrammaentry`
--

LOCK TABLES `main_vakantieprogrammaentry` WRITE;
/*!40000 ALTER TABLE `main_vakantieprogrammaentry` DISABLE KEYS */;
INSERT INTO `main_vakantieprogrammaentry` VALUES (1,'2026-02-07','interval 6x200 m in 30 seconde + 30 sec rust','',0,'2026-02-07 11:05:51.512005',21);
/*!40000 ALTER TABLE `main_vakantieprogrammaentry` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_wedstrijddata`
--

DROP TABLE IF EXISTS `main_wedstrijddata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_wedstrijddata` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `match_date` date NOT NULL,
  `week` int unsigned NOT NULL,
  `total_distance` double NOT NULL,
  `hsd` double NOT NULL,
  `sprints` int NOT NULL,
  `load` double NOT NULL,
  `player_id` bigint NOT NULL,
  `accelerations` int NOT NULL,
  `decelerations` int NOT NULL,
  `his` double NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `main_wedstrijddata_player_id_match_date_63275ef1_uniq` (`player_id`,`match_date`),
  CONSTRAINT `main_wedstrijddata_player_id_c4b8ef7d_fk_main_player_id` FOREIGN KEY (`player_id`) REFERENCES `main_player` (`id`),
  CONSTRAINT `main_wedstrijddata_chk_1` CHECK ((`week` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=65 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_wedstrijddata`
--

LOCK TABLES `main_wedstrijddata` WRITE;
/*!40000 ALTER TABLE `main_wedstrijddata` DISABLE KEYS */;
INSERT INTO `main_wedstrijddata` VALUES (52,'2025-11-15',46,10395.69,683.04,48,2144,2,72,92,85.51),(53,'2025-11-15',46,13070.4,1477.46,87,3560,14,78,131,324.06),(54,'2025-11-15',46,8153.06,498.8,30,1641.24,4,46,47,107.56),(55,'2025-11-15',46,9672.27,1037.2,58,2316.3,19,61,82,201.6),(56,'2025-11-15',46,10536.81,994.07,58,2394.36,9,70,87,205.54),(57,'2025-11-15',46,11690.13,1210.73,72,2852.4,1,98,131,222.17),(58,'2025-11-15',46,10810.53,877.89,56,2261.28,11,58,103,183.46),(59,'2025-11-15',46,12797.51,899.46,64,3171.49,20,110,138,52.81),(60,'2025-11-15',46,11145.48,653.83,47,2217.52,26,70,79,106.06),(61,'2025-11-15',46,2310.38,244.05,13,609.39,22,22,24,86),(62,'2025-11-15',46,4107.92,176.01,14,908.79,24,28,40,11.38),(63,'2025-11-15',46,11391.48,898.64,55,2486.95,21,87,125,192.75),(64,'2025-11-15',46,1288.78,82.65,4,295.48,25,11,15,28.76);
/*!40000 ALTER TABLE `main_wedstrijddata` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_weightentry`
--

DROP TABLE IF EXISTS `main_weightentry`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_weightentry` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `weight` double NOT NULL,
  `player_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `main_weightentry_player_id_date_f20e6e7e_uniq` (`player_id`,`date`),
  CONSTRAINT `main_weightentry_player_id_326dccd1_fk_main_player_id` FOREIGN KEY (`player_id`) REFERENCES `main_player` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_weightentry`
--

LOCK TABLES `main_weightentry` WRITE;
/*!40000 ALTER TABLE `main_weightentry` DISABLE KEYS */;
/*!40000 ALTER TABLE `main_weightentry` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_wellnessentry`
--

DROP TABLE IF EXISTS `main_wellnessentry`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_wellnessentry` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `player_id` bigint NOT NULL,
  `date` date NOT NULL,
  `sleep` int DEFAULT NULL,
  `mood` int DEFAULT NULL,
  `fitness` int DEFAULT NULL,
  `soreness` int DEFAULT NULL,
  `comment` text,
  PRIMARY KEY (`id`),
  KEY `main_wellnessentry_player_id_fk` (`player_id`),
  CONSTRAINT `main_wellnessentry_player_id_fk` FOREIGN KEY (`player_id`) REFERENCES `main_player` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_wellnessentry`
--

LOCK TABLES `main_wellnessentry` WRITE;
/*!40000 ALTER TABLE `main_wellnessentry` DISABLE KEYS */;
INSERT INTO `main_wellnessentry` VALUES (1,21,'2025-12-05',2,1,3,1,'niks'),(2,21,'2026-01-20',1,2,1,1,'');
/*!40000 ALTER TABLE `main_wellnessentry` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_youthguest`
--

DROP TABLE IF EXISTS `main_youthguest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_youthguest` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `team` varchar(100) DEFAULT NULL,
  `week_of` date DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_youthguest`
--

LOCK TABLES `main_youthguest` WRITE;
/*!40000 ALTER TABLE `main_youthguest` DISABLE KEYS */;
/*!40000 ALTER TABLE `main_youthguest` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_youthguestprofile`
--

DROP TABLE IF EXISTS `main_youthguestprofile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_youthguestprofile` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `team` varchar(100) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_youthguest_profile_name_team` (`name`,`team`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_youthguestprofile`
--

LOCK TABLES `main_youthguestprofile` WRITE;
/*!40000 ALTER TABLE `main_youthguestprofile` DISABLE KEYS */;
/*!40000 ALTER TABLE `main_youthguestprofile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_youthguestweek`
--

DROP TABLE IF EXISTS `main_youthguestweek`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_youthguestweek` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `week_of` date DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `profile_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_youthguest_profile_week` (`profile_id`,`week_of`),
  CONSTRAINT `main_youthguestweek_profile_id_5efdaa67_fk_main_yout` FOREIGN KEY (`profile_id`) REFERENCES `main_youthguestprofile` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_youthguestweek`
--

LOCK TABLES `main_youthguestweek` WRITE;
/*!40000 ALTER TABLE `main_youthguestweek` DISABLE KEYS */;
/*!40000 ALTER TABLE `main_youthguestweek` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'willemii_dashboard'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-02-18 14:34:17
