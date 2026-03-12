-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: localhost    Database: willemii_dashboard
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
) ENGINE=InnoDB AUTO_INCREMENT=345 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add player',7,'add_player'),(26,'Can change player',7,'change_player'),(27,'Can delete player',7,'delete_player'),(28,'Can view player',7,'view_player'),(29,'Can add Dagprogramma',8,'add_dayprogram'),(30,'Can change Dagprogramma',8,'change_dayprogram'),(31,'Can delete Dagprogramma',8,'delete_dayprogram'),(32,'Can view Dagprogramma',8,'view_dayprogram'),(33,'Can add Blessure',9,'add_injury'),(34,'Can change Blessure',9,'change_injury'),(35,'Can delete Blessure',9,'delete_injury'),(36,'Can view Blessure',9,'view_injury'),(37,'Can add Testresultaat',10,'add_playertest'),(38,'Can change Testresultaat',10,'change_playertest'),(39,'Can delete Testresultaat',10,'delete_playertest'),(40,'Can view Testresultaat',10,'view_playertest'),(41,'Can add Trainingsdata',11,'add_trainingdata'),(42,'Can change Trainingsdata',11,'change_trainingdata'),(43,'Can delete Trainingsdata',11,'delete_trainingdata'),(44,'Can view Trainingsdata',11,'view_trainingdata'),(45,'Can add Oefening',12,'add_oefening'),(46,'Can change Oefening',12,'change_oefening'),(47,'Can delete Oefening',12,'delete_oefening'),(48,'Can view Oefening',12,'view_oefening'),(49,'Can add Wellnessinvoer',13,'add_wellnessentry'),(50,'Can change Wellnessinvoer',13,'change_wellnessentry'),(51,'Can delete Wellnessinvoer',13,'delete_wellnessentry'),(52,'Can view Wellnessinvoer',13,'view_wellnessentry'),(53,'Can add Veldrevalidatie sessie',14,'add_fieldrehabsession'),(54,'Can change Veldrevalidatie sessie',14,'change_fieldrehabsession'),(55,'Can delete Veldrevalidatie sessie',14,'delete_fieldrehabsession'),(56,'Can view Veldrevalidatie sessie',14,'view_fieldrehabsession'),(57,'Can add Individueel Programma',15,'add_programma'),(58,'Can change Individueel Programma',15,'change_programma'),(59,'Can delete Individueel Programma',15,'delete_programma'),(60,'Can view Individueel Programma',15,'view_programma'),(61,'Can add Programma Oefening',16,'add_programmaoefening'),(62,'Can change Programma Oefening',16,'change_programmaoefening'),(63,'Can delete Programma Oefening',16,'delete_programmaoefening'),(64,'Can view Programma Oefening',16,'view_programmaoefening'),(65,'Can add RPE Invoer',17,'add_rpeentry'),(66,'Can change RPE Invoer',17,'change_rpeentry'),(67,'Can delete RPE Invoer',17,'delete_rpeentry'),(68,'Can view RPE Invoer',17,'view_rpeentry'),(69,'Can add pop gesprek',18,'add_popgesprek'),(70,'Can change pop gesprek',18,'change_popgesprek'),(71,'Can delete pop gesprek',18,'delete_popgesprek'),(72,'Can view pop gesprek',18,'view_popgesprek'),(73,'Can add Dagprogramma',19,'add_dailyprogram'),(74,'Can change Dagprogramma',19,'change_dailyprogram'),(75,'Can delete Dagprogramma',19,'delete_dailyprogram'),(76,'Can view Dagprogramma',19,'view_dailyprogram'),(77,'Can add attendance',20,'add_attendance'),(78,'Can change attendance',20,'change_attendance'),(79,'Can delete attendance',20,'delete_attendance'),(80,'Can view attendance',20,'view_attendance'),(81,'Can add Aanwezigheid',21,'add_aanwezigheid'),(82,'Can change Aanwezigheid',21,'change_aanwezigheid'),(83,'Can delete Aanwezigheid',21,'delete_aanwezigheid'),(84,'Can view Aanwezigheid',21,'view_aanwezigheid'),(85,'Can add overig',22,'add_overig'),(86,'Can change overig',22,'change_overig'),(87,'Can delete overig',22,'delete_overig'),(88,'Can view overig',22,'view_overig'),(89,'Can add Staflid',23,'add_staff'),(90,'Can change Staflid',23,'change_staff'),(91,'Can delete Staflid',23,'delete_staff'),(92,'Can view Staflid',23,'view_staff'),(93,'Can add Wedstrijddata',24,'add_wedstrijddata'),(94,'Can change Wedstrijddata',24,'change_wedstrijddata'),(95,'Can delete Wedstrijddata',24,'delete_wedstrijddata'),(96,'Can view Wedstrijddata',24,'view_wedstrijddata'),(97,'Can add hit week planning',25,'add_hitweekplanning'),(98,'Can change hit week planning',25,'change_hitweekplanning'),(99,'Can delete hit week planning',25,'delete_hitweekplanning'),(100,'Can view hit week planning',25,'view_hitweekplanning'),(101,'Can add nutrition day',26,'add_nutritionday'),(102,'Can change nutrition day',26,'change_nutritionday'),(103,'Can delete nutrition day',26,'delete_nutritionday'),(104,'Can view nutrition day',26,'view_nutritionday'),(105,'Can add antropometry',27,'add_antropometry'),(106,'Can change antropometry',27,'change_antropometry'),(107,'Can delete antropometry',27,'delete_antropometry'),(108,'Can view antropometry',27,'view_antropometry'),(109,'Can add match',28,'add_match'),(110,'Can change match',28,'change_match'),(111,'Can delete match',28,'delete_match'),(112,'Can view match',28,'view_match'),(113,'Can add player intake',29,'add_playerintake'),(114,'Can change player intake',29,'change_playerintake'),(115,'Can delete player intake',29,'delete_playerintake'),(116,'Can view player intake',29,'view_playerintake'),(117,'Can add Verjaardag',30,'add_birthday'),(118,'Can change Verjaardag',30,'change_birthday'),(119,'Can delete Verjaardag',30,'delete_birthday'),(120,'Can view Verjaardag',30,'view_birthday'),(121,'Can add Meetrainer jeugd',31,'add_youthguest'),(122,'Can change Meetrainer jeugd',31,'change_youthguest'),(123,'Can delete Meetrainer jeugd',31,'delete_youthguest'),(124,'Can view Meetrainer jeugd',31,'view_youthguest'),(125,'Can add weight entry',32,'add_weightentry'),(126,'Can change weight entry',32,'change_weightentry'),(127,'Can delete weight entry',32,'delete_weightentry'),(128,'Can view weight entry',32,'view_weightentry'),(129,'Can add Vakantieprogramma item',33,'add_vakantieprogrammaentry'),(130,'Can change Vakantieprogramma item',33,'change_vakantieprogrammaentry'),(131,'Can delete Vakantieprogramma item',33,'delete_vakantieprogrammaentry'),(132,'Can view Vakantieprogramma item',33,'view_vakantieprogrammaentry'),(133,'Can add Vakantieplanning',34,'add_vakantieplanning'),(134,'Can change Vakantieplanning',34,'change_vakantieplanning'),(135,'Can delete Vakantieplanning',34,'delete_vakantieplanning'),(136,'Can view Vakantieplanning',34,'view_vakantieplanning'),(137,'Can add Groeimeetpunt',35,'add_growthmeasurement'),(138,'Can change Groeimeetpunt',35,'change_growthmeasurement'),(139,'Can delete Groeimeetpunt',35,'delete_growthmeasurement'),(140,'Can view Groeimeetpunt',35,'view_growthmeasurement'),(141,'Can add Groeiprofiel',36,'add_growthprofile'),(142,'Can change Groeiprofiel',36,'change_growthprofile'),(143,'Can delete Groeiprofiel',36,'delete_growthprofile'),(144,'Can view Groeiprofiel',36,'view_growthprofile'),(145,'Can add team',37,'add_team'),(146,'Can change team',37,'change_team'),(147,'Can delete team',37,'delete_team'),(148,'Can view team',37,'view_team'),(149,'Can add day program entry',38,'add_dayprogramentry'),(150,'Can change day program entry',38,'change_dayprogramentry'),(151,'Can delete day program entry',38,'delete_dayprogramentry'),(152,'Can view day program entry',38,'view_dayprogramentry'),(153,'Can add hit week plan',39,'add_hitweekplan'),(154,'Can change hit week plan',39,'change_hitweekplan'),(155,'Can delete hit week plan',39,'delete_hitweekplan'),(156,'Can view hit week plan',39,'view_hitweekplan'),(157,'Can add injury case',40,'add_injurycase'),(158,'Can change injury case',40,'change_injurycase'),(159,'Can delete injury case',40,'delete_injurycase'),(160,'Can view injury case',40,'view_injurycase'),(161,'Can add player team assignment',41,'add_playerteamassignment'),(162,'Can change player team assignment',41,'change_playerteamassignment'),(163,'Can delete player team assignment',41,'delete_playerteamassignment'),(164,'Can view player team assignment',41,'view_playerteamassignment'),(165,'Can add hit week plan entry',42,'add_hitweekplanentry'),(166,'Can change hit week plan entry',42,'change_hitweekplanentry'),(167,'Can delete hit week plan entry',42,'delete_hitweekplanentry'),(168,'Can view hit week plan entry',42,'view_hitweekplanentry'),(169,'Can add anthropometry measurement',43,'add_anthropometrymeasurement'),(170,'Can change anthropometry measurement',43,'change_anthropometrymeasurement'),(171,'Can delete anthropometry measurement',43,'delete_anthropometrymeasurement'),(172,'Can view anthropometry measurement',43,'view_anthropometrymeasurement'),(173,'Can add anthropometry session',44,'add_anthropometrysession'),(174,'Can change anthropometry session',44,'change_anthropometrysession'),(175,'Can delete anthropometry session',44,'delete_anthropometrysession'),(176,'Can view anthropometry session',44,'view_anthropometrysession'),(177,'Can add nutrition intake session',45,'add_nutritionintakesession'),(178,'Can change nutrition intake session',45,'change_nutritionintakesession'),(179,'Can delete nutrition intake session',45,'delete_nutritionintakesession'),(180,'Can view nutrition intake session',45,'view_nutritionintakesession'),(181,'Can add nutrition intake item',46,'add_nutritionintakeitem'),(182,'Can change nutrition intake item',46,'change_nutritionintakeitem'),(183,'Can delete nutrition intake item',46,'delete_nutritionintakeitem'),(184,'Can view nutrition intake item',46,'view_nutritionintakeitem'),(185,'Can add birthday record',47,'add_birthdayrecord'),(186,'Can change birthday record',47,'change_birthdayrecord'),(187,'Can delete birthday record',47,'delete_birthdayrecord'),(188,'Can view birthday record',47,'view_birthdayrecord'),(189,'Can add birthday profile',48,'add_birthdayprofile'),(190,'Can change birthday profile',48,'change_birthdayprofile'),(191,'Can delete birthday profile',48,'delete_birthdayprofile'),(192,'Can view birthday profile',48,'view_birthdayprofile'),(193,'Can add youth guest week',49,'add_youthguestweek'),(194,'Can change youth guest week',49,'change_youthguestweek'),(195,'Can delete youth guest week',49,'delete_youthguestweek'),(196,'Can view youth guest week',49,'view_youthguestweek'),(197,'Can add youth guest profile',50,'add_youthguestprofile'),(198,'Can change youth guest profile',50,'change_youthguestprofile'),(199,'Can delete youth guest profile',50,'delete_youthguestprofile'),(200,'Can view youth guest profile',50,'view_youthguestprofile'),(201,'Can add attendance status',51,'add_attendancestatus'),(202,'Can change attendance status',51,'change_attendancestatus'),(203,'Can delete attendance status',51,'delete_attendancestatus'),(204,'Can view attendance status',51,'view_attendancestatus'),(205,'Can add individual day plan',52,'add_individualdayplan'),(206,'Can change individual day plan',52,'change_individualdayplan'),(207,'Can delete individual day plan',52,'delete_individualdayplan'),(208,'Can view individual day plan',52,'view_individualdayplan'),(209,'Can add individual day plan note',53,'add_individualdayplannote'),(210,'Can change individual day plan note',53,'change_individualdayplannote'),(211,'Can delete individual day plan note',53,'delete_individualdayplannote'),(212,'Can view individual day plan note',53,'view_individualdayplannote'),(213,'Can add attendance record',54,'add_attendancerecord'),(214,'Can change attendance record',54,'change_attendancerecord'),(215,'Can delete attendance record',54,'delete_attendancerecord'),(216,'Can view attendance record',54,'view_attendancerecord'),(217,'Can add overig note',55,'add_overignote'),(218,'Can change overig note',55,'change_overignote'),(219,'Can delete overig note',55,'delete_overignote'),(220,'Can view overig note',55,'view_overignote'),(221,'Can add performance metric type',56,'add_performancemetrictype'),(222,'Can change performance metric type',56,'change_performancemetrictype'),(223,'Can delete performance metric type',56,'delete_performancemetrictype'),(224,'Can view performance metric type',56,'view_performancemetrictype'),(225,'Can add performance session',57,'add_performancesession'),(226,'Can change performance session',57,'change_performancesession'),(227,'Can delete performance session',57,'delete_performancesession'),(228,'Can view performance session',57,'view_performancesession'),(229,'Can add performance metric',58,'add_performancemetric'),(230,'Can change performance metric',58,'change_performancemetric'),(231,'Can delete performance metric',58,'delete_performancemetric'),(232,'Can view performance metric',58,'view_performancemetric'),(233,'Can add injury phase',59,'add_injuryphase'),(234,'Can change injury phase',59,'change_injuryphase'),(235,'Can delete injury phase',59,'delete_injuryphase'),(236,'Can view injury phase',59,'view_injuryphase'),(237,'Can add injury status',60,'add_injurystatus'),(238,'Can change injury status',60,'change_injurystatus'),(239,'Can delete injury status',60,'delete_injurystatus'),(240,'Can view injury status',60,'view_injurystatus'),(241,'Can add injury type',61,'add_injurytype'),(242,'Can change injury type',61,'change_injurytype'),(243,'Can delete injury type',61,'delete_injurytype'),(244,'Can view injury type',61,'view_injurytype'),(245,'Can add field rehab component',62,'add_fieldrehabcomponent'),(246,'Can change field rehab component',62,'change_fieldrehabcomponent'),(247,'Can delete field rehab component',62,'delete_fieldrehabcomponent'),(248,'Can view field rehab component',62,'view_fieldrehabcomponent'),(249,'Can add field rehab phase',63,'add_fieldrehabphase'),(250,'Can change field rehab phase',63,'change_fieldrehabphase'),(251,'Can delete field rehab phase',63,'delete_fieldrehabphase'),(252,'Can view field rehab phase',63,'view_fieldrehabphase'),(253,'Can add rpe training type',64,'add_rpetrainingtype'),(254,'Can change rpe training type',64,'change_rpetrainingtype'),(255,'Can delete rpe training type',64,'delete_rpetrainingtype'),(256,'Can view rpe training type',64,'view_rpetrainingtype'),(257,'Can add player monitoring profile',65,'add_playermonitoringprofile'),(258,'Can change player monitoring profile',65,'change_playermonitoringprofile'),(259,'Can delete player monitoring profile',65,'delete_playermonitoringprofile'),(260,'Can view player monitoring profile',65,'view_playermonitoringprofile'),(261,'Can add player position',66,'add_playerposition'),(262,'Can change player position',66,'change_playerposition'),(263,'Can delete player position',66,'delete_playerposition'),(264,'Can view player position',66,'view_playerposition'),(265,'Can add staff role',67,'add_staffrole'),(266,'Can change staff role',67,'change_staffrole'),(267,'Can delete staff role',67,'delete_staffrole'),(268,'Can view staff role',67,'view_staffrole'),(269,'Can add oefening focus point',68,'add_oefeningfocuspoint'),(270,'Can change oefening focus point',68,'change_oefeningfocuspoint'),(271,'Can delete oefening focus point',68,'delete_oefeningfocuspoint'),(272,'Can view oefening focus point',68,'view_oefeningfocuspoint'),(273,'Can add oefening phase',69,'add_oefeningphase'),(274,'Can change oefening phase',69,'change_oefeningphase'),(275,'Can delete oefening phase',69,'delete_oefeningphase'),(276,'Can view oefening phase',69,'view_oefeningphase'),(277,'Can add oefening program type',70,'add_oefeningprogramtype'),(278,'Can change oefening program type',70,'change_oefeningprogramtype'),(279,'Can delete oefening program type',70,'delete_oefeningprogramtype'),(280,'Can view oefening program type',70,'view_oefeningprogramtype'),(281,'Can add field rehab metric type',71,'add_fieldrehabmetrictype'),(282,'Can change field rehab metric type',71,'change_fieldrehabmetrictype'),(283,'Can delete field rehab metric type',71,'delete_fieldrehabmetrictype'),(284,'Can view field rehab metric type',71,'view_fieldrehabmetrictype'),(285,'Can add Veldrevalidatie metric',72,'add_fieldrehabmetric'),(286,'Can change Veldrevalidatie metric',72,'change_fieldrehabmetric'),(287,'Can delete Veldrevalidatie metric',72,'delete_fieldrehabmetric'),(288,'Can view Veldrevalidatie metric',72,'view_fieldrehabmetric'),(289,'Can add programma frequentie',73,'add_programmafrequentie'),(290,'Can change programma frequentie',73,'change_programmafrequentie'),(291,'Can delete programma frequentie',73,'delete_programmafrequentie'),(292,'Can view programma frequentie',73,'view_programmafrequentie'),(293,'Can add programma duur unit',74,'add_programmaduurunit'),(294,'Can change programma duur unit',74,'change_programmaduurunit'),(295,'Can delete programma duur unit',74,'delete_programmaduurunit'),(296,'Can view programma duur unit',74,'view_programmaduurunit'),(297,'Can add programma oefening naam',75,'add_programmaoefeningnaam'),(298,'Can change programma oefening naam',75,'change_programmaoefeningnaam'),(299,'Can delete programma oefening naam',75,'delete_programmaoefeningnaam'),(300,'Can view programma oefening naam',75,'view_programmaoefeningnaam'),(301,'Can add Snelheidstest (MSS/MAS)',76,'add_playerspeedtest'),(302,'Can change Snelheidstest (MSS/MAS)',76,'change_playerspeedtest'),(303,'Can delete Snelheidstest (MSS/MAS)',76,'delete_playerspeedtest'),(304,'Can view Snelheidstest (MSS/MAS)',76,'view_playerspeedtest'),(305,'Can add HIT ASR planning',77,'add_hitasrplansession'),(306,'Can change HIT ASR planning',77,'change_hitasrplansession'),(307,'Can delete HIT ASR planning',77,'delete_hitasrplansession'),(308,'Can view HIT ASR planning',77,'view_hitasrplansession'),(309,'Can add HIT ASR planning regel',78,'add_hitasrplanentry'),(310,'Can change HIT ASR planning regel',78,'change_hitasrplanentry'),(311,'Can delete HIT ASR planning regel',78,'delete_hitasrplanentry'),(312,'Can view HIT ASR planning regel',78,'view_hitasrplanentry'),(313,'Can add youth guest team',79,'add_youthguestteam'),(314,'Can change youth guest team',79,'change_youthguestteam'),(315,'Can delete youth guest team',79,'delete_youthguestteam'),(316,'Can view youth guest team',79,'view_youthguestteam'),(317,'Can add performance session kind',80,'add_performancesessionkind'),(318,'Can change performance session kind',80,'change_performancesessionkind'),(319,'Can delete performance session kind',80,'delete_performancesessionkind'),(320,'Can view performance session kind',80,'view_performancesessionkind'),(321,'Can add individual day plan note type',81,'add_individualdayplannotetype'),(322,'Can change individual day plan note type',81,'change_individualdayplannotetype'),(323,'Can delete individual day plan note type',81,'delete_individualdayplannotetype'),(324,'Can view individual day plan note type',81,'view_individualdayplannotetype'),(325,'Can add beweeganalyse onderdeel',82,'add_beweeganalyseonderdeel'),(326,'Can change beweeganalyse onderdeel',82,'change_beweeganalyseonderdeel'),(327,'Can delete beweeganalyse onderdeel',82,'delete_beweeganalyseonderdeel'),(328,'Can view beweeganalyse onderdeel',82,'view_beweeganalyseonderdeel'),(329,'Can add beweeganalyse punt',83,'add_beweeganalysepunt'),(330,'Can change beweeganalyse punt',83,'change_beweeganalysepunt'),(331,'Can delete beweeganalyse punt',83,'delete_beweeganalysepunt'),(332,'Can view beweeganalyse punt',83,'view_beweeganalysepunt'),(333,'Can add beweeganalyse sessie',84,'add_beweeganalysesessie'),(334,'Can change beweeganalyse sessie',84,'change_beweeganalysesessie'),(335,'Can delete beweeganalyse sessie',84,'delete_beweeganalysesessie'),(336,'Can view beweeganalyse sessie',84,'view_beweeganalysesessie'),(337,'Can add beweeganalyse beoordeling',85,'add_beweeganalysebeoordeling'),(338,'Can change beweeganalyse beoordeling',85,'change_beweeganalysebeoordeling'),(339,'Can delete beweeganalyse beoordeling',85,'delete_beweeganalysebeoordeling'),(340,'Can view beweeganalyse beoordeling',85,'view_beweeganalysebeoordeling'),(341,'Can add beweeganalyse oefening',86,'add_beweeganalyseoefening'),(342,'Can change beweeganalyse oefening',86,'change_beweeganalyseoefening'),(343,'Can delete beweeganalyse oefening',86,'delete_beweeganalyseoefening'),(344,'Can view beweeganalyse oefening',86,'view_beweeganalyseoefening');
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
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$1000000$pbUij1JS694KI4dHqKXsKf$VeO4hJf7u/PEg8C4v1pa+uvVqd4GVM9yHBXakF7KcSU=','2026-03-10 16:19:17.178864',1,'SiebeHermsen','','','Hermsen.siebe@gmail.com',1,1,'2025-11-07 10:02:59.036236');
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
) ENGINE=InnoDB AUTO_INCREMENT=87 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(21,'main','aanwezigheid'),(43,'main','anthropometrymeasurement'),(44,'main','anthropometrysession'),(27,'main','antropometry'),(20,'main','attendance'),(54,'main','attendancerecord'),(51,'main','attendancestatus'),(85,'main','beweeganalysebeoordeling'),(86,'main','beweeganalyseoefening'),(82,'main','beweeganalyseonderdeel'),(83,'main','beweeganalysepunt'),(84,'main','beweeganalysesessie'),(30,'main','birthday'),(48,'main','birthdayprofile'),(47,'main','birthdayrecord'),(19,'main','dailyprogram'),(8,'main','dayprogram'),(38,'main','dayprogramentry'),(62,'main','fieldrehabcomponent'),(72,'main','fieldrehabmetric'),(71,'main','fieldrehabmetrictype'),(63,'main','fieldrehabphase'),(14,'main','fieldrehabsession'),(35,'main','growthmeasurement'),(36,'main','growthprofile'),(78,'main','hitasrplanentry'),(77,'main','hitasrplansession'),(39,'main','hitweekplan'),(42,'main','hitweekplanentry'),(25,'main','hitweekplanning'),(52,'main','individualdayplan'),(53,'main','individualdayplannote'),(81,'main','individualdayplannotetype'),(9,'main','injury'),(40,'main','injurycase'),(59,'main','injuryphase'),(60,'main','injurystatus'),(61,'main','injurytype'),(28,'main','match'),(26,'main','nutritionday'),(46,'main','nutritionintakeitem'),(45,'main','nutritionintakesession'),(12,'main','oefening'),(68,'main','oefeningfocuspoint'),(69,'main','oefeningphase'),(70,'main','oefeningprogramtype'),(22,'main','overig'),(55,'main','overignote'),(58,'main','performancemetric'),(56,'main','performancemetrictype'),(57,'main','performancesession'),(80,'main','performancesessionkind'),(7,'main','player'),(29,'main','playerintake'),(65,'main','playermonitoringprofile'),(66,'main','playerposition'),(76,'main','playerspeedtest'),(41,'main','playerteamassignment'),(10,'main','playertest'),(18,'main','popgesprek'),(15,'main','programma'),(74,'main','programmaduurunit'),(73,'main','programmafrequentie'),(16,'main','programmaoefening'),(75,'main','programmaoefeningnaam'),(17,'main','rpeentry'),(64,'main','rpetrainingtype'),(23,'main','staff'),(67,'main','staffrole'),(37,'main','team'),(11,'main','trainingdata'),(34,'main','vakantieplanning'),(33,'main','vakantieprogrammaentry'),(24,'main','wedstrijddata'),(32,'main','weightentry'),(13,'main','wellnessentry'),(31,'main','youthguest'),(50,'main','youthguestprofile'),(79,'main','youthguestteam'),(49,'main','youthguestweek'),(6,'sessions','session');
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
) ENGINE=InnoDB AUTO_INCREMENT=136 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-11-07 09:59:01.273167'),(2,'auth','0001_initial','2025-11-07 09:59:02.215760'),(3,'admin','0001_initial','2025-11-07 09:59:02.447028'),(4,'admin','0002_logentry_remove_auto_add','2025-11-07 09:59:02.456437'),(5,'admin','0003_logentry_add_action_flag_choices','2025-11-07 09:59:02.467737'),(6,'contenttypes','0002_remove_content_type_name','2025-11-07 09:59:02.621807'),(7,'auth','0002_alter_permission_name_max_length','2025-11-07 09:59:02.716331'),(8,'auth','0003_alter_user_email_max_length','2025-11-07 09:59:02.775961'),(9,'auth','0004_alter_user_username_opts','2025-11-07 09:59:02.791752'),(10,'auth','0005_alter_user_last_login_null','2025-11-07 09:59:02.871605'),(11,'auth','0006_require_contenttypes_0002','2025-11-07 09:59:02.884029'),(12,'auth','0007_alter_validators_add_error_messages','2025-11-07 09:59:02.899310'),(13,'auth','0008_alter_user_username_max_length','2025-11-07 09:59:03.011237'),(14,'auth','0009_alter_user_last_name_max_length','2025-11-07 09:59:03.123927'),(15,'auth','0010_alter_group_name_max_length','2025-11-07 09:59:03.165424'),(16,'auth','0011_update_proxy_permissions','2025-11-07 09:59:03.171094'),(17,'auth','0012_alter_user_first_name_max_length','2025-11-07 09:59:03.273236'),(20,'sessions','0001_initial','2025-11-07 09:59:03.567841'),(41,'main','0001_initial','2025-11-21 10:26:31.000000'),(42,'main','0002_alter_oefening_options_alter_playertest_options_and_more','2025-11-21 10:28:51.645062'),(43,'main','0003_alter_dailyprogram_date_alter_dailyprogram_player_and_more','2025-11-21 11:32:01.489138'),(44,'main','0004_attendance','2025-11-21 13:27:07.523018'),(45,'main','0005_aanwezigheid_delete_attendance','2025-11-21 14:01:40.362043'),(46,'main','0006_overig_delete_popgesprek','2025-11-24 06:20:04.240248'),(47,'main','0007_remove_overig_player','2025-11-24 06:34:34.367408'),(48,'main','0002_alter_oefening_player','2025-11-25 06:27:04.162291'),(49,'main','0003_wellnessentry','2025-11-25 06:28:06.992208'),(50,'main','0004_alter_wellnessentry_player','2025-11-25 06:28:06.994243'),(51,'main','0005_alter_oefening_player','2025-11-25 06:28:07.003158'),(52,'main','0006_injury_phase','2025-11-25 06:28:07.008121'),(53,'main','0007_player_nutrition_focus','2025-11-25 06:28:07.012159'),(54,'main','0008_playertest_created_at_playertest_curr_weight_and_more','2025-11-25 06:28:07.018541'),(55,'main','0009_alter_oefening_options_alter_playertest_options','2025-11-25 06:28:07.024414'),(56,'main','0010_oefening_focus_point','2025-11-25 06:28:07.029403'),(57,'main','0011_fieldrehabsession','2025-11-25 06:28:07.038012'),(58,'main','0012_programma_programmaoefening','2025-11-25 06:28:07.042317'),(59,'main','0013_player_image','2025-11-25 06:28:07.042317'),(60,'main','0014_rpeentry','2025-11-25 06:28:07.052228'),(61,'main','0015_remove_wellnessentry_rpe_alter_wellnessentry_date_and_more','2025-11-25 06:28:07.055014'),(62,'main','0016_rename_aandachtspunten_popgesprek_belangrijk_and_more','2025-11-25 06:28:07.060922'),(63,'main','0016_auto_20251121_0833','2025-11-25 06:28:07.064206'),(64,'main','0017_merge_20251125_0726','2025-11-25 06:28:07.072393'),(65,'main','0018_staff','2025-11-25 06:28:59.267270'),(66,'main','0019_alter_trainingdata_options_trainingdata_session_date_and_more','2025-11-26 09:46:43.921205'),(67,'main','0020_wedstrijddata','2025-11-26 11:13:45.999164'),(68,'main','0021_player_position_alter_player_name','2025-11-26 13:46:39.739792'),(69,'main','0022_wedstrijddata_accelerations_and_more','2025-11-28 17:22:31.887792'),(70,'main','0023_hitweekplanning','2025-12-05 10:33:11.411195'),(71,'main','0024_alter_hitweekplanning_trainer','2025-12-08 08:23:45.426953'),(72,'main','0025_alter_playertest_options_remove_playertest_name_and_more','2025-12-09 05:33:39.854146'),(73,'main','0026_playertest_length_alter_playertest_cmj_and_more','2025-12-09 05:53:36.457064'),(74,'main','0027_alter_playertest_options_playertest_test_date','2025-12-10 11:59:03.650026'),(75,'main','0028_nutritionday','2025-12-15 15:51:06.934847'),(76,'main','0029_antropometry','2025-12-17 09:27:34.189236'),(77,'main','0030_antropometry_fat_average_antropometry_fat_carter_and_more','2025-12-18 05:47:44.702329'),(78,'main','0031_match','2026-01-20 15:27:40.591848'),(79,'main','0032_alter_nutritionday_color_alter_nutritionday_meal_and_more','2026-02-05 06:22:34.823267'),(80,'main','0033_birthday','2026-02-06 14:45:13.432759'),(81,'main','0034_youthguest_playerintake_supplements','2026-02-06 16:02:29.408290'),(82,'main','0035_youthguest_days','2026-02-06 16:10:44.228043'),(83,'main','0036_remove_youthguest_days_weightentry','2026-02-07 07:02:28.758144'),(84,'main','0037_vakantieprogrammaentry','2026-02-07 11:04:04.258039'),(85,'main','0038_vakantieplanning','2026-02-07 11:22:39.014480'),(86,'main','0039_growthprofile_growthmeasurement','2026-02-17 17:22:29.514620'),(87,'main','0040_3nf_phase1_foundation','2026-02-18 09:15:06.573042'),(88,'main','0041_rename_main_injuryc_player__8c0f5b_idx_main_injury_player__4e7bb7_idx_and_more','2026-02-18 09:15:06.643435'),(89,'main','0042_backfill_3nf_phase1_data','2026-02-18 10:31:10.993447'),(90,'main','0043_backfill_dayprogramentry','2026-02-18 10:39:15.777882'),(91,'main','0044_anthropometrysession_anthropometrymeasurement','2026-02-18 11:00:27.939597'),(92,'main','0045_backfill_anthropometry_v2','2026-02-18 11:00:28.079186'),(93,'main','0046_nutritionintakesession_nutritionintakeitem','2026-02-18 11:47:42.681687'),(94,'main','0047_backfill_nutrition_intake_v2','2026-02-18 11:47:42.695563'),(95,'main','0046_rename_main_anthro_category_3366cb_idx_main_anthro_categor_c3426b_idx','2026-02-18 11:47:42.714992'),(96,'main','0048_merge_0046_rename_and_0047_nutrition','2026-02-18 11:47:42.714992'),(97,'main','0049_deprecate_legacy_tables_preflight','2026-02-18 12:45:31.696773'),(98,'main','0050_birthdayprofile_birthdayrecord_youthguestprofile_youthguestweek','2026-02-18 13:16:17.101707'),(99,'main','0051_backfill_birthday_youthguest_v2','2026-02-18 13:16:17.111766'),(100,'main','0052_drop_legacy_antropometry','2026-02-19 06:10:17.991266'),(101,'main','0053_dailyplan_attendance_3nf','2026-02-19 09:42:59.465445'),(102,'main','0054_overignote_3nf','2026-02-19 18:21:30.161918'),(103,'main','0055_cleanup_legacy_models_phase2','2026-02-20 07:47:06.818841'),(104,'main','0056_performance_session_metric_3nf','2026-02-20 09:28:14.993634'),(105,'main','0057_drop_legacy_performance_models','2026-02-23 10:21:02.512992'),(106,'main','0058_match_team_3nf','2026-02-23 10:21:03.400815'),(107,'main','0059_rename_main_attend_date_1efd36_idx_main_attend_date_35e05c_idx_and_more','2026-02-23 10:21:03.990787'),(108,'main','0059_injurycase_lookup_3nf','2026-02-23 10:54:53.049027'),(109,'main','0060_merge_0059_injury_and_attendance','2026-02-23 10:54:53.053529'),(110,'main','0061_fieldrehabsession_lookup_3nf','2026-02-23 11:00:32.726359'),(111,'main','0062_rpe_training_type_lookup_3nf','2026-02-23 11:06:02.157303'),(112,'main','0063_player_monitoring_profile_3nf','2026-02-25 08:59:53.139137'),(113,'main','0064_player_position_staff_role_lookup_3nf','2026-02-26 07:15:14.611283'),(114,'main','0065_oefening_phase_focus_lookup_3nf','2026-02-26 07:15:15.021518'),(115,'main','0066_fieldrehab_metrics_3nf','2026-02-26 07:15:15.506682'),(116,'main','0067_programma_oefening_frequentie_lookup_3nf','2026-02-26 09:09:08.065396'),(117,'main','0068_programma_oefening_rpe_numeric_3nf','2026-02-26 09:09:08.259979'),(118,'main','0069_programma_oefening_duur_structured_3nf','2026-02-26 09:09:08.747278'),(119,'main','0070_programma_oefening_name_lookup_3nf','2026-02-26 09:09:09.077452'),(120,'main','0071_player_speed_test_3nf','2026-02-26 09:58:27.344085'),(121,'main','0072_hit_asr_planning_3nf','2026-02-26 09:58:27.860407'),(122,'main','0073_youthguest_team_lookup_3nf','2026-03-02 15:55:55.545483'),(123,'main','0074_remove_injurycase_main_injury_player__4e7bb7_idx_and_more','2026-03-03 05:56:08.200361'),(124,'main','0075_performancesessionkind_and_more','2026-03-03 12:15:20.886586'),(125,'main','0076_individualdayplannotetype_and_more','2026-03-03 14:01:06.735543'),(126,'main','0077_nutritionintakesession_uniq_nutri_session_player_date_and_more','2026-03-04 14:59:10.656170'),(127,'main','0078_remove_nutritionintakesession_uniq_nutri_session_player_date_and_more','2026-03-04 15:05:35.030937'),(128,'main','0079_beweeganalyseonderdeel_beweeganalysepunt_and_more','2026-03-06 09:17:50.822045'),(129,'main','0080_seed_beweeganalyse_template','2026-03-06 09:17:50.909934'),(130,'main','0081_beweeganalysesessie_video_file','2026-03-06 11:28:55.182378'),(131,'main','0082_beweeganalysebeoordeling_priority_flag','2026-03-06 11:58:48.239737'),(132,'main','0083_seed_beweeganalyse_medisch','2026-03-06 11:58:48.289951'),(133,'main','0084_beweeganalyseoefening','2026-03-06 13:34:05.843518'),(134,'main','0085_seed_beweeganalyse_oefeningen','2026-03-06 13:34:05.901573'),(135,'main','0086_alter_rpeentry_rpe_alter_wellnessentry_fitness_and_more','2026-03-08 14:09:44.767815');
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
INSERT INTO `django_session` VALUES ('47axpa2unj9fyhfitu3kbh2sasij3hnp','.eJxVjDsOwjAQBe_iGln-yjElPWewdu1dHEC2FCcV4u4QKQW0b2beSyTY1pq2QUuaizgLLU6_G0J-UNtBuUO7dZl7W5cZ5a7Igw557YWel8P9O6gw6rfOQIhI3kWlomGDQaNnbzIYhTZYA-SyIh0dT5QtT8AmakZUPnjWRbw_BHQ4qw:1vLOzo:3nkqSwaLua0EhVgNPjp3j4L0LAOmtYXxTBX_pLNOoTI','2025-12-02 16:56:00.280423'),('awjpbkq4cczun1lu7zizgfc440dnw1b9','.eJxVjDsOwjAQBe_iGln-yjElPWewdu1dHEC2FCcV4u4QKQW0b2beSyTY1pq2QUuaizgLLU6_G0J-UNtBuUO7dZl7W5cZ5a7Igw557YWel8P9O6gw6rfOQIhI3kWlomGDQaNnbzIYhTZYA-SyIh0dT5QtT8AmakZUPnjWRbw_BHQ4qw:1vzznh:moe4UOYoYuVZvqy3FSkehiYbmrpPbZKLlQHaRMiL5rA','2026-03-24 16:19:17.184375');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=167 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_anthropometrymeasurement`
--

LOCK TABLES `main_anthropometrymeasurement` WRITE;
/*!40000 ALTER TABLE `main_anthropometrymeasurement` DISABLE KEYS */;
INSERT INTO `main_anthropometrymeasurement` VALUES (21,'skinfold','triceps',1,8,'2026-02-18 11:00:27.981784',2),(22,'skinfold','triceps',2,8,'2026-02-18 11:00:27.981784',2),(23,'skinfold','biceps',1,8,'2026-02-18 11:00:27.982784',2),(24,'skinfold','biceps',2,8,'2026-02-18 11:00:27.982784',2),(25,'skinfold','subscapular',1,8,'2026-02-18 11:00:27.983782',2),(26,'skinfold','subscapular',2,8,'2026-02-18 11:00:27.984782',2),(27,'skinfold','iliac_crest',1,8,'2026-02-18 11:00:27.984782',2),(28,'skinfold','iliac_crest',2,8,'2026-02-18 11:00:27.985786',2),(29,'skinfold','supraspinale',1,8,'2026-02-18 11:00:27.985786',2),(30,'skinfold','supraspinale',2,8,'2026-02-18 11:00:27.986783',2),(31,'skinfold','abdominal',1,8,'2026-02-18 11:00:27.986783',2),(32,'skinfold','abdominal',2,8,'2026-02-18 11:00:27.987783',2),(33,'skinfold','thigh',1,8,'2026-02-18 11:00:27.987783',2),(34,'skinfold','thigh',2,8,'2026-02-18 11:00:27.988783',2),(35,'skinfold','calf',1,8,'2026-02-18 11:00:27.988783',2),(36,'skinfold','calf',2,8,'2026-02-18 11:00:27.989784',2),(37,'skinfold','triceps',1,8,'2026-02-18 11:00:27.993789',3),(38,'skinfold','triceps',2,8,'2026-02-18 11:00:27.995239',3),(39,'skinfold','biceps',1,9,'2026-02-18 11:00:27.996251',3),(40,'skinfold','biceps',2,9,'2026-02-18 11:00:27.997252',3),(41,'skinfold','subscapular',1,8,'2026-02-18 11:00:27.997252',3),(42,'skinfold','subscapular',2,8,'2026-02-18 11:00:27.998252',3),(43,'skinfold','iliac_crest',1,9,'2026-02-18 11:00:27.998252',3),(44,'skinfold','iliac_crest',2,9,'2026-02-18 11:00:27.999252',3),(45,'skinfold','supraspinale',1,9,'2026-02-18 11:00:27.999252',3),(46,'skinfold','supraspinale',2,9,'2026-02-18 11:00:28.000251',3),(47,'skinfold','abdominal',1,9,'2026-02-18 11:00:28.001251',3),(48,'skinfold','abdominal',2,9,'2026-02-18 11:00:28.001251',3),(49,'skinfold','thigh',1,9,'2026-02-18 11:00:28.002251',3),(50,'skinfold','thigh',2,9,'2026-02-18 11:00:28.003252',3),(51,'skinfold','calf',1,9,'2026-02-18 11:00:28.003252',3),(52,'skinfold','calf',2,9,'2026-02-18 11:00:28.004251',3),(53,'skinfold','triceps',1,8,'2026-02-18 11:00:28.009255',4),(54,'skinfold','triceps',2,8,'2026-02-18 11:00:28.009255',4),(55,'skinfold','biceps',1,8,'2026-02-18 11:00:28.010252',4),(56,'skinfold','biceps',2,8,'2026-02-18 11:00:28.011251',4),(57,'skinfold','subscapular',1,8,'2026-02-18 11:00:28.012254',4),(58,'skinfold','subscapular',2,8,'2026-02-18 11:00:28.012763',4),(59,'skinfold','iliac_crest',1,9,'2026-02-18 11:00:28.012763',4),(60,'skinfold','iliac_crest',2,9,'2026-02-18 11:00:28.013775',4),(61,'skinfold','supraspinale',1,6,'2026-02-18 11:00:28.013775',4),(62,'skinfold','supraspinale',2,6,'2026-02-18 11:00:28.014776',4),(63,'skinfold','abdominal',1,6,'2026-02-18 11:00:28.015783',4),(64,'skinfold','abdominal',2,6,'2026-02-18 11:00:28.015783',4),(65,'skinfold','thigh',1,6,'2026-02-18 11:00:28.016776',4),(66,'skinfold','thigh',2,6,'2026-02-18 11:00:28.016776',4),(67,'skinfold','calf',1,6,'2026-02-18 11:00:28.017776',4),(68,'skinfold','calf',2,6,'2026-02-18 11:00:28.017776',4),(69,'skinfold','triceps',1,9,'2026-02-18 11:00:28.022774',5),(70,'skinfold','triceps',2,9,'2026-02-18 11:00:28.023780',5),(71,'skinfold','biceps',1,6,'2026-02-18 11:00:28.023780',5),(72,'skinfold','biceps',2,6,'2026-02-18 11:00:28.024775',5),(73,'skinfold','subscapular',1,2,'2026-02-18 11:00:28.025977',5),(74,'skinfold','subscapular',2,2,'2026-02-18 11:00:28.025977',5),(75,'skinfold','iliac_crest',1,6,'2026-02-18 11:00:28.026984',5),(76,'skinfold','iliac_crest',2,6,'2026-02-18 11:00:28.027986',5),(77,'skinfold','supraspinale',1,6,'2026-02-18 11:00:28.027986',5),(78,'skinfold','supraspinale',2,6,'2026-02-18 11:00:28.028986',5),(79,'skinfold','abdominal',1,6,'2026-02-18 11:00:28.028986',5),(80,'skinfold','abdominal',2,6,'2026-02-18 11:00:28.029989',5),(81,'skinfold','thigh',1,6,'2026-02-18 11:00:28.030986',5),(82,'skinfold','thigh',2,6,'2026-02-18 11:00:28.031985',5),(83,'skinfold','calf',1,6,'2026-02-18 11:00:28.032986',5),(84,'skinfold','calf',2,6,'2026-02-18 11:00:28.032986',5),(85,'skinfold','triceps',1,8,'2026-02-18 11:00:28.037113',6),(86,'skinfold','triceps',2,8,'2026-02-18 11:00:28.037113',6),(87,'skinfold','biceps',1,10,'2026-02-18 11:00:28.037113',6),(88,'skinfold','biceps',2,10,'2026-02-18 11:00:28.041949',6),(89,'skinfold','subscapular',1,8,'2026-02-18 11:00:28.041949',6),(90,'skinfold','subscapular',2,8,'2026-02-18 11:00:28.041949',6),(91,'skinfold','iliac_crest',1,10,'2026-02-18 11:00:28.041949',6),(92,'skinfold','iliac_crest',2,10,'2026-02-18 11:00:28.043968',6),(93,'skinfold','supraspinale',1,10,'2026-02-18 11:00:28.044708',6),(94,'skinfold','supraspinale',2,10,'2026-02-18 11:00:28.044708',6),(95,'skinfold','abdominal',1,10,'2026-02-18 11:00:28.045727',6),(96,'skinfold','abdominal',2,10,'2026-02-18 11:00:28.046728',6),(97,'skinfold','thigh',1,10,'2026-02-18 11:00:28.046728',6),(98,'skinfold','thigh',2,10,'2026-02-18 11:00:28.047729',6),(99,'skinfold','calf',1,10,'2026-02-18 11:00:28.047729',6),(100,'skinfold','calf',2,10,'2026-02-18 11:00:28.048728',6),(101,'skinfold','triceps',1,9,'2026-02-18 11:00:28.053099',7),(102,'skinfold','triceps',2,9,'2026-02-18 11:00:28.054099',7),(103,'skinfold','biceps',1,8,'2026-02-18 11:00:28.054099',7),(104,'skinfold','biceps',2,9,'2026-02-18 11:00:28.055604',7),(105,'skinfold','biceps',3,9,'2026-02-18 11:00:28.055604',7),(106,'skinfold','subscapular',1,9,'2026-02-18 11:00:28.056610',7),(107,'skinfold','subscapular',2,9,'2026-02-18 11:00:28.056610',7),(108,'skinfold','iliac_crest',1,9,'2026-02-18 11:00:28.057610',7),(109,'skinfold','iliac_crest',2,9,'2026-02-18 11:00:28.057610',7),(110,'skinfold','supraspinale',1,6,'2026-02-18 11:00:28.058610',7),(111,'skinfold','supraspinale',2,6,'2026-02-18 11:00:28.058610',7),(112,'skinfold','abdominal',1,6,'2026-02-18 11:00:28.059610',7),(113,'skinfold','abdominal',2,6,'2026-02-18 11:00:28.059610',7),(114,'skinfold','thigh',1,6,'2026-02-18 11:00:28.060614',7),(115,'skinfold','thigh',2,6,'2026-02-18 11:00:28.060614',7),(116,'skinfold','calf',1,6,'2026-02-18 11:00:28.061727',7),(117,'skinfold','calf',2,6,'2026-02-18 11:00:28.062816',7),(118,'skinfold','triceps',1,6.8,'2026-02-18 11:00:28.066822',8),(119,'skinfold','triceps',2,7,'2026-02-18 11:00:28.066822',8),(120,'skinfold','biceps',1,3.3,'2026-02-18 11:00:28.067814',8),(121,'skinfold','biceps',2,3.2,'2026-02-18 11:00:28.068813',8),(122,'skinfold','subscapular',1,7.8,'2026-02-18 11:00:28.068813',8),(123,'skinfold','subscapular',2,8,'2026-02-18 11:00:28.069827',8),(124,'skinfold','iliac_crest',1,8.2,'2026-02-18 11:00:28.069827',8),(125,'skinfold','iliac_crest',2,8.8,'2026-02-18 11:00:28.070817',8),(126,'skinfold','iliac_crest',3,8.6,'2026-02-18 11:00:28.070817',8),(127,'skinfold','supraspinale',1,5.8,'2026-02-18 11:00:28.071818',8),(128,'skinfold','supraspinale',2,6,'2026-02-18 11:00:28.071818',8),(129,'skinfold','abdominal',1,9,'2026-02-18 11:00:28.072816',8),(130,'skinfold','abdominal',2,8.8,'2026-02-18 11:00:28.072816',8),(131,'skinfold','thigh',1,8.6,'2026-02-18 11:00:28.072816',8),(132,'skinfold','thigh',2,9,'2026-02-18 11:00:28.074814',8),(133,'skinfold','calf',1,4,'2026-02-18 11:00:28.075816',8),(134,'skinfold','calf',2,4,'2026-02-18 11:00:28.075816',8),(135,'skinfold','triceps',1,9,'2026-02-18 11:05:20.782076',9),(136,'skinfold','triceps',2,9,'2026-02-18 11:05:20.782076',9),(137,'skinfold','biceps',1,9,'2026-02-18 11:05:20.782076',9),(138,'skinfold','biceps',2,9,'2026-02-18 11:05:20.790387',9),(139,'skinfold','subscapular',1,9,'2026-02-18 11:05:20.792400',9),(140,'skinfold','subscapular',2,9,'2026-02-18 11:05:20.794412',9),(141,'skinfold','iliac_crest',1,9,'2026-02-18 11:05:20.795790',9),(142,'skinfold','iliac_crest',2,9,'2026-02-18 11:05:20.798720',9),(143,'skinfold','supraspinale',1,9,'2026-02-18 11:05:20.798720',9),(144,'skinfold','supraspinale',2,9,'2026-02-18 11:05:20.798720',9),(145,'skinfold','abdominal',1,9,'2026-02-18 11:05:20.798720',9),(146,'skinfold','abdominal',2,9,'2026-02-18 11:05:20.798720',9),(147,'skinfold','thigh',1,9,'2026-02-18 11:05:20.798720',9),(148,'skinfold','thigh',2,9,'2026-02-18 11:05:20.798720',9),(149,'skinfold','calf',1,9,'2026-02-18 11:05:20.814424',9),(150,'skinfold','calf',2,9,'2026-02-18 11:05:20.815209',9),(151,'skinfold','triceps',1,6,'2026-02-18 13:44:01.048718',1),(152,'skinfold','triceps',2,6,'2026-02-18 13:44:01.052357',1),(153,'skinfold','biceps',1,6,'2026-02-18 13:44:01.054366',1),(154,'skinfold','biceps',2,6,'2026-02-18 13:44:01.056373',1),(155,'skinfold','subscapular',1,6,'2026-02-18 13:44:01.058382',1),(156,'skinfold','subscapular',2,6,'2026-02-18 13:44:01.060391',1),(157,'skinfold','iliac_crest',1,9,'2026-02-18 13:44:01.062400',1),(158,'skinfold','iliac_crest',2,9,'2026-02-18 13:44:01.066979',1),(159,'skinfold','supraspinale',1,9,'2026-02-18 13:44:01.068954',1),(160,'skinfold','supraspinale',2,9,'2026-02-18 13:44:01.068954',1),(161,'skinfold','abdominal',1,9,'2026-02-18 13:44:01.068954',1),(162,'skinfold','abdominal',2,9,'2026-02-18 13:44:01.068954',1),(163,'skinfold','thigh',1,9,'2026-02-18 13:44:01.068954',1),(164,'skinfold','thigh',2,9,'2026-02-18 13:44:01.068954',1),(165,'skinfold','calf',1,9,'2026-02-18 13:44:01.083474',1),(166,'skinfold','calf',2,9,'2026-02-18 13:44:01.084675',1);
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
INSERT INTO `main_anthropometrysession` VALUES (1,'2025-12-17',80,180,11.5,10.4,9.2,10.4,'2026-02-18 11:00:27.959311','2026-02-18 13:44:01.036915',12),(2,'2025-12-17',65,NULL,NULL,NULL,NULL,NULL,'2026-02-18 11:00:27.979311','2026-02-18 11:00:27.979311',21),(3,'2025-12-17',NULL,NULL,NULL,NULL,NULL,NULL,'2026-02-18 11:00:27.992785','2026-02-18 11:00:27.992785',13),(4,'2025-12-17',89,NULL,NULL,NULL,NULL,NULL,'2026-02-18 11:00:28.007251','2026-02-18 11:00:28.007251',28),(5,'2026-01-26',80,NULL,9.6,9.3,7.5,8.8,'2026-02-18 11:00:28.020776','2026-02-18 11:00:28.020776',18),(6,'2026-01-31',NULL,NULL,14.9,11.3,10.6,12.3,'2026-02-18 11:00:28.037113','2026-02-18 11:00:28.037113',18),(7,'2026-02-14',90,190,14.6,10.4,8.9,11.3,'2026-02-18 11:00:28.052103','2026-02-18 11:00:28.052103',18),(8,'2026-01-19',76,NULL,11.1,10.3,8.3,9.9,'2026-02-18 11:00:28.064821','2026-02-18 11:00:28.064821',20),(9,'2026-02-18',80,180,14.9,11.3,10.2,12.1,'2026-02-18 11:05:20.775821','2026-02-18 11:05:20.775821',19);
/*!40000 ALTER TABLE `main_anthropometrysession` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_attendancerecord`
--

DROP TABLE IF EXISTS `main_attendancerecord`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_attendancerecord` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `completed` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `player_id` bigint NOT NULL,
  `status_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_attendance_player_date` (`player_id`,`date`),
  KEY `main_attend_date_35e05c_idx` (`date`,`status_id`),
  KEY `main_attendancerecor_status_id_42502348_fk_main_atte` (`status_id`),
  CONSTRAINT `main_attendancerecor_status_id_42502348_fk_main_atte` FOREIGN KEY (`status_id`) REFERENCES `main_attendancestatus` (`id`),
  CONSTRAINT `main_attendancerecord_player_id_13e466b9_fk_main_player_id` FOREIGN KEY (`player_id`) REFERENCES `main_player` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=897 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_attendancerecord`
--

LOCK TABLES `main_attendancerecord` WRITE;
/*!40000 ALTER TABLE `main_attendancerecord` DISABLE KEYS */;
INSERT INTO `main_attendancerecord` VALUES (1,'2025-11-21',0,'2026-02-19 09:42:57.976472','2026-02-19 09:42:57.976472',1,10),(2,'2025-11-22',0,'2026-02-19 09:42:57.978473','2026-02-19 09:42:57.978473',1,10),(3,'2025-11-24',0,'2026-02-19 09:42:57.979473','2026-02-19 09:42:57.979473',1,10),(4,'2025-11-25',0,'2026-02-19 09:42:57.980471','2026-02-19 09:42:57.980471',1,10),(5,'2025-11-26',0,'2026-02-19 09:42:57.981472','2026-02-19 09:42:57.981472',1,10),(6,'2025-11-28',0,'2026-02-19 09:42:57.983474','2026-02-19 09:42:57.983474',1,10),(7,'2025-11-29',0,'2026-02-19 09:42:57.985481','2026-02-19 09:42:57.985481',1,10),(8,'2025-12-01',0,'2026-02-19 09:42:57.987472','2026-02-19 09:42:57.987472',1,10),(9,'2025-12-02',0,'2026-02-19 09:42:57.988470','2026-02-19 09:42:57.988470',1,10),(10,'2025-12-05',0,'2026-02-19 09:42:57.991554','2026-02-19 09:42:57.991554',1,10),(11,'2025-12-06',0,'2026-02-19 09:42:57.992560','2026-02-19 09:42:57.992560',1,10),(12,'2025-12-08',0,'2026-02-19 09:42:57.994563','2026-02-19 09:42:57.994563',1,10),(13,'2025-12-10',0,'2026-02-19 09:42:57.995569','2026-02-19 09:42:57.995569',1,10),(14,'2025-12-11',0,'2026-02-19 09:42:57.997573','2026-02-19 09:42:57.997573',1,10),(15,'2025-12-12',0,'2026-02-19 09:42:57.999569','2026-02-19 09:42:57.999569',1,10),(16,'2025-12-13',0,'2026-02-19 09:42:58.000571','2026-02-19 09:42:58.000571',1,10),(17,'2025-12-15',0,'2026-02-19 09:42:58.001574','2026-02-19 09:42:58.001574',1,10),(18,'2025-12-17',0,'2026-02-19 09:42:58.003573','2026-02-19 09:42:58.003573',1,10),(19,'2025-12-18',0,'2026-02-19 09:42:58.004569','2026-02-19 09:42:58.004569',1,10),(20,'2026-01-20',0,'2026-02-19 09:42:58.006569','2026-02-19 09:42:58.006569',1,10),(21,'2026-01-26',0,'2026-02-19 09:42:58.008713','2026-02-19 09:42:58.008713',1,10),(22,'2026-02-06',0,'2026-02-19 09:42:58.010604','2026-02-19 09:42:58.010604',1,10),(23,'2026-02-07',0,'2026-02-19 09:42:58.012610','2026-02-19 09:42:58.012610',1,10),(24,'2026-02-12',0,'2026-02-19 09:42:58.014613','2026-02-19 09:42:58.014613',1,10),(25,'2026-02-18',0,'2026-02-19 09:42:58.015656','2026-02-19 09:42:58.015656',1,10),(26,'2025-11-21',0,'2026-02-19 09:42:58.018782','2026-02-19 09:42:58.018782',2,10),(27,'2025-11-22',0,'2026-02-19 09:42:58.022780','2026-02-19 09:42:58.022780',2,10),(28,'2025-11-24',0,'2026-02-19 09:42:58.027073','2026-02-19 09:42:58.027073',2,10),(29,'2025-11-25',0,'2026-02-19 09:42:58.029912','2026-02-19 09:42:58.029912',2,10),(30,'2025-11-26',0,'2026-02-19 09:42:58.031395','2026-02-19 09:42:58.031395',2,10),(31,'2025-11-28',0,'2026-02-19 09:42:58.034135','2026-02-19 09:42:58.034135',2,10),(32,'2025-11-29',0,'2026-02-19 09:42:58.036834','2026-02-19 09:42:58.036834',2,10),(33,'2025-12-01',0,'2026-02-19 09:42:58.038920','2026-02-19 09:42:58.038920',2,10),(34,'2025-12-02',0,'2026-02-19 09:42:58.041008','2026-02-19 09:42:58.041008',2,10),(35,'2025-12-05',0,'2026-02-19 09:42:58.043016','2026-02-19 09:42:58.043016',2,10),(36,'2025-12-06',0,'2026-02-19 09:42:58.045908','2026-02-19 09:42:58.045908',2,10),(37,'2025-12-08',0,'2026-02-19 09:42:58.048471','2026-02-19 09:42:58.048471',2,10),(38,'2025-12-10',0,'2026-02-19 09:42:58.050483','2026-02-19 09:42:58.050483',2,10),(39,'2025-12-11',0,'2026-02-19 09:42:58.052480','2026-02-19 09:42:58.052480',2,10),(40,'2025-12-12',0,'2026-02-19 09:42:58.054481','2026-02-19 09:42:58.054481',2,10),(41,'2025-12-13',0,'2026-02-19 09:42:58.057869','2026-02-19 09:42:58.057869',2,10),(42,'2025-12-15',0,'2026-02-19 09:42:58.059877','2026-02-19 09:42:58.059877',2,10),(43,'2025-12-17',0,'2026-02-19 09:42:58.062276','2026-02-19 09:42:58.062276',2,10),(44,'2025-12-18',0,'2026-02-19 09:42:58.064286','2026-02-19 09:42:58.064286',2,10),(45,'2026-01-20',0,'2026-02-19 09:42:58.066285','2026-02-19 09:42:58.066285',2,10),(46,'2026-01-26',0,'2026-02-19 09:42:58.069287','2026-02-19 09:42:58.069287',2,10),(47,'2026-02-06',0,'2026-02-19 09:42:58.071136','2026-02-19 09:42:58.071136',2,10),(48,'2026-02-07',0,'2026-02-19 09:42:58.074167','2026-02-19 09:42:58.074167',2,10),(49,'2026-02-12',0,'2026-02-19 09:42:58.077086','2026-02-19 09:42:58.077086',2,10),(50,'2026-02-18',0,'2026-02-19 09:42:58.079093','2026-02-19 09:42:58.079093',2,10),(51,'2025-11-21',0,'2026-02-19 09:42:58.083522','2026-02-19 09:42:58.083522',3,10),(52,'2025-11-22',0,'2026-02-19 09:42:58.085825','2026-02-19 09:42:58.085825',3,10),(53,'2025-11-24',0,'2026-02-19 09:42:58.097519','2026-02-19 09:42:58.097519',3,10),(54,'2025-11-25',0,'2026-02-19 09:42:58.101073','2026-02-19 09:42:58.101073',3,10),(55,'2025-11-26',0,'2026-02-19 09:42:58.103075','2026-02-19 09:42:58.103075',3,10),(56,'2025-11-28',0,'2026-02-19 09:42:58.105074','2026-02-19 09:42:58.105074',3,10),(57,'2025-11-29',0,'2026-02-19 09:42:58.107800','2026-02-19 09:42:58.107800',3,10),(58,'2025-12-01',0,'2026-02-19 09:42:58.109800','2026-02-19 09:42:58.109800',3,10),(59,'2025-12-02',0,'2026-02-19 09:42:58.112322','2026-02-19 09:42:58.112322',3,10),(60,'2025-12-05',0,'2026-02-19 09:42:58.114323','2026-02-19 09:42:58.114323',3,10),(61,'2025-12-06',0,'2026-02-19 09:42:58.115322','2026-02-19 09:42:58.115322',3,10),(62,'2025-12-08',0,'2026-02-19 09:42:58.117323','2026-02-19 09:42:58.117323',3,10),(63,'2025-12-10',0,'2026-02-19 09:42:58.119330','2026-02-19 09:42:58.119330',3,10),(64,'2025-12-11',0,'2026-02-19 09:42:58.121321','2026-02-19 09:42:58.121321',3,10),(65,'2025-12-12',0,'2026-02-19 09:42:58.123324','2026-02-19 09:42:58.123324',3,10),(66,'2025-12-13',0,'2026-02-19 09:42:58.124720','2026-02-19 09:42:58.124720',3,10),(67,'2025-12-15',0,'2026-02-19 09:42:58.127079','2026-02-19 09:42:58.127079',3,10),(68,'2025-12-17',0,'2026-02-19 09:42:58.129077','2026-02-19 09:42:58.129077',3,10),(69,'2025-12-18',0,'2026-02-19 09:42:58.131080','2026-02-19 09:42:58.131080',3,10),(70,'2026-01-20',0,'2026-02-19 09:42:58.133081','2026-02-19 09:42:58.133081',3,10),(71,'2026-01-26',0,'2026-02-19 09:42:58.134082','2026-02-19 09:42:58.134082',3,10),(72,'2026-02-06',0,'2026-02-19 09:42:58.137077','2026-02-19 09:42:58.137077',3,10),(73,'2026-02-07',0,'2026-02-19 09:42:58.139075','2026-02-19 09:42:58.139075',3,10),(74,'2026-02-12',0,'2026-02-19 09:42:58.141081','2026-02-19 09:42:58.141081',3,10),(75,'2026-02-18',0,'2026-02-19 09:42:58.143080','2026-02-19 09:42:58.143080',3,10),(76,'2025-11-21',0,'2026-02-19 09:42:58.148084','2026-02-19 09:42:58.148084',4,10),(77,'2025-11-22',0,'2026-02-19 09:42:58.149084','2026-02-19 09:42:58.149084',4,10),(78,'2025-11-24',0,'2026-02-19 09:42:58.151085','2026-02-19 09:42:58.151085',4,10),(79,'2025-11-25',0,'2026-02-19 09:42:58.153085','2026-02-19 09:42:58.153085',4,10),(80,'2025-11-26',0,'2026-02-19 09:42:58.154084','2026-02-19 09:42:58.154084',4,10),(81,'2025-11-28',0,'2026-02-19 09:42:58.156577','2026-02-19 09:42:58.156577',4,10),(82,'2025-11-29',0,'2026-02-19 09:42:58.158007','2026-02-19 09:42:58.158007',4,10),(83,'2025-12-01',0,'2026-02-19 09:42:58.161810','2026-02-19 09:42:58.161810',4,10),(84,'2025-12-02',0,'2026-02-19 09:42:58.162814','2026-02-19 09:42:58.162814',4,10),(85,'2025-12-05',0,'2026-02-19 09:42:58.164807','2026-02-19 09:42:58.164807',4,10),(86,'2025-12-06',0,'2026-02-19 09:42:58.166811','2026-02-19 09:42:58.166811',4,10),(87,'2025-12-08',0,'2026-02-19 09:42:58.167809','2026-02-19 09:42:58.167809',4,10),(88,'2025-12-10',0,'2026-02-19 09:42:58.169821','2026-02-19 09:42:58.169821',4,10),(89,'2025-12-11',0,'2026-02-19 09:42:58.171806','2026-02-19 09:42:58.171806',4,10),(90,'2025-12-12',0,'2026-02-19 09:42:58.175361','2026-02-19 09:42:58.175361',4,10),(91,'2025-12-13',0,'2026-02-19 09:42:58.177359','2026-02-19 09:42:58.177359',4,10),(92,'2025-12-15',0,'2026-02-19 09:42:58.179358','2026-02-19 09:42:58.179358',4,10),(93,'2025-12-17',0,'2026-02-19 09:42:58.181360','2026-02-19 09:42:58.181360',4,10),(94,'2025-12-18',0,'2026-02-19 09:42:58.182356','2026-02-19 09:42:58.182356',4,10),(95,'2026-01-20',0,'2026-02-19 09:42:58.184357','2026-02-19 09:42:58.184357',4,10),(96,'2026-01-26',0,'2026-02-19 09:42:58.185356','2026-02-19 09:42:58.185356',4,10),(97,'2026-02-06',0,'2026-02-19 09:42:58.187357','2026-02-19 09:42:58.187357',4,10),(98,'2026-02-07',0,'2026-02-19 09:42:58.189356','2026-02-19 09:42:58.189356',4,10),(99,'2026-02-12',0,'2026-02-19 09:42:58.191135','2026-02-19 09:42:58.191135',4,10),(100,'2026-02-18',0,'2026-02-19 09:42:58.194135','2026-02-19 09:42:58.194135',4,10),(101,'2025-11-21',0,'2026-02-19 09:42:58.198144','2026-02-19 09:42:58.198144',5,10),(102,'2025-11-22',0,'2026-02-19 09:42:58.199142','2026-02-19 09:42:58.199142',5,10),(103,'2025-11-24',0,'2026-02-19 09:42:58.200144','2026-02-19 09:42:58.201143',5,10),(104,'2025-11-25',0,'2026-02-19 09:42:58.202146','2026-02-19 09:42:58.202146',5,10),(105,'2025-11-26',0,'2026-02-19 09:42:58.204143','2026-02-19 09:42:58.204143',5,10),(106,'2025-11-28',0,'2026-02-19 09:42:58.206187','2026-02-19 09:42:58.206187',5,10),(107,'2025-11-29',0,'2026-02-19 09:42:58.208596','2026-02-19 09:42:58.208596',5,10),(108,'2025-12-01',0,'2026-02-19 09:42:58.209597','2026-02-19 09:42:58.209597',5,10),(109,'2025-12-02',0,'2026-02-19 09:42:58.211107','2026-02-19 09:42:58.211107',5,10),(110,'2025-12-05',0,'2026-02-19 09:42:58.213120','2026-02-19 09:42:58.213120',5,10),(111,'2025-12-06',0,'2026-02-19 09:42:58.215119','2026-02-19 09:42:58.215119',5,10),(112,'2025-12-08',0,'2026-02-19 09:42:58.216118','2026-02-19 09:42:58.216118',5,10),(113,'2025-12-10',0,'2026-02-19 09:42:58.218119','2026-02-19 09:42:58.218119',5,10),(114,'2025-12-11',0,'2026-02-19 09:42:58.219119','2026-02-19 09:42:58.219119',5,10),(115,'2025-12-12',0,'2026-02-19 09:42:58.223117','2026-02-19 09:42:58.223117',5,10),(116,'2025-12-13',0,'2026-02-19 09:42:58.225380','2026-02-19 09:42:58.225380',5,10),(117,'2025-12-15',0,'2026-02-19 09:42:58.227381','2026-02-19 09:42:58.227381',5,10),(118,'2025-12-17',0,'2026-02-19 09:42:58.228381','2026-02-19 09:42:58.228381',5,10),(119,'2025-12-18',0,'2026-02-19 09:42:58.230381','2026-02-19 09:42:58.230381',5,10),(120,'2026-01-20',0,'2026-02-19 09:42:58.231381','2026-02-19 09:42:58.231381',5,10),(121,'2026-01-26',0,'2026-02-19 09:42:58.233381','2026-02-19 09:42:58.233381',5,10),(122,'2026-02-06',0,'2026-02-19 09:42:58.234380','2026-02-19 09:42:58.234380',5,10),(123,'2026-02-07',0,'2026-02-19 09:42:58.236380','2026-02-19 09:42:58.236380',5,10),(124,'2026-02-12',0,'2026-02-19 09:42:58.237381','2026-02-19 09:42:58.237381',5,10),(125,'2026-02-18',0,'2026-02-19 09:42:58.239379','2026-02-19 09:42:58.239379',5,10),(126,'2025-11-21',0,'2026-02-19 09:42:58.247129','2026-02-19 09:42:58.247129',6,10),(127,'2025-11-22',0,'2026-02-19 09:42:58.248130','2026-02-19 09:42:58.248130',6,10),(128,'2025-11-24',0,'2026-02-19 09:42:58.250126','2026-02-19 09:42:58.250126',6,10),(129,'2025-11-25',0,'2026-02-19 09:42:58.252133','2026-02-19 09:42:58.252133',6,10),(130,'2025-11-26',0,'2026-02-19 09:42:58.254165','2026-02-19 09:42:58.254165',6,10),(131,'2025-11-28',0,'2026-02-19 09:42:58.257129','2026-02-19 09:42:58.257129',6,10),(132,'2025-11-29',0,'2026-02-19 09:42:58.258826','2026-02-19 09:42:58.258826',6,10),(133,'2025-12-01',0,'2026-02-19 09:42:58.260820','2026-02-19 09:42:58.260820',6,10),(134,'2025-12-02',0,'2026-02-19 09:42:58.262822','2026-02-19 09:42:58.262822',6,10),(135,'2025-12-05',0,'2026-02-19 09:42:58.264045','2026-02-19 09:42:58.264045',6,10),(136,'2025-12-06',0,'2026-02-19 09:42:58.266058','2026-02-19 09:42:58.266058',6,10),(137,'2025-12-08',0,'2026-02-19 09:42:58.267056','2026-02-19 09:42:58.267056',6,10),(138,'2025-12-10',0,'2026-02-19 09:42:58.268056','2026-02-19 09:42:58.268056',6,10),(139,'2025-12-11',0,'2026-02-19 09:42:58.270058','2026-02-19 09:42:58.270058',6,10),(140,'2025-12-12',0,'2026-02-19 09:42:58.271058','2026-02-19 09:42:58.271058',6,10),(141,'2025-12-13',0,'2026-02-19 09:42:58.272061','2026-02-19 09:42:58.272061',6,10),(142,'2025-12-15',0,'2026-02-19 09:42:58.274978','2026-02-19 09:42:58.274978',6,10),(143,'2025-12-17',0,'2026-02-19 09:42:58.276987','2026-02-19 09:42:58.276987',6,10),(144,'2025-12-18',0,'2026-02-19 09:42:58.277987','2026-02-19 09:42:58.277987',6,10),(145,'2026-01-20',0,'2026-02-19 09:42:58.279989','2026-02-19 09:42:58.279989',6,10),(146,'2026-01-26',0,'2026-02-19 09:42:58.281988','2026-02-19 09:42:58.281988',6,10),(147,'2026-02-06',0,'2026-02-19 09:42:58.282988','2026-02-19 09:42:58.282988',6,10),(148,'2026-02-07',0,'2026-02-19 09:42:58.285986','2026-02-19 09:42:58.285986',6,10),(149,'2026-02-12',0,'2026-02-19 09:42:58.286988','2026-02-19 09:42:58.286988',6,10),(150,'2026-02-18',0,'2026-02-19 09:42:58.289905','2026-02-19 09:42:58.289905',6,10),(151,'2025-11-21',0,'2026-02-19 09:42:58.297083','2026-02-19 09:42:58.297083',7,10),(152,'2025-11-22',0,'2026-02-19 09:42:58.298080','2026-02-19 09:42:58.298080',7,10),(153,'2025-11-24',0,'2026-02-19 09:42:58.300080','2026-02-19 09:42:58.300080',7,10),(154,'2025-11-25',0,'2026-02-19 09:42:58.301080','2026-02-19 09:42:58.301080',7,10),(155,'2025-11-26',0,'2026-02-19 09:42:58.302082','2026-02-19 09:42:58.302082',7,10),(156,'2025-11-28',0,'2026-02-19 09:42:58.303081','2026-02-19 09:42:58.304080',7,10),(157,'2025-11-29',0,'2026-02-19 09:42:58.305080','2026-02-19 09:42:58.305080',7,10),(158,'2025-12-01',0,'2026-02-19 09:42:58.307823','2026-02-19 09:42:58.307823',7,10),(159,'2025-12-02',0,'2026-02-19 09:42:58.309875','2026-02-19 09:42:58.309875',7,10),(160,'2025-12-05',0,'2026-02-19 09:42:58.311387','2026-02-19 09:42:58.311387',7,10),(161,'2025-12-06',0,'2026-02-19 09:42:58.312402','2026-02-19 09:42:58.312402',7,10),(162,'2025-12-08',0,'2026-02-19 09:42:58.314403','2026-02-19 09:42:58.314403',7,10),(163,'2025-12-10',0,'2026-02-19 09:42:58.315401','2026-02-19 09:42:58.315401',7,10),(164,'2025-12-11',0,'2026-02-19 09:42:58.316403','2026-02-19 09:42:58.316403',7,10),(165,'2025-12-12',0,'2026-02-19 09:42:58.319420','2026-02-19 09:42:58.319420',7,10),(166,'2025-12-13',0,'2026-02-19 09:42:58.320440','2026-02-19 09:42:58.320440',7,10),(167,'2025-12-15',0,'2026-02-19 09:42:58.321440','2026-02-19 09:42:58.321440',7,10),(168,'2025-12-17',0,'2026-02-19 09:42:58.323439','2026-02-19 09:42:58.323439',7,10),(169,'2025-12-18',0,'2026-02-19 09:42:58.325470','2026-02-19 09:42:58.325470',7,10),(170,'2026-01-20',0,'2026-02-19 09:42:58.327471','2026-02-19 09:42:58.327471',7,10),(171,'2026-01-26',0,'2026-02-19 09:42:58.328468','2026-02-19 09:42:58.328468',7,10),(172,'2026-02-06',0,'2026-02-19 09:42:58.330474','2026-02-19 09:42:58.330474',7,10),(173,'2026-02-07',0,'2026-02-19 09:42:58.331474','2026-02-19 09:42:58.331474',7,10),(174,'2026-02-12',0,'2026-02-19 09:42:58.334112','2026-02-19 09:42:58.334112',7,10),(175,'2026-02-18',0,'2026-02-19 09:42:58.335130','2026-02-19 09:42:58.335130',7,10),(176,'2025-11-21',0,'2026-02-19 09:42:58.338133','2026-02-19 09:42:58.338133',8,10),(177,'2025-11-22',0,'2026-02-19 09:42:58.340133','2026-02-19 09:42:58.340133',8,10),(178,'2025-11-24',0,'2026-02-19 09:42:58.342727','2026-02-19 09:42:58.342727',8,10),(179,'2025-11-25',0,'2026-02-19 09:42:58.343727','2026-02-19 09:42:58.343727',8,10),(180,'2025-11-26',0,'2026-02-19 09:42:58.345732','2026-02-19 09:42:58.345732',8,10),(181,'2025-11-28',0,'2026-02-19 09:42:58.347727','2026-02-19 09:42:58.347727',8,10),(182,'2025-11-29',0,'2026-02-19 09:42:58.348726','2026-02-19 09:42:58.348726',8,10),(183,'2025-12-01',0,'2026-02-19 09:42:58.350728','2026-02-19 09:42:58.350728',8,10),(184,'2025-12-02',0,'2026-02-19 09:42:58.351729','2026-02-19 09:42:58.351729',8,10),(185,'2025-12-05',0,'2026-02-19 09:42:58.352730','2026-02-19 09:42:58.352730',8,10),(186,'2025-12-06',0,'2026-02-19 09:42:58.354730','2026-02-19 09:42:58.354730',8,10),(187,'2025-12-08',0,'2026-02-19 09:42:58.356575','2026-02-19 09:42:58.356575',8,10),(188,'2025-12-10',0,'2026-02-19 09:42:58.358845','2026-02-19 09:42:58.358845',8,10),(189,'2025-12-11',0,'2026-02-19 09:42:58.359858','2026-02-19 09:42:58.359858',8,10),(190,'2025-12-12',0,'2026-02-19 09:42:58.360858','2026-02-19 09:42:58.360858',8,10),(191,'2025-12-13',0,'2026-02-19 09:42:58.361858','2026-02-19 09:42:58.361858',8,10),(192,'2025-12-15',0,'2026-02-19 09:42:58.362862','2026-02-19 09:42:58.362862',8,10),(193,'2025-12-17',0,'2026-02-19 09:42:58.363859','2026-02-19 09:42:58.363859',8,10),(194,'2025-12-18',0,'2026-02-19 09:42:58.364860','2026-02-19 09:42:58.365865',8,10),(195,'2026-01-20',0,'2026-02-19 09:42:58.366859','2026-02-19 09:42:58.366859',8,10),(196,'2026-01-26',0,'2026-02-19 09:42:58.367857','2026-02-19 09:42:58.367857',8,10),(197,'2026-02-06',0,'2026-02-19 09:42:58.368859','2026-02-19 09:42:58.368859',8,10),(198,'2026-02-07',0,'2026-02-19 09:42:58.369858','2026-02-19 09:42:58.369858',8,10),(199,'2026-02-12',0,'2026-02-19 09:42:58.371861','2026-02-19 09:42:58.371861',8,10),(200,'2026-02-18',0,'2026-02-19 09:42:58.374326','2026-02-19 09:42:58.374326',8,10),(201,'2025-11-21',0,'2026-02-19 09:42:58.381441','2026-02-19 09:42:58.381441',9,10),(202,'2025-11-22',0,'2026-02-19 09:42:58.383442','2026-02-19 09:42:58.383442',9,10),(203,'2025-11-24',0,'2026-02-19 09:42:58.385445','2026-02-19 09:42:58.385445',9,10),(204,'2025-11-25',0,'2026-02-19 09:42:58.386446','2026-02-19 09:42:58.386446',9,10),(205,'2025-11-26',0,'2026-02-19 09:42:58.388447','2026-02-19 09:42:58.388447',9,10),(206,'2025-11-28',0,'2026-02-19 09:42:58.389953','2026-02-19 09:42:58.389953',9,10),(207,'2025-11-29',0,'2026-02-19 09:42:58.392078','2026-02-19 09:42:58.392078',9,10),(208,'2025-12-01',0,'2026-02-19 09:42:58.394076','2026-02-19 09:42:58.394076',9,10),(209,'2025-12-02',0,'2026-02-19 09:42:58.395076','2026-02-19 09:42:58.396077',9,10),(210,'2025-12-05',0,'2026-02-19 09:42:58.397085','2026-02-19 09:42:58.397085',9,10),(211,'2025-12-06',0,'2026-02-19 09:42:58.398085','2026-02-19 09:42:58.398085',9,10),(212,'2025-12-08',0,'2026-02-19 09:42:58.401092','2026-02-19 09:42:58.401092',9,10),(213,'2025-12-10',0,'2026-02-19 09:42:58.402084','2026-02-19 09:42:58.402084',9,10),(214,'2025-12-11',0,'2026-02-19 09:42:58.404087','2026-02-19 09:42:58.404087',9,10),(215,'2025-12-12',0,'2026-02-19 09:42:58.406086','2026-02-19 09:42:58.406086',9,10),(216,'2025-12-13',0,'2026-02-19 09:42:58.407721','2026-02-19 09:42:58.407721',9,10),(217,'2025-12-15',0,'2026-02-19 09:42:58.409857','2026-02-19 09:42:58.409857',9,10),(218,'2025-12-17',0,'2026-02-19 09:42:58.411372','2026-02-19 09:42:58.411372',9,10),(219,'2025-12-18',0,'2026-02-19 09:42:58.412386','2026-02-19 09:42:58.412386',9,10),(220,'2026-01-20',0,'2026-02-19 09:42:58.414382','2026-02-19 09:42:58.414382',9,10),(221,'2026-01-26',0,'2026-02-19 09:42:58.416379','2026-02-19 09:42:58.416379',9,10),(222,'2026-02-06',0,'2026-02-19 09:42:58.417380','2026-02-19 09:42:58.417380',9,10),(223,'2026-02-07',0,'2026-02-19 09:42:58.419382','2026-02-19 09:42:58.419382',9,10),(224,'2026-02-12',0,'2026-02-19 09:42:58.420380','2026-02-19 09:42:58.421380',9,10),(225,'2026-02-18',0,'2026-02-19 09:42:58.422380','2026-02-19 09:42:58.422380',9,10),(226,'2025-11-21',0,'2026-02-19 09:42:58.426342','2026-02-19 09:42:58.426342',10,10),(227,'2025-11-22',0,'2026-02-19 09:42:58.427340','2026-02-19 09:42:58.427340',10,10),(228,'2025-11-24',0,'2026-02-19 09:42:58.428340','2026-02-19 09:42:58.428340',10,10),(229,'2025-11-25',0,'2026-02-19 09:42:58.430340','2026-02-19 09:42:58.430340',10,10),(230,'2025-11-26',0,'2026-02-19 09:42:58.431340','2026-02-19 09:42:58.431340',10,10),(231,'2025-11-28',0,'2026-02-19 09:42:58.432343','2026-02-19 09:42:58.432343',10,10),(232,'2025-11-29',0,'2026-02-19 09:42:58.433340','2026-02-19 09:42:58.433340',10,10),(233,'2025-12-01',0,'2026-02-19 09:42:58.435342','2026-02-19 09:42:58.435342',10,10),(234,'2025-12-02',0,'2026-02-19 09:42:58.436342','2026-02-19 09:42:58.436342',10,10),(235,'2025-12-05',0,'2026-02-19 09:42:58.437341','2026-02-19 09:42:58.437341',10,10),(236,'2025-12-06',0,'2026-02-19 09:42:58.439341','2026-02-19 09:42:58.440342',10,10),(237,'2025-12-08',0,'2026-02-19 09:42:58.441921','2026-02-19 09:42:58.441921',10,10),(238,'2025-12-10',0,'2026-02-19 09:42:58.443918','2026-02-19 09:42:58.443918',10,10),(239,'2025-12-11',0,'2026-02-19 09:42:58.444920','2026-02-19 09:42:58.444920',10,10),(240,'2025-12-12',0,'2026-02-19 09:42:58.445918','2026-02-19 09:42:58.445918',10,10),(241,'2025-12-13',0,'2026-02-19 09:42:58.447920','2026-02-19 09:42:58.447920',10,10),(242,'2025-12-15',0,'2026-02-19 09:42:58.448920','2026-02-19 09:42:58.448920',10,10),(243,'2025-12-17',0,'2026-02-19 09:42:58.450919','2026-02-19 09:42:58.450919',10,10),(244,'2025-12-18',0,'2026-02-19 09:42:58.451919','2026-02-19 09:42:58.451919',10,10),(245,'2026-01-20',0,'2026-02-19 09:42:58.454918','2026-02-19 09:42:58.454918',10,10),(246,'2026-01-26',0,'2026-02-19 09:42:58.456496','2026-02-19 09:42:58.456496',10,10),(247,'2026-02-06',0,'2026-02-19 09:42:58.458608','2026-02-19 09:42:58.458608',10,10),(248,'2026-02-07',0,'2026-02-19 09:42:58.460612','2026-02-19 09:42:58.460612',10,10),(249,'2026-02-12',0,'2026-02-19 09:42:58.461611','2026-02-19 09:42:58.461611',10,10),(250,'2026-02-18',0,'2026-02-19 09:42:58.462613','2026-02-19 09:42:58.462613',10,10),(251,'2025-11-21',0,'2026-02-19 09:42:58.466612','2026-02-19 09:42:58.466612',11,10),(252,'2025-11-22',0,'2026-02-19 09:42:58.467611','2026-02-19 09:42:58.467611',11,10),(253,'2025-11-24',0,'2026-02-19 09:42:58.469608','2026-02-19 09:42:58.469608',11,10),(254,'2025-11-25',0,'2026-02-19 09:42:58.472609','2026-02-19 09:42:58.472609',11,10),(255,'2025-11-26',0,'2026-02-19 09:42:58.474351','2026-02-19 09:42:58.474351',11,10),(256,'2025-11-28',0,'2026-02-19 09:42:58.476478','2026-02-19 09:42:58.476478',11,10),(257,'2025-11-29',0,'2026-02-19 09:42:58.477478','2026-02-19 09:42:58.477478',11,10),(258,'2025-12-01',0,'2026-02-19 09:42:58.480475','2026-02-19 09:42:58.480475',11,10),(259,'2025-12-02',0,'2026-02-19 09:42:58.481474','2026-02-19 09:42:58.481474',11,10),(260,'2025-12-05',0,'2026-02-19 09:42:58.483473','2026-02-19 09:42:58.483473',11,10),(261,'2025-12-06',0,'2026-02-19 09:42:58.484473','2026-02-19 09:42:58.484473',11,10),(262,'2025-12-08',0,'2026-02-19 09:42:58.486475','2026-02-19 09:42:58.486475',11,10),(263,'2025-12-10',0,'2026-02-19 09:42:58.487475','2026-02-19 09:42:58.487475',11,10),(264,'2025-12-11',0,'2026-02-19 09:42:58.488474','2026-02-19 09:42:58.488474',11,10),(265,'2025-12-12',0,'2026-02-19 09:42:58.489852','2026-02-19 09:42:58.489852',11,10),(266,'2025-12-13',0,'2026-02-19 09:42:58.491962','2026-02-19 09:42:58.491962',11,10),(267,'2025-12-15',0,'2026-02-19 09:42:58.492965','2026-02-19 09:42:58.492965',11,10),(268,'2025-12-17',0,'2026-02-19 09:42:58.494964','2026-02-19 09:42:58.494964',11,10),(269,'2025-12-18',0,'2026-02-19 09:42:58.495965','2026-02-19 09:42:58.495965',11,10),(270,'2026-01-20',0,'2026-02-19 09:42:58.497972','2026-02-19 09:42:58.497972',11,10),(271,'2026-01-26',0,'2026-02-19 09:42:58.499971','2026-02-19 09:42:58.499971',11,10),(272,'2026-02-06',0,'2026-02-19 09:42:58.501244','2026-02-19 09:42:58.501244',11,10),(273,'2026-02-07',0,'2026-02-19 09:42:58.501244','2026-02-19 09:42:58.501244',11,10),(274,'2026-02-12',0,'2026-02-19 09:42:58.501244','2026-02-19 09:42:58.501244',11,10),(275,'2026-02-18',0,'2026-02-19 09:42:58.507617','2026-02-19 09:42:58.507617',11,10),(276,'2025-11-21',0,'2026-02-19 09:42:58.511620','2026-02-19 09:42:58.511620',12,10),(277,'2025-11-22',0,'2026-02-19 09:42:58.513141','2026-02-19 09:42:58.513141',12,10),(278,'2025-11-24',0,'2026-02-19 09:42:58.514146','2026-02-19 09:42:58.514146',12,10),(279,'2025-11-25',0,'2026-02-19 09:42:58.515145','2026-02-19 09:42:58.515145',12,10),(280,'2025-11-26',0,'2026-02-19 09:42:58.516143','2026-02-19 09:42:58.516143',12,10),(281,'2025-11-28',0,'2026-02-19 09:42:58.517143','2026-02-19 09:42:58.517143',12,10),(282,'2025-11-29',0,'2026-02-19 09:42:58.518146','2026-02-19 09:42:58.518146',12,10),(283,'2025-12-01',0,'2026-02-19 09:42:58.519142','2026-02-19 09:42:58.519142',12,10),(284,'2025-12-02',0,'2026-02-19 09:42:58.520142','2026-02-19 09:42:58.520142',12,10),(285,'2025-12-05',0,'2026-02-19 09:42:58.522143','2026-02-19 09:42:58.522143',12,10),(286,'2025-12-06',0,'2026-02-19 09:42:58.524664','2026-02-19 09:42:58.524664',12,10),(287,'2025-12-08',0,'2026-02-19 09:42:58.526749','2026-02-19 09:42:58.526749',12,10),(288,'2025-12-10',0,'2026-02-19 09:42:58.528748','2026-02-19 09:42:58.528748',12,10),(289,'2025-12-11',0,'2026-02-19 09:42:58.529748','2026-02-19 09:42:58.529748',12,10),(290,'2025-12-12',0,'2026-02-19 09:42:58.530750','2026-02-19 09:42:58.530750',12,10),(291,'2025-12-13',0,'2026-02-19 09:42:58.531748','2026-02-19 09:42:58.531748',12,10),(292,'2025-12-15',0,'2026-02-19 09:42:58.532749','2026-02-19 09:42:58.532749',12,10),(293,'2025-12-17',0,'2026-02-19 09:42:58.533750','2026-02-19 09:42:58.533750',12,10),(294,'2025-12-18',0,'2026-02-19 09:42:58.535748','2026-02-19 09:42:58.535748',12,10),(295,'2026-01-20',0,'2026-02-19 09:42:58.536749','2026-02-19 09:42:58.536749',12,10),(296,'2026-01-26',0,'2026-02-19 09:42:58.537748','2026-02-19 09:42:58.537748',12,10),(297,'2026-02-06',0,'2026-02-19 09:42:58.539748','2026-02-19 09:42:58.539748',12,10),(298,'2026-02-07',0,'2026-02-19 09:42:58.539748','2026-02-19 09:42:58.539748',12,10),(299,'2026-02-12',0,'2026-02-19 09:42:58.539748','2026-02-19 09:42:58.539748',12,10),(300,'2026-02-18',0,'2026-02-19 09:42:58.539748','2026-02-19 09:42:58.539748',12,10),(301,'2025-11-21',0,'2026-02-19 09:42:58.539748','2026-02-19 09:42:58.539748',13,10),(302,'2025-11-22',0,'2026-02-19 09:42:58.539748','2026-02-19 09:42:58.539748',13,10),(303,'2025-11-24',0,'2026-02-19 09:42:58.539748','2026-02-19 09:42:58.539748',13,10),(304,'2025-11-25',0,'2026-02-19 09:42:58.539748','2026-02-19 09:42:58.539748',13,10),(305,'2025-11-26',0,'2026-02-19 09:42:58.539748','2026-02-19 09:42:58.539748',13,10),(306,'2025-11-28',0,'2026-02-19 09:42:58.539748','2026-02-19 09:42:58.539748',13,10),(307,'2025-11-29',0,'2026-02-19 09:42:58.539748','2026-02-19 09:42:58.539748',13,10),(308,'2025-12-01',0,'2026-02-19 09:42:58.555496','2026-02-19 09:42:58.555496',13,10),(309,'2025-12-02',0,'2026-02-19 09:42:58.555496','2026-02-19 09:42:58.555496',13,10),(310,'2025-12-05',0,'2026-02-19 09:42:58.555496','2026-02-19 09:42:58.555496',13,10),(311,'2025-12-06',0,'2026-02-19 09:42:58.555496','2026-02-19 09:42:58.555496',13,10),(312,'2025-12-08',0,'2026-02-19 09:42:58.555496','2026-02-19 09:42:58.555496',13,10),(313,'2025-12-10',0,'2026-02-19 09:42:58.555496','2026-02-19 09:42:58.555496',13,10),(314,'2025-12-11',0,'2026-02-19 09:42:58.555496','2026-02-19 09:42:58.555496',13,10),(315,'2025-12-12',0,'2026-02-19 09:42:58.555496','2026-02-19 09:42:58.555496',13,10),(316,'2025-12-13',0,'2026-02-19 09:42:58.555496','2026-02-19 09:42:58.555496',13,10),(317,'2025-12-15',0,'2026-02-19 09:42:58.555496','2026-02-19 09:42:58.555496',13,10),(318,'2025-12-17',0,'2026-02-19 09:42:58.571385','2026-02-19 09:42:58.571385',13,10),(319,'2025-12-18',0,'2026-02-19 09:42:58.571385','2026-02-19 09:42:58.571385',13,10),(320,'2026-01-20',0,'2026-02-19 09:42:58.575573','2026-02-19 09:42:58.575573',13,10),(321,'2026-01-26',0,'2026-02-19 09:42:58.577584','2026-02-19 09:42:58.577584',13,10),(322,'2026-02-06',0,'2026-02-19 09:42:58.577584','2026-02-19 09:42:58.577584',13,10),(323,'2026-02-07',0,'2026-02-19 09:42:58.577584','2026-02-19 09:42:58.577584',13,10),(324,'2026-02-12',0,'2026-02-19 09:42:58.577584','2026-02-19 09:42:58.577584',13,10),(325,'2026-02-18',0,'2026-02-19 09:42:58.577584','2026-02-19 09:42:58.577584',13,10),(326,'2025-11-21',0,'2026-02-19 09:42:58.584235','2026-02-19 09:42:58.584235',14,10),(327,'2025-11-22',0,'2026-02-19 09:42:58.587244','2026-02-19 09:42:58.587244',14,10),(328,'2025-11-24',0,'2026-02-19 09:42:58.587244','2026-02-19 09:42:58.587244',14,10),(329,'2025-11-25',0,'2026-02-19 09:42:58.587244','2026-02-19 09:42:58.587244',14,10),(330,'2025-11-26',0,'2026-02-19 09:42:58.587244','2026-02-19 09:42:58.587244',14,10),(331,'2025-11-28',0,'2026-02-19 09:42:58.587244','2026-02-19 09:42:58.587244',14,10),(332,'2025-11-29',0,'2026-02-19 09:42:58.587244','2026-02-19 09:42:58.587244',14,10),(333,'2025-12-01',0,'2026-02-19 09:42:58.587244','2026-02-19 09:42:58.587244',14,10),(334,'2025-12-02',0,'2026-02-19 09:42:58.587244','2026-02-19 09:42:58.587244',14,10),(335,'2025-12-05',0,'2026-02-19 09:42:58.587244','2026-02-19 09:42:58.587244',14,10),(336,'2025-12-06',0,'2026-02-19 09:42:58.587244','2026-02-19 09:42:58.587244',14,10),(337,'2025-12-08',0,'2026-02-19 09:42:58.587244','2026-02-19 09:42:58.587244',14,10),(338,'2025-12-10',0,'2026-02-19 09:42:58.603268','2026-02-19 09:42:58.603268',14,10),(339,'2025-12-11',0,'2026-02-19 09:42:58.605280','2026-02-19 09:42:58.605280',14,10),(340,'2025-12-12',0,'2026-02-19 09:42:58.605280','2026-02-19 09:42:58.605280',14,10),(341,'2025-12-13',0,'2026-02-19 09:42:58.607570','2026-02-19 09:42:58.607570',14,10),(342,'2025-12-15',0,'2026-02-19 09:42:58.607570','2026-02-19 09:42:58.607570',14,10),(343,'2025-12-17',0,'2026-02-19 09:42:58.611602','2026-02-19 09:42:58.611602',14,10),(344,'2025-12-18',0,'2026-02-19 09:42:58.614410','2026-02-19 09:42:58.614410',14,10),(345,'2026-01-20',0,'2026-02-19 09:42:58.614410','2026-02-19 09:42:58.614410',14,10),(346,'2026-01-26',0,'2026-02-19 09:42:58.616423','2026-02-19 09:42:58.616423',14,10),(347,'2026-02-06',0,'2026-02-19 09:42:58.616423','2026-02-19 09:42:58.616423',14,10),(348,'2026-02-07',0,'2026-02-19 09:42:58.619141','2026-02-19 09:42:58.619141',14,10),(349,'2026-02-12',0,'2026-02-19 09:42:58.619141','2026-02-19 09:42:58.619141',14,10),(350,'2026-02-18',0,'2026-02-19 09:42:58.622454','2026-02-19 09:42:58.622454',14,10),(351,'2025-11-21',0,'2026-02-19 09:42:58.625991','2026-02-19 09:42:58.625991',15,10),(352,'2025-11-22',0,'2026-02-19 09:42:58.625991','2026-02-19 09:42:58.625991',15,10),(353,'2025-11-24',0,'2026-02-19 09:42:58.630960','2026-02-19 09:42:58.630960',15,10),(354,'2025-11-25',0,'2026-02-19 09:42:58.632969','2026-02-19 09:42:58.632969',15,10),(355,'2025-11-26',0,'2026-02-19 09:42:58.632969','2026-02-19 09:42:58.632969',15,10),(356,'2025-11-28',0,'2026-02-19 09:42:58.634975','2026-02-19 09:42:58.634975',15,10),(357,'2025-11-29',0,'2026-02-19 09:42:58.634975','2026-02-19 09:42:58.634975',15,10),(358,'2025-12-01',0,'2026-02-19 09:42:58.634975','2026-02-19 09:42:58.634975',15,10),(359,'2025-12-02',0,'2026-02-19 09:42:58.640224','2026-02-19 09:42:58.640224',15,10),(360,'2025-12-05',0,'2026-02-19 09:42:58.642719','2026-02-19 09:42:58.642719',15,10),(361,'2025-12-06',0,'2026-02-19 09:42:58.642719','2026-02-19 09:42:58.642719',15,10),(362,'2025-12-08',0,'2026-02-19 09:42:58.644730','2026-02-19 09:42:58.644730',15,10),(363,'2025-12-10',0,'2026-02-19 09:42:58.644730','2026-02-19 09:42:58.644730',15,10),(364,'2025-12-11',0,'2026-02-19 09:42:58.644730','2026-02-19 09:42:58.644730',15,10),(365,'2025-12-12',0,'2026-02-19 09:42:58.651034','2026-02-19 09:42:58.651034',15,10),(366,'2025-12-13',0,'2026-02-19 09:42:58.651034','2026-02-19 09:42:58.651034',15,10),(367,'2025-12-15',0,'2026-02-19 09:42:58.651034','2026-02-19 09:42:58.651034',15,10),(368,'2025-12-17',0,'2026-02-19 09:42:58.651034','2026-02-19 09:42:58.651034',15,10),(369,'2025-12-18',0,'2026-02-19 09:42:58.651034','2026-02-19 09:42:58.651034',15,10),(370,'2026-01-20',0,'2026-02-19 09:42:58.651034','2026-02-19 09:42:58.651034',15,10),(371,'2026-01-26',0,'2026-02-19 09:42:58.651034','2026-02-19 09:42:58.651034',15,10),(372,'2026-02-06',0,'2026-02-19 09:42:58.651034','2026-02-19 09:42:58.651034',15,10),(373,'2026-02-07',0,'2026-02-19 09:42:58.651034','2026-02-19 09:42:58.651034',15,10),(374,'2026-02-12',0,'2026-02-19 09:42:58.651034','2026-02-19 09:42:58.651034',15,10),(375,'2026-02-18',0,'2026-02-19 09:42:58.666830','2026-02-19 09:42:58.666830',15,10),(376,'2025-11-21',0,'2026-02-19 09:42:58.668184','2026-02-19 09:42:58.668184',16,10),(377,'2025-11-22',0,'2026-02-19 09:42:58.668184','2026-02-19 09:42:58.668184',16,10),(378,'2025-11-24',0,'2026-02-19 09:42:58.677758','2026-02-19 09:42:58.677758',16,10),(379,'2025-11-25',0,'2026-02-19 09:42:58.678752','2026-02-19 09:42:58.678752',16,10),(380,'2025-11-26',0,'2026-02-19 09:42:58.679753','2026-02-19 09:42:58.679753',16,10),(381,'2025-11-28',0,'2026-02-19 09:42:58.681754','2026-02-19 09:42:58.681754',16,10),(382,'2025-11-29',0,'2026-02-19 09:42:58.683752','2026-02-19 09:42:58.683752',16,10),(383,'2025-12-01',0,'2026-02-19 09:42:58.685750','2026-02-19 09:42:58.685750',16,10),(384,'2025-12-02',0,'2026-02-19 09:42:58.686750','2026-02-19 09:42:58.686750',16,10),(385,'2025-12-05',0,'2026-02-19 09:42:58.687751','2026-02-19 09:42:58.687751',16,10),(386,'2025-12-06',0,'2026-02-19 09:42:58.689751','2026-02-19 09:42:58.689751',16,10),(387,'2025-12-08',0,'2026-02-19 09:42:58.691988','2026-02-19 09:42:58.691988',16,10),(388,'2025-12-10',0,'2026-02-19 09:42:58.694007','2026-02-19 09:42:58.694007',16,10),(389,'2025-12-11',0,'2026-02-19 09:42:58.695007','2026-02-19 09:42:58.695007',16,10),(390,'2025-12-12',0,'2026-02-19 09:42:58.696007','2026-02-19 09:42:58.696007',16,10),(391,'2025-12-13',0,'2026-02-19 09:42:58.697014','2026-02-19 09:42:58.697014',16,10),(392,'2025-12-15',0,'2026-02-19 09:42:58.699016','2026-02-19 09:42:58.699016',16,10),(393,'2025-12-17',0,'2026-02-19 09:42:58.700016','2026-02-19 09:42:58.700016',16,10),(394,'2025-12-18',0,'2026-02-19 09:42:58.701020','2026-02-19 09:42:58.701020',16,10),(395,'2026-01-20',0,'2026-02-19 09:42:58.702016','2026-02-19 09:42:58.702016',16,10),(396,'2026-01-26',0,'2026-02-19 09:42:58.704189','2026-02-19 09:42:58.704189',16,10),(397,'2026-02-06',0,'2026-02-19 09:42:58.705191','2026-02-19 09:42:58.705191',16,10),(398,'2026-02-07',0,'2026-02-19 09:42:58.707543','2026-02-19 09:42:58.707543',16,10),(399,'2026-02-12',0,'2026-02-19 09:42:58.710543','2026-02-19 09:42:58.710543',16,10),(400,'2026-02-18',0,'2026-02-19 09:42:58.711568','2026-02-19 09:42:58.711568',16,10),(401,'2025-11-21',0,'2026-02-19 09:42:58.715577','2026-02-19 09:42:58.715577',17,10),(402,'2025-11-22',0,'2026-02-19 09:42:58.717610','2026-02-19 09:42:58.717610',17,10),(403,'2025-11-24',0,'2026-02-19 09:42:58.718579','2026-02-19 09:42:58.718579',17,10),(404,'2025-11-25',0,'2026-02-19 09:42:58.720577','2026-02-19 09:42:58.720577',17,10),(405,'2025-11-26',0,'2026-02-19 09:42:58.722757','2026-02-19 09:42:58.722757',17,10),(406,'2025-11-28',0,'2026-02-19 09:42:58.724344','2026-02-19 09:42:58.724344',17,10),(407,'2025-11-29',0,'2026-02-19 09:42:58.726451','2026-02-19 09:42:58.726451',17,10),(408,'2025-12-01',0,'2026-02-19 09:42:58.727449','2026-02-19 09:42:58.727449',17,10),(409,'2025-12-02',0,'2026-02-19 09:42:58.729455','2026-02-19 09:42:58.729455',17,10),(410,'2025-12-05',0,'2026-02-19 09:42:58.730455','2026-02-19 09:42:58.730455',17,10),(411,'2025-12-06',0,'2026-02-19 09:42:58.731455','2026-02-19 09:42:58.731455',17,10),(412,'2025-12-08',0,'2026-02-19 09:42:58.733466','2026-02-19 09:42:58.733466',17,10),(413,'2025-12-10',0,'2026-02-19 09:42:58.734463','2026-02-19 09:42:58.734463',17,10),(414,'2025-12-11',0,'2026-02-19 09:42:58.736451','2026-02-19 09:42:58.736451',17,10),(415,'2025-12-12',0,'2026-02-19 09:42:58.737451','2026-02-19 09:42:58.737451',17,10),(416,'2025-12-13',0,'2026-02-19 09:42:58.739826','2026-02-19 09:42:58.739826',17,10),(417,'2025-12-15',0,'2026-02-19 09:42:58.741960','2026-02-19 09:42:58.741960',17,10),(418,'2025-12-17',0,'2026-02-19 09:42:58.743961','2026-02-19 09:42:58.743961',17,10),(419,'2025-12-18',0,'2026-02-19 09:42:58.744962','2026-02-19 09:42:58.744962',17,10),(420,'2026-01-20',0,'2026-02-19 09:42:58.745969','2026-02-19 09:42:58.746977',17,10),(421,'2026-01-26',0,'2026-02-19 09:42:58.747962','2026-02-19 09:42:58.747962',17,10),(422,'2026-02-06',0,'2026-02-19 09:42:58.748965','2026-02-19 09:42:58.748965',17,10),(423,'2026-02-07',0,'2026-02-19 09:42:58.750974','2026-02-19 09:42:58.750974',17,10),(424,'2026-02-12',0,'2026-02-19 09:42:58.751963','2026-02-19 09:42:58.751963',17,10),(425,'2026-02-18',0,'2026-02-19 09:42:58.752962','2026-02-19 09:42:58.752962',17,10),(426,'2025-11-21',0,'2026-02-19 09:42:58.757003','2026-02-19 09:42:58.757003',18,10),(427,'2025-11-22',0,'2026-02-19 09:42:58.758776','2026-02-19 09:42:58.758776',18,10),(428,'2025-11-24',0,'2026-02-19 09:42:58.760754','2026-02-19 09:42:58.760754',18,10),(429,'2025-11-25',0,'2026-02-19 09:42:58.762753','2026-02-19 09:42:58.762753',18,10),(430,'2025-11-26',0,'2026-02-19 09:42:58.763750','2026-02-19 09:42:58.763750',18,10),(431,'2025-11-28',0,'2026-02-19 09:42:58.764755','2026-02-19 09:42:58.764755',18,10),(432,'2025-11-29',0,'2026-02-19 09:42:58.765754','2026-02-19 09:42:58.765754',18,10),(433,'2025-12-01',0,'2026-02-19 09:42:58.767754','2026-02-19 09:42:58.767754',18,10),(434,'2025-12-02',0,'2026-02-19 09:42:58.768754','2026-02-19 09:42:58.768754',18,10),(435,'2025-12-05',0,'2026-02-19 09:42:58.770749','2026-02-19 09:42:58.770749',18,10),(436,'2025-12-06',0,'2026-02-19 09:42:58.771750','2026-02-19 09:42:58.771750',18,10),(437,'2025-12-08',0,'2026-02-19 09:42:58.774640','2026-02-19 09:42:58.774640',18,10),(438,'2025-12-10',0,'2026-02-19 09:42:58.775638','2026-02-19 09:42:58.775638',18,10),(439,'2025-12-11',0,'2026-02-19 09:42:58.776638','2026-02-19 09:42:58.776638',18,10),(440,'2025-12-12',0,'2026-02-19 09:42:58.777636','2026-02-19 09:42:58.777636',18,10),(441,'2025-12-13',0,'2026-02-19 09:42:58.779637','2026-02-19 09:42:58.779637',18,10),(442,'2025-12-15',0,'2026-02-19 09:42:58.780639','2026-02-19 09:42:58.780639',18,10),(443,'2025-12-17',0,'2026-02-19 09:42:58.782639','2026-02-19 09:42:58.782639',18,10),(444,'2025-12-18',0,'2026-02-19 09:42:58.783639','2026-02-19 09:42:58.783639',18,10),(445,'2026-01-20',0,'2026-02-19 09:42:58.784649','2026-02-19 09:42:58.784649',18,10),(446,'2026-01-26',0,'2026-02-19 09:42:58.785640','2026-02-19 09:42:58.785640',18,10),(447,'2026-02-06',0,'2026-02-19 09:42:58.787715','2026-02-19 09:42:58.787715',18,10),(448,'2026-02-07',0,'2026-02-19 09:42:58.789685','2026-02-19 09:42:58.789685',18,10),(449,'2026-02-12',0,'2026-02-19 09:42:58.791140','2026-02-19 09:42:58.791140',18,10),(450,'2026-02-18',0,'2026-02-19 09:42:58.792163','2026-02-19 09:42:58.792163',18,10),(451,'2025-11-21',0,'2026-02-19 09:42:58.795163','2026-02-19 09:42:58.795163',19,10),(452,'2025-11-22',0,'2026-02-19 09:42:58.796162','2026-02-19 09:42:58.796162',19,10),(453,'2025-11-24',0,'2026-02-19 09:42:58.798174','2026-02-19 09:42:58.798174',19,10),(454,'2025-11-25',0,'2026-02-19 09:42:58.799169','2026-02-19 09:42:58.799169',19,10),(455,'2025-11-26',0,'2026-02-19 09:42:58.801166','2026-02-19 09:42:58.801166',19,10),(456,'2025-11-28',0,'2026-02-19 09:42:58.802168','2026-02-19 09:42:58.802168',19,10),(457,'2025-11-29',0,'2026-02-19 09:42:58.803169','2026-02-19 09:42:58.803169',19,10),(458,'2025-12-01',0,'2026-02-19 09:42:58.804169','2026-02-19 09:42:58.804169',19,10),(459,'2025-12-02',0,'2026-02-19 09:42:58.805169','2026-02-19 09:42:58.805169',19,10),(460,'2025-12-05',0,'2026-02-19 09:42:58.807482','2026-02-19 09:42:58.807482',19,10),(461,'2025-12-06',0,'2026-02-19 09:42:58.808483','2026-02-19 09:42:58.808483',19,10),(462,'2025-12-08',0,'2026-02-19 09:42:58.810494','2026-02-19 09:42:58.810494',19,10),(463,'2025-12-10',0,'2026-02-19 09:42:58.812013','2026-02-19 09:42:58.812013',19,10),(464,'2025-12-11',0,'2026-02-19 09:42:58.813035','2026-02-19 09:42:58.813035',19,10),(465,'2025-12-12',0,'2026-02-19 09:42:58.814036','2026-02-19 09:42:58.814036',19,10),(466,'2025-12-13',0,'2026-02-19 09:42:58.816027','2026-02-19 09:42:58.816027',19,10),(467,'2025-12-15',0,'2026-02-19 09:42:58.817025','2026-02-19 09:42:58.817025',19,10),(468,'2025-12-17',0,'2026-02-19 09:42:58.819026','2026-02-19 09:42:58.819026',19,10),(469,'2025-12-18',0,'2026-02-19 09:42:58.821027','2026-02-19 09:42:58.821027',19,10),(470,'2026-01-20',0,'2026-02-19 09:42:58.823024','2026-02-19 09:42:58.823024',19,10),(471,'2026-01-26',0,'2026-02-19 09:42:58.825439','2026-02-19 09:42:58.825439',19,10),(472,'2026-02-06',0,'2026-02-19 09:42:58.825945','2026-02-19 09:42:58.825945',19,10),(473,'2026-02-07',0,'2026-02-19 09:42:58.827953','2026-02-19 09:42:58.827953',19,10),(474,'2026-02-12',0,'2026-02-19 09:42:58.828956','2026-02-19 09:42:58.828956',19,10),(475,'2026-02-18',0,'2026-02-19 09:42:58.830955','2026-02-19 09:42:58.830955',19,10),(476,'2025-11-21',0,'2026-02-19 09:42:58.832956','2026-02-19 09:42:58.832956',20,10),(477,'2025-11-22',0,'2026-02-19 09:42:58.833957','2026-02-19 09:42:58.834956',20,10),(478,'2025-11-24',0,'2026-02-19 09:42:58.835958','2026-02-19 09:42:58.835958',20,10),(479,'2025-11-25',0,'2026-02-19 09:42:58.836958','2026-02-19 09:42:58.836958',20,10),(480,'2025-11-26',0,'2026-02-19 09:42:58.837957','2026-02-19 09:42:58.837957',20,10),(481,'2025-11-28',0,'2026-02-19 09:42:58.839694','2026-02-19 09:42:58.839694',20,10),(482,'2025-11-29',0,'2026-02-19 09:42:58.841352','2026-02-19 09:42:58.841352',20,10),(483,'2025-12-01',0,'2026-02-19 09:42:58.843346','2026-02-19 09:42:58.843346',20,10),(484,'2025-12-02',0,'2026-02-19 09:42:58.844348','2026-02-19 09:42:58.844348',20,10),(485,'2025-12-05',0,'2026-02-19 09:42:58.845347','2026-02-19 09:42:58.845347',20,10),(486,'2025-12-06',0,'2026-02-19 09:42:58.846345','2026-02-19 09:42:58.846345',20,10),(487,'2025-12-08',0,'2026-02-19 09:42:58.848345','2026-02-19 09:42:58.848345',20,10),(488,'2025-12-10',0,'2026-02-19 09:42:58.849346','2026-02-19 09:42:58.849346',20,10),(489,'2025-12-11',0,'2026-02-19 09:42:58.851348','2026-02-19 09:42:58.851348',20,10),(490,'2025-12-12',0,'2026-02-19 09:42:58.852349','2026-02-19 09:42:58.852349',20,10),(491,'2025-12-13',0,'2026-02-19 09:42:58.853347','2026-02-19 09:42:58.853347',20,10),(492,'2025-12-15',0,'2026-02-19 09:42:58.854348','2026-02-19 09:42:58.854348',20,10),(493,'2025-12-17',0,'2026-02-19 09:42:58.856350','2026-02-19 09:42:58.856350',20,10),(494,'2025-12-18',0,'2026-02-19 09:42:58.858744','2026-02-19 09:42:58.858744',20,10),(495,'2026-01-20',0,'2026-02-19 09:42:58.859745','2026-02-19 09:42:58.859745',20,10),(496,'2026-01-26',0,'2026-02-19 09:42:58.860744','2026-02-19 09:42:58.860744',20,10),(497,'2026-02-06',0,'2026-02-19 09:42:58.862744','2026-02-19 09:42:58.862744',20,10),(498,'2026-02-07',0,'2026-02-19 09:42:58.863743','2026-02-19 09:42:58.863743',20,10),(499,'2026-02-12',0,'2026-02-19 09:42:58.864744','2026-02-19 09:42:58.864744',20,10),(500,'2026-02-18',0,'2026-02-19 09:42:58.865743','2026-02-19 09:42:58.865743',20,10),(501,'2025-11-21',0,'2026-02-19 09:42:58.895037','2026-02-19 09:42:58.895037',21,10),(502,'2025-11-22',0,'2026-02-19 09:42:58.896051','2026-02-19 09:42:58.896051',21,10),(503,'2025-11-24',0,'2026-02-19 09:42:58.897063','2026-02-19 09:42:58.897063',21,10),(504,'2025-11-25',0,'2026-02-19 09:42:58.898058','2026-02-19 09:42:58.898058',21,10),(505,'2025-11-26',0,'2026-02-19 09:42:58.900056','2026-02-19 09:42:58.900056',21,10),(506,'2025-11-28',0,'2026-02-19 09:42:58.901058','2026-02-19 09:42:58.901058',21,10),(507,'2025-11-29',0,'2026-02-19 09:42:58.902057','2026-02-19 09:42:58.902057',21,10),(508,'2025-12-01',0,'2026-02-19 09:42:58.904063','2026-02-19 09:42:58.904063',21,10),(509,'2025-12-02',0,'2026-02-19 09:42:58.905058','2026-02-19 09:42:58.905058',21,10),(510,'2025-12-05',0,'2026-02-19 09:42:58.908400','2026-02-19 09:42:58.908400',21,10),(511,'2025-12-06',0,'2026-02-19 09:42:58.909400','2026-02-19 09:42:58.909400',21,10),(512,'2025-12-08',0,'2026-02-19 09:42:58.911401','2026-02-19 09:42:58.911401',21,10),(513,'2025-12-10',0,'2026-02-19 09:42:58.912921','2026-02-19 09:42:58.912921',21,10),(514,'2025-12-11',0,'2026-02-19 09:42:58.913921','2026-02-19 09:42:58.913921',21,10),(515,'2025-12-12',0,'2026-02-19 09:42:58.914920','2026-02-19 09:42:58.914920',21,10),(516,'2025-12-13',0,'2026-02-19 09:42:58.915921','2026-02-19 09:42:58.915921',21,3),(517,'2025-12-15',0,'2026-02-19 09:42:58.916922','2026-02-19 09:42:58.916922',21,10),(518,'2025-12-17',0,'2026-02-19 09:42:58.917921','2026-02-19 09:42:58.917921',21,10),(519,'2025-12-18',0,'2026-02-19 09:42:58.918918','2026-02-19 09:42:58.918918',21,10),(520,'2026-01-20',0,'2026-02-19 09:42:58.920922','2026-02-19 09:42:58.920922',21,10),(521,'2026-01-26',0,'2026-02-19 09:42:58.922007','2026-02-19 09:42:58.922007',21,10),(522,'2026-02-06',0,'2026-02-19 09:42:58.924065','2026-02-19 09:42:58.924065',21,10),(523,'2026-02-07',0,'2026-02-19 09:42:58.926450','2026-02-19 09:42:58.926450',21,10),(524,'2026-02-12',0,'2026-02-19 09:42:58.927448','2026-02-19 09:42:58.927448',21,10),(525,'2026-02-18',0,'2026-02-19 09:42:58.930456','2026-02-19 09:42:58.930456',21,10),(526,'2025-11-21',0,'2026-02-19 09:42:58.937447','2026-02-19 09:42:58.937447',22,10),(527,'2025-11-22',0,'2026-02-19 09:42:58.939447','2026-02-19 09:42:58.939447',22,10),(528,'2025-11-24',0,'2026-02-19 09:42:58.941686','2026-02-19 09:42:58.941686',22,10),(529,'2025-11-25',0,'2026-02-19 09:42:58.942686','2026-02-19 09:42:58.942686',22,10),(530,'2025-11-26',0,'2026-02-19 09:42:58.943691','2026-02-19 09:42:58.943691',22,10),(531,'2025-11-28',0,'2026-02-19 09:42:58.944927','2026-02-19 09:42:58.944927',22,10),(532,'2025-11-29',0,'2026-02-19 09:42:58.945935','2026-02-19 09:42:58.945935',22,10),(533,'2025-12-01',0,'2026-02-19 09:42:58.947947','2026-02-19 09:42:58.947947',22,10),(534,'2025-12-02',0,'2026-02-19 09:42:58.948938','2026-02-19 09:42:58.948938',22,10),(535,'2025-12-05',0,'2026-02-19 09:42:58.949935','2026-02-19 09:42:58.949935',22,10),(536,'2025-12-06',0,'2026-02-19 09:42:58.950941','2026-02-19 09:42:58.950941',22,10),(537,'2025-12-08',0,'2026-02-19 09:42:58.953044','2026-02-19 09:42:58.953044',22,10),(538,'2025-12-10',0,'2026-02-19 09:42:58.954058','2026-02-19 09:42:58.954058',22,10),(539,'2025-12-11',0,'2026-02-19 09:42:58.956058','2026-02-19 09:42:58.956058',22,10),(540,'2025-12-12',0,'2026-02-19 09:42:58.957409','2026-02-19 09:42:58.957409',22,10),(541,'2025-12-13',0,'2026-02-19 09:42:58.959410','2026-02-19 09:42:58.959410',22,10),(542,'2025-12-15',0,'2026-02-19 09:42:58.960411','2026-02-19 09:42:58.960411',22,10),(543,'2025-12-17',0,'2026-02-19 09:42:58.962410','2026-02-19 09:42:58.962410',22,10),(544,'2025-12-18',0,'2026-02-19 09:42:58.964412','2026-02-19 09:42:58.964412',22,10),(545,'2026-01-20',0,'2026-02-19 09:42:58.965409','2026-02-19 09:42:58.965409',22,10),(546,'2026-01-26',0,'2026-02-19 09:42:58.966412','2026-02-19 09:42:58.966412',22,10),(547,'2026-02-06',0,'2026-02-19 09:42:58.967410','2026-02-19 09:42:58.967410',22,10),(548,'2026-02-07',0,'2026-02-19 09:42:58.968411','2026-02-19 09:42:58.968411',22,10),(549,'2026-02-12',0,'2026-02-19 09:42:58.970408','2026-02-19 09:42:58.970408',22,10),(550,'2026-02-18',0,'2026-02-19 09:42:58.971407','2026-02-19 09:42:58.971407',22,10),(551,'2025-11-21',0,'2026-02-19 09:42:58.983078','2026-02-19 09:42:58.983078',23,10),(552,'2025-11-22',0,'2026-02-19 09:42:58.984073','2026-02-19 09:42:58.984073',23,10),(553,'2025-11-24',0,'2026-02-19 09:42:58.985075','2026-02-19 09:42:58.985075',23,10),(554,'2025-11-25',0,'2026-02-19 09:42:58.987073','2026-02-19 09:42:58.987073',23,10),(555,'2025-11-26',0,'2026-02-19 09:42:58.988070','2026-02-19 09:42:58.988070',23,10),(556,'2025-11-28',0,'2026-02-19 09:42:58.989663','2026-02-19 09:42:58.989663',23,10),(557,'2025-11-29',0,'2026-02-19 09:42:58.991170','2026-02-19 09:42:58.991170',23,10),(558,'2025-12-01',0,'2026-02-19 09:42:58.992177','2026-02-19 09:42:58.992177',23,10),(559,'2025-12-02',0,'2026-02-19 09:42:58.994406','2026-02-19 09:42:58.994406',23,10),(560,'2025-12-05',0,'2026-02-19 09:42:58.995408','2026-02-19 09:42:58.995408',23,10),(561,'2025-12-06',0,'2026-02-19 09:42:58.997423','2026-02-19 09:42:58.997423',23,10),(562,'2025-12-08',0,'2026-02-19 09:42:58.998421','2026-02-19 09:42:58.998421',23,10),(563,'2025-12-10',0,'2026-02-19 09:42:59.000417','2026-02-19 09:42:59.000417',23,10),(564,'2025-12-11',0,'2026-02-19 09:42:59.001417','2026-02-19 09:42:59.001417',23,10),(565,'2025-12-12',0,'2026-02-19 09:42:59.002418','2026-02-19 09:42:59.002418',23,10),(566,'2025-12-13',0,'2026-02-19 09:42:59.003420','2026-02-19 09:42:59.003420',23,10),(567,'2025-12-15',0,'2026-02-19 09:42:59.004418','2026-02-19 09:42:59.004418',23,10),(568,'2025-12-17',0,'2026-02-19 09:42:59.006369','2026-02-19 09:42:59.006369',23,10),(569,'2025-12-18',0,'2026-02-19 09:42:59.008598','2026-02-19 09:42:59.008598',23,10),(570,'2026-01-20',0,'2026-02-19 09:42:59.009599','2026-02-19 09:42:59.009599',23,10),(571,'2026-01-26',0,'2026-02-19 09:42:59.010597','2026-02-19 09:42:59.010597',23,10),(572,'2026-02-06',0,'2026-02-19 09:42:59.012110','2026-02-19 09:42:59.012110',23,10),(573,'2026-02-07',0,'2026-02-19 09:42:59.014142','2026-02-19 09:42:59.014142',23,10),(574,'2026-02-12',0,'2026-02-19 09:42:59.016120','2026-02-19 09:42:59.016120',23,10),(575,'2026-02-18',0,'2026-02-19 09:42:59.017120','2026-02-19 09:42:59.017120',23,10),(576,'2025-11-21',0,'2026-02-19 09:42:59.022999','2026-02-19 09:42:59.022999',24,10),(577,'2025-11-22',0,'2026-02-19 09:42:59.024161','2026-02-19 09:42:59.024161',24,10),(578,'2025-11-24',0,'2026-02-19 09:42:59.025159','2026-02-19 09:42:59.025159',24,10),(579,'2025-11-25',0,'2026-02-19 09:42:59.026158','2026-02-19 09:42:59.026158',24,10),(580,'2025-11-26',0,'2026-02-19 09:42:59.027161','2026-02-19 09:42:59.027161',24,10),(581,'2025-11-28',0,'2026-02-19 09:42:59.028161','2026-02-19 09:42:59.028161',24,10),(582,'2025-11-29',0,'2026-02-19 09:42:59.029159','2026-02-19 09:42:59.029159',24,10),(583,'2025-12-01',0,'2026-02-19 09:42:59.031171','2026-02-19 09:42:59.031171',24,10),(584,'2025-12-02',0,'2026-02-19 09:42:59.032175','2026-02-19 09:42:59.032175',24,10),(585,'2025-12-05',0,'2026-02-19 09:42:59.033173','2026-02-19 09:42:59.033173',24,10),(586,'2025-12-06',0,'2026-02-19 09:42:59.035167','2026-02-19 09:42:59.035167',24,10),(587,'2025-12-08',0,'2026-02-19 09:42:59.036163','2026-02-19 09:42:59.036163',24,10),(588,'2025-12-10',0,'2026-02-19 09:42:59.037164','2026-02-19 09:42:59.037164',24,10),(589,'2025-12-11',0,'2026-02-19 09:42:59.039164','2026-02-19 09:42:59.039164',24,10),(590,'2025-12-12',0,'2026-02-19 09:42:59.040757','2026-02-19 09:42:59.040757',24,10),(591,'2025-12-13',0,'2026-02-19 09:42:59.043165','2026-02-19 09:42:59.043165',24,10),(592,'2025-12-15',0,'2026-02-19 09:42:59.044694','2026-02-19 09:42:59.044694',24,10),(593,'2025-12-17',0,'2026-02-19 09:42:59.045686','2026-02-19 09:42:59.045686',24,10),(594,'2025-12-18',0,'2026-02-19 09:42:59.047685','2026-02-19 09:42:59.047685',24,10),(595,'2026-01-20',0,'2026-02-19 09:42:59.048685','2026-02-19 09:42:59.048685',24,10),(596,'2026-01-26',0,'2026-02-19 09:42:59.049689','2026-02-19 09:42:59.049689',24,10),(597,'2026-02-06',0,'2026-02-19 09:42:59.051695','2026-02-19 09:42:59.051695',24,10),(598,'2026-02-07',0,'2026-02-19 09:42:59.053687','2026-02-19 09:42:59.053687',24,10),(599,'2026-02-12',0,'2026-02-19 09:42:59.055719','2026-02-19 09:42:59.055719',24,10),(600,'2026-02-18',0,'2026-02-19 09:42:59.057908','2026-02-19 09:42:59.057908',24,10),(601,'2025-11-21',0,'2026-02-19 09:42:59.062041','2026-02-19 09:42:59.062041',25,10),(602,'2025-11-22',0,'2026-02-19 09:42:59.064056','2026-02-19 09:42:59.064056',25,10),(603,'2025-11-24',0,'2026-02-19 09:42:59.065330','2026-02-19 09:42:59.065330',25,10),(604,'2025-11-25',0,'2026-02-19 09:42:59.065330','2026-02-19 09:42:59.065330',25,10),(605,'2025-11-26',0,'2026-02-19 09:42:59.065330','2026-02-19 09:42:59.065330',25,10),(606,'2025-11-28',0,'2026-02-19 09:42:59.065330','2026-02-19 09:42:59.065330',25,10),(607,'2025-11-29',0,'2026-02-19 09:42:59.071391','2026-02-19 09:42:59.071391',25,10),(608,'2025-12-01',0,'2026-02-19 09:42:59.071391','2026-02-19 09:42:59.071391',25,10),(609,'2025-12-02',0,'2026-02-19 09:42:59.076129','2026-02-19 09:42:59.076129',25,10),(610,'2025-12-05',0,'2026-02-19 09:42:59.077107','2026-02-19 09:42:59.077107',25,10),(611,'2025-12-06',0,'2026-02-19 09:42:59.079118','2026-02-19 09:42:59.079118',25,10),(612,'2025-12-08',0,'2026-02-19 09:42:59.080117','2026-02-19 09:42:59.080117',25,10),(613,'2025-12-10',0,'2026-02-19 09:42:59.081539','2026-02-19 09:42:59.081539',25,10),(614,'2025-12-11',0,'2026-02-19 09:42:59.083555','2026-02-19 09:42:59.083555',25,10),(615,'2025-12-12',0,'2026-02-19 09:42:59.084556','2026-02-19 09:42:59.084556',25,10),(616,'2025-12-13',0,'2026-02-19 09:42:59.086551','2026-02-19 09:42:59.086551',25,10),(617,'2025-12-15',0,'2026-02-19 09:42:59.088550','2026-02-19 09:42:59.088550',25,10),(618,'2025-12-17',0,'2026-02-19 09:42:59.090860','2026-02-19 09:42:59.090860',25,10),(619,'2025-12-18',0,'2026-02-19 09:42:59.093323','2026-02-19 09:42:59.093323',25,10),(620,'2026-01-20',0,'2026-02-19 09:42:59.094318','2026-02-19 09:42:59.094318',25,10),(621,'2026-01-26',0,'2026-02-19 09:42:59.095317','2026-02-19 09:42:59.095317',25,10),(622,'2026-02-06',0,'2026-02-19 09:42:59.097333','2026-02-19 09:42:59.097333',25,10),(623,'2026-02-07',0,'2026-02-19 09:42:59.099328','2026-02-19 09:42:59.099328',25,10),(624,'2026-02-12',0,'2026-02-19 09:42:59.100331','2026-02-19 09:42:59.100331',25,10),(625,'2026-02-18',0,'2026-02-19 09:42:59.101330','2026-02-19 09:42:59.101330',25,10),(626,'2025-11-21',0,'2026-02-19 09:42:59.104329','2026-02-19 09:42:59.104329',26,10),(627,'2025-11-22',0,'2026-02-19 09:42:59.107905','2026-02-19 09:42:59.107905',26,10),(628,'2025-11-24',0,'2026-02-19 09:42:59.108904','2026-02-19 09:42:59.108904',26,10),(629,'2025-11-25',0,'2026-02-19 09:42:59.110908','2026-02-19 09:42:59.110908',26,10),(630,'2025-11-26',0,'2026-02-19 09:42:59.111907','2026-02-19 09:42:59.111907',26,10),(631,'2025-11-28',0,'2026-02-19 09:42:59.113447','2026-02-19 09:42:59.113447',26,10),(632,'2025-11-29',0,'2026-02-19 09:42:59.114455','2026-02-19 09:42:59.114455',26,10),(633,'2025-12-01',0,'2026-02-19 09:42:59.116459','2026-02-19 09:42:59.116459',26,10),(634,'2025-12-02',0,'2026-02-19 09:42:59.117457','2026-02-19 09:42:59.117457',26,10),(635,'2025-12-05',0,'2026-02-19 09:42:59.118454','2026-02-19 09:42:59.118454',26,10),(636,'2025-12-06',0,'2026-02-19 09:42:59.119458','2026-02-19 09:42:59.119458',26,10),(637,'2025-12-08',0,'2026-02-19 09:42:59.121455','2026-02-19 09:42:59.121455',26,10),(638,'2025-12-10',0,'2026-02-19 09:42:59.124090','2026-02-19 09:42:59.124090',26,10),(639,'2025-12-11',0,'2026-02-19 09:42:59.126089','2026-02-19 09:42:59.126089',26,10),(640,'2025-12-12',0,'2026-02-19 09:42:59.127090','2026-02-19 09:42:59.127090',26,10),(641,'2025-12-13',0,'2026-02-19 09:42:59.129087','2026-02-19 09:42:59.129087',26,10),(642,'2025-12-15',0,'2026-02-19 09:42:59.130089','2026-02-19 09:42:59.130089',26,10),(643,'2025-12-17',0,'2026-02-19 09:42:59.131089','2026-02-19 09:42:59.131089',26,10),(644,'2025-12-18',0,'2026-02-19 09:42:59.132087','2026-02-19 09:42:59.132087',26,10),(645,'2026-01-20',0,'2026-02-19 09:42:59.134091','2026-02-19 09:42:59.134091',26,10),(646,'2026-01-26',0,'2026-02-19 09:42:59.136091','2026-02-19 09:42:59.136091',26,10),(647,'2026-02-06',0,'2026-02-19 09:42:59.137089','2026-02-19 09:42:59.137089',26,10),(648,'2026-02-07',0,'2026-02-19 09:42:59.138092','2026-02-19 09:42:59.138092',26,10),(649,'2026-02-12',0,'2026-02-19 09:42:59.140090','2026-02-19 09:42:59.140090',26,10),(650,'2026-02-18',0,'2026-02-19 09:42:59.141942','2026-02-19 09:42:59.141942',26,10),(651,'2025-11-21',0,'2026-02-19 09:42:59.144943','2026-02-19 09:42:59.144943',27,10),(652,'2025-11-22',0,'2026-02-19 09:42:59.145942','2026-02-19 09:42:59.145942',27,10),(653,'2025-11-24',0,'2026-02-19 09:42:59.146940','2026-02-19 09:42:59.146940',27,10),(654,'2025-11-25',0,'2026-02-19 09:42:59.148942','2026-02-19 09:42:59.148942',27,10),(655,'2025-11-26',0,'2026-02-19 09:42:59.150285','2026-02-19 09:42:59.150285',27,10),(656,'2025-11-28',0,'2026-02-19 09:42:59.151299','2026-02-19 09:42:59.151299',27,10),(657,'2025-11-29',0,'2026-02-19 09:42:59.152298','2026-02-19 09:42:59.152298',27,10),(658,'2025-12-01',0,'2026-02-19 09:42:59.154293','2026-02-19 09:42:59.154293',27,10),(659,'2025-12-02',0,'2026-02-19 09:42:59.156293','2026-02-19 09:42:59.156293',27,10),(660,'2025-12-05',0,'2026-02-19 09:42:59.157293','2026-02-19 09:42:59.157293',27,10),(661,'2025-12-06',0,'2026-02-19 09:42:59.159499','2026-02-19 09:42:59.159499',27,10),(662,'2025-12-08',0,'2026-02-19 09:42:59.160498','2026-02-19 09:42:59.161501',27,10),(663,'2025-12-10',0,'2026-02-19 09:42:59.162498','2026-02-19 09:42:59.162498',27,10),(664,'2025-12-11',0,'2026-02-19 09:42:59.163498','2026-02-19 09:42:59.163498',27,10),(665,'2025-12-12',0,'2026-02-19 09:42:59.166587','2026-02-19 09:42:59.166587',27,10),(666,'2025-12-13',0,'2026-02-19 09:42:59.167498','2026-02-19 09:42:59.167498',27,10),(667,'2025-12-15',0,'2026-02-19 09:42:59.168500','2026-02-19 09:42:59.168500',27,10),(668,'2025-12-17',0,'2026-02-19 09:42:59.170499','2026-02-19 09:42:59.170499',27,10),(669,'2025-12-18',0,'2026-02-19 09:42:59.171500','2026-02-19 09:42:59.171500',27,10),(670,'2026-01-20',0,'2026-02-19 09:42:59.172674','2026-02-19 09:42:59.172674',27,10),(671,'2026-01-26',0,'2026-02-19 09:42:59.174865','2026-02-19 09:42:59.174865',27,10),(672,'2026-02-06',0,'2026-02-19 09:42:59.176864','2026-02-19 09:42:59.176864',27,10),(673,'2026-02-07',0,'2026-02-19 09:42:59.177864','2026-02-19 09:42:59.178863',27,10),(674,'2026-02-12',0,'2026-02-19 09:42:59.179862','2026-02-19 09:42:59.179862',27,10),(675,'2026-02-18',0,'2026-02-19 09:42:59.182858','2026-02-19 09:42:59.182858',27,10),(676,'2025-11-21',0,'2026-02-19 09:42:59.187859','2026-02-19 09:42:59.187859',28,10),(677,'2025-11-22',0,'2026-02-19 09:42:59.190740','2026-02-19 09:42:59.190740',28,10),(678,'2025-11-24',0,'2026-02-19 09:42:59.191749','2026-02-19 09:42:59.191749',28,10),(679,'2025-11-25',0,'2026-02-19 09:42:59.192747','2026-02-19 09:42:59.192747',28,10),(680,'2025-11-26',0,'2026-02-19 09:42:59.193771','2026-02-19 09:42:59.193771',28,10),(681,'2025-11-28',0,'2026-02-19 09:42:59.194755','2026-02-19 09:42:59.194755',28,10),(682,'2025-11-29',0,'2026-02-19 09:42:59.195746','2026-02-19 09:42:59.195746',28,10),(683,'2025-12-01',0,'2026-02-19 09:42:59.196751','2026-02-19 09:42:59.196751',28,10),(684,'2025-12-02',0,'2026-02-19 09:42:59.197759','2026-02-19 09:42:59.197759',28,10),(685,'2025-12-05',0,'2026-02-19 09:42:59.198759','2026-02-19 09:42:59.198759',28,10),(686,'2025-12-06',0,'2026-02-19 09:42:59.199758','2026-02-19 09:42:59.199758',28,10),(687,'2025-12-08',0,'2026-02-19 09:42:59.200758','2026-02-19 09:42:59.200758',28,10),(688,'2025-12-10',0,'2026-02-19 09:42:59.201758','2026-02-19 09:42:59.201758',28,10),(689,'2025-12-11',0,'2026-02-19 09:42:59.202761','2026-02-19 09:42:59.202761',28,10),(690,'2025-12-12',0,'2026-02-19 09:42:59.203760','2026-02-19 09:42:59.203760',28,10),(691,'2025-12-13',0,'2026-02-19 09:42:59.205759','2026-02-19 09:42:59.205759',28,10),(692,'2025-12-15',0,'2026-02-19 09:42:59.208440','2026-02-19 09:42:59.208440',28,10),(693,'2025-12-17',0,'2026-02-19 09:42:59.209438','2026-02-19 09:42:59.209438',28,10),(694,'2025-12-18',0,'2026-02-19 09:42:59.211944','2026-02-19 09:42:59.211944',28,10),(695,'2026-01-20',0,'2026-02-19 09:42:59.212952','2026-02-19 09:42:59.212952',28,10),(696,'2026-01-26',0,'2026-02-19 09:42:59.213949','2026-02-19 09:42:59.213949',28,10),(697,'2026-02-06',0,'2026-02-19 09:42:59.215949','2026-02-19 09:42:59.215949',28,10),(698,'2026-02-07',0,'2026-02-19 09:42:59.216949','2026-02-19 09:42:59.216949',28,10),(699,'2026-02-12',0,'2026-02-19 09:42:59.217952','2026-02-19 09:42:59.217952',28,10),(700,'2026-02-18',0,'2026-02-19 09:42:59.219960','2026-02-19 09:42:59.219960',28,10),(701,'2026-02-19',0,'2026-02-19 18:22:24.222085','2026-02-19 18:22:24.222085',21,10),(702,'2026-02-19',0,'2026-02-19 18:22:24.229599','2026-02-19 18:22:24.229599',13,10),(703,'2026-02-19',0,'2026-02-19 18:22:24.237794','2026-02-19 18:22:24.237794',24,10),(704,'2026-02-19',0,'2026-02-19 18:22:24.245885','2026-02-19 18:22:24.245885',22,10),(705,'2026-02-19',0,'2026-02-19 18:22:24.254114','2026-02-19 18:22:24.254114',28,10),(706,'2026-02-19',0,'2026-02-19 18:22:24.264918','2026-02-19 18:22:24.264918',7,10),(707,'2026-02-19',0,'2026-02-19 18:22:24.270555','2026-02-19 18:22:24.270555',19,10),(708,'2026-02-19',0,'2026-02-19 18:22:24.278678','2026-02-19 18:22:24.278678',26,10),(709,'2026-02-19',0,'2026-02-19 18:22:24.278678','2026-02-19 18:22:24.287144',20,10),(710,'2026-02-19',0,'2026-02-19 18:22:24.292148','2026-02-19 18:22:24.295417',4,10),(711,'2026-02-19',0,'2026-02-19 18:22:24.295417','2026-02-19 18:22:24.295417',6,10),(712,'2026-02-19',0,'2026-02-19 18:22:24.309701','2026-02-19 18:22:24.309701',15,10),(713,'2026-02-19',0,'2026-02-19 18:22:24.313346','2026-02-19 18:22:24.313346',3,10),(714,'2026-02-19',0,'2026-02-19 18:22:24.324535','2026-02-19 18:22:24.324535',18,10),(715,'2026-02-19',0,'2026-02-19 18:22:24.330036','2026-02-19 18:22:24.330036',12,10),(716,'2026-02-19',0,'2026-02-19 18:22:24.338436','2026-02-19 18:22:24.338436',25,10),(717,'2026-02-19',0,'2026-02-19 18:22:24.341923','2026-02-19 18:22:24.341923',11,10),(718,'2026-02-19',0,'2026-02-19 18:22:24.353268','2026-02-19 18:22:24.353268',1,10),(719,'2026-02-19',0,'2026-02-19 18:22:24.359088','2026-02-19 18:22:24.359088',5,10),(720,'2026-02-19',0,'2026-02-19 18:22:24.365169','2026-02-19 18:22:24.365169',16,10),(721,'2026-02-19',0,'2026-02-19 18:22:24.370205','2026-02-19 18:22:24.370205',27,10),(722,'2026-02-19',0,'2026-02-19 18:22:24.376397','2026-02-19 18:22:24.376397',2,10),(723,'2026-02-19',0,'2026-02-19 18:22:24.384806','2026-02-19 18:22:24.384806',23,10),(724,'2026-02-19',0,'2026-02-19 18:22:24.392100','2026-02-19 18:22:24.392100',9,10),(725,'2026-02-19',0,'2026-02-19 18:22:24.400507','2026-02-19 18:22:24.400507',17,10),(726,'2026-02-19',0,'2026-02-19 18:22:24.408258','2026-02-19 18:22:24.408258',10,10),(727,'2026-02-19',0,'2026-02-19 18:22:24.411295','2026-02-19 18:22:24.411295',14,10),(728,'2026-02-19',0,'2026-02-19 18:22:24.418452','2026-02-19 18:22:24.418452',8,10),(729,'2026-03-04',0,'2026-03-04 15:24:00.105629','2026-03-04 15:24:00.105629',21,10),(730,'2026-03-04',0,'2026-03-04 15:24:00.114140','2026-03-04 15:24:00.114140',13,10),(731,'2026-03-04',0,'2026-03-04 15:24:00.118878','2026-03-04 15:24:00.118878',24,10),(732,'2026-03-04',0,'2026-03-04 15:24:00.122139','2026-03-04 15:24:00.122139',22,10),(733,'2026-03-04',0,'2026-03-04 15:24:00.126605','2026-03-04 15:24:00.126605',28,10),(734,'2026-03-04',0,'2026-03-04 15:24:00.129601','2026-03-04 15:24:00.129601',7,10),(735,'2026-03-04',0,'2026-03-04 15:24:00.132600','2026-03-04 15:24:00.132600',19,10),(736,'2026-03-04',0,'2026-03-04 15:24:00.136613','2026-03-04 15:24:00.136613',26,10),(737,'2026-03-04',0,'2026-03-04 15:24:00.140864','2026-03-04 15:24:00.140864',20,10),(738,'2026-03-04',0,'2026-03-04 15:24:00.143862','2026-03-04 15:24:00.143862',4,10),(739,'2026-03-04',0,'2026-03-04 15:24:00.146865','2026-03-04 15:24:00.146865',6,10),(740,'2026-03-04',0,'2026-03-04 15:24:00.149861','2026-03-04 15:24:00.149861',15,10),(741,'2026-03-04',0,'2026-03-04 15:24:00.154211','2026-03-04 15:24:00.154211',3,10),(742,'2026-03-04',0,'2026-03-04 15:24:00.159512','2026-03-04 15:24:00.159512',18,10),(743,'2026-03-04',0,'2026-03-04 15:24:00.162733','2026-03-04 15:24:00.162733',12,10),(744,'2026-03-04',0,'2026-03-04 15:24:00.165731','2026-03-04 15:24:00.165731',25,10),(745,'2026-03-04',0,'2026-03-04 15:24:00.170431','2026-03-04 15:24:00.170431',11,10),(746,'2026-03-04',0,'2026-03-04 15:24:00.174797','2026-03-04 15:24:00.174797',1,10),(747,'2026-03-04',0,'2026-03-04 15:24:00.178780','2026-03-04 15:24:00.178780',5,10),(748,'2026-03-04',0,'2026-03-04 15:24:00.182778','2026-03-04 15:24:00.182778',16,10),(749,'2026-03-04',0,'2026-03-04 15:24:00.188695','2026-03-04 15:24:00.188695',27,10),(750,'2026-03-04',0,'2026-03-04 15:24:00.192200','2026-03-04 15:24:00.192200',2,10),(751,'2026-03-04',0,'2026-03-04 15:24:00.196213','2026-03-04 15:24:00.196213',23,10),(752,'2026-03-04',0,'2026-03-04 15:24:00.199207','2026-03-04 15:24:00.199207',9,10),(753,'2026-03-04',0,'2026-03-04 15:24:00.203840','2026-03-04 15:24:00.203840',17,10),(754,'2026-03-04',0,'2026-03-04 15:24:00.207885','2026-03-04 15:24:00.207885',10,10),(755,'2026-03-04',0,'2026-03-04 15:24:00.210893','2026-03-04 15:24:00.210893',14,10),(756,'2026-03-04',0,'2026-03-04 15:24:00.215058','2026-03-04 15:24:00.215058',8,10),(757,'2026-03-05',0,'2026-03-05 10:36:03.710233','2026-03-05 10:36:03.710233',21,10),(758,'2026-03-05',0,'2026-03-05 10:36:03.716623','2026-03-05 10:36:03.716623',13,10),(759,'2026-03-05',0,'2026-03-05 10:36:03.720624','2026-03-05 10:36:03.720624',24,10),(760,'2026-03-05',0,'2026-03-05 10:36:03.723623','2026-03-05 10:36:03.723623',22,10),(761,'2026-03-05',0,'2026-03-05 10:36:03.727982','2026-03-05 10:36:03.727982',28,10),(762,'2026-03-05',0,'2026-03-05 10:36:03.730978','2026-03-05 10:36:03.730978',7,10),(763,'2026-03-05',0,'2026-03-05 10:36:03.733975','2026-03-05 10:36:03.733975',19,10),(764,'2026-03-05',0,'2026-03-05 10:36:03.736975','2026-03-05 10:36:03.736975',26,10),(765,'2026-03-05',0,'2026-03-05 10:36:03.741552','2026-03-05 10:36:03.741552',20,10),(766,'2026-03-05',0,'2026-03-05 10:36:03.744739','2026-03-05 10:36:03.744739',4,10),(767,'2026-03-05',0,'2026-03-05 10:36:03.747737','2026-03-05 10:36:03.747737',6,10),(768,'2026-03-05',0,'2026-03-05 10:36:03.750741','2026-03-05 10:36:03.750741',15,10),(769,'2026-03-05',0,'2026-03-05 10:36:03.754739','2026-03-05 10:36:03.754739',3,10),(770,'2026-03-05',0,'2026-03-05 10:36:03.758428','2026-03-05 10:36:03.758428',18,10),(771,'2026-03-05',0,'2026-03-05 10:36:03.761499','2026-03-05 10:36:03.761499',12,10),(772,'2026-03-05',0,'2026-03-05 10:36:03.764479','2026-03-05 10:36:03.764479',25,10),(773,'2026-03-05',0,'2026-03-05 10:36:03.767478','2026-03-05 10:36:03.767478',11,10),(774,'2026-03-05',0,'2026-03-05 10:36:03.770479','2026-03-05 10:36:03.770479',1,10),(775,'2026-03-05',0,'2026-03-05 10:36:03.773436','2026-03-05 10:36:03.773436',5,10),(776,'2026-03-05',0,'2026-03-05 10:36:03.776176','2026-03-05 10:36:03.776176',16,10),(777,'2026-03-05',0,'2026-03-05 10:36:03.779153','2026-03-05 10:36:03.779153',27,10),(778,'2026-03-05',0,'2026-03-05 10:36:03.782154','2026-03-05 10:36:03.782154',2,10),(779,'2026-03-05',0,'2026-03-05 10:36:03.785174','2026-03-05 10:36:03.785174',23,10),(780,'2026-03-05',0,'2026-03-05 10:36:03.788169','2026-03-05 10:36:03.788169',9,10),(781,'2026-03-05',0,'2026-03-05 10:36:03.791155','2026-03-05 10:36:03.791155',17,10),(782,'2026-03-05',0,'2026-03-05 10:36:03.791155','2026-03-05 10:36:03.791155',10,10),(783,'2026-03-05',0,'2026-03-05 10:36:03.791155','2026-03-05 10:36:03.791155',14,10),(784,'2026-03-05',0,'2026-03-05 10:36:03.791155','2026-03-05 10:36:03.791155',8,10),(785,'2026-03-06',0,'2026-03-06 15:37:22.394635','2026-03-06 15:37:22.394635',21,10),(786,'2026-03-06',0,'2026-03-06 15:37:22.427739','2026-03-06 15:37:22.427739',13,10),(787,'2026-03-06',0,'2026-03-06 15:37:22.427739','2026-03-06 15:37:22.427739',24,10),(788,'2026-03-06',0,'2026-03-06 15:37:22.427739','2026-03-06 15:37:22.427739',22,10),(789,'2026-03-06',0,'2026-03-06 15:37:22.427739','2026-03-06 15:37:22.427739',28,10),(790,'2026-03-06',0,'2026-03-06 15:37:22.444400','2026-03-06 15:37:22.444400',7,10),(791,'2026-03-06',0,'2026-03-06 15:37:22.444400','2026-03-06 15:37:22.444400',19,10),(792,'2026-03-06',0,'2026-03-06 15:37:22.444400','2026-03-06 15:37:22.444400',26,10),(793,'2026-03-06',0,'2026-03-06 15:37:22.444400','2026-03-06 15:37:22.444400',20,10),(794,'2026-03-06',0,'2026-03-06 15:37:22.460267','2026-03-06 15:37:22.460267',4,10),(795,'2026-03-06',0,'2026-03-06 15:37:22.461155','2026-03-06 15:37:22.461155',6,10),(796,'2026-03-06',0,'2026-03-06 15:37:22.461155','2026-03-06 15:37:22.461155',15,10),(797,'2026-03-06',0,'2026-03-06 15:37:22.461155','2026-03-06 15:37:22.461155',3,10),(798,'2026-03-06',0,'2026-03-06 15:37:22.476224','2026-03-06 15:37:22.476224',18,10),(799,'2026-03-06',0,'2026-03-06 15:37:22.477787','2026-03-06 15:37:22.477787',12,10),(800,'2026-03-06',0,'2026-03-06 15:37:22.477787','2026-03-06 15:37:22.477787',25,10),(801,'2026-03-06',0,'2026-03-06 15:37:22.477787','2026-03-06 15:37:22.477787',11,10),(802,'2026-03-06',0,'2026-03-06 15:37:22.477787','2026-03-06 15:37:22.477787',1,10),(803,'2026-03-06',0,'2026-03-06 15:37:22.477787','2026-03-06 15:37:22.477787',5,10),(804,'2026-03-06',0,'2026-03-06 15:37:22.494411','2026-03-06 15:37:22.494411',16,10),(805,'2026-03-06',0,'2026-03-06 15:37:22.494411','2026-03-06 15:37:22.494411',27,10),(806,'2026-03-06',0,'2026-03-06 15:37:22.494411','2026-03-06 15:37:22.494411',2,10),(807,'2026-03-06',0,'2026-03-06 15:37:22.504374','2026-03-06 15:37:22.504374',23,10),(808,'2026-03-06',0,'2026-03-06 15:37:22.504374','2026-03-06 15:37:22.504374',9,10),(809,'2026-03-06',0,'2026-03-06 15:37:22.510947','2026-03-06 15:37:22.510947',17,10),(810,'2026-03-06',0,'2026-03-06 15:37:22.510947','2026-03-06 15:37:22.510947',10,10),(811,'2026-03-06',0,'2026-03-06 15:37:22.510947','2026-03-06 15:37:22.510947',14,10),(812,'2026-03-06',0,'2026-03-06 15:37:22.510947','2026-03-06 15:37:22.510947',8,10),(813,'2026-03-07',0,'2026-03-07 21:23:38.106770','2026-03-07 21:23:38.106770',21,10),(814,'2026-03-07',0,'2026-03-07 21:23:38.113856','2026-03-07 21:23:38.113856',13,10),(815,'2026-03-07',0,'2026-03-07 21:23:38.118102','2026-03-07 21:23:38.118102',24,10),(816,'2026-03-07',0,'2026-03-07 21:23:38.118102','2026-03-07 21:23:38.118102',22,10),(817,'2026-03-07',0,'2026-03-07 21:23:38.118102','2026-03-07 21:23:38.118102',28,10),(818,'2026-03-07',0,'2026-03-07 21:23:38.130807','2026-03-07 21:23:38.130807',7,10),(819,'2026-03-07',0,'2026-03-07 21:23:38.130807','2026-03-07 21:23:38.130807',19,10),(820,'2026-03-07',0,'2026-03-07 21:23:38.144656','2026-03-07 21:23:38.144656',26,10),(821,'2026-03-07',0,'2026-03-07 21:23:38.147134','2026-03-07 21:23:38.147134',20,10),(822,'2026-03-07',0,'2026-03-07 21:23:38.154736','2026-03-07 21:23:38.154736',4,10),(823,'2026-03-07',0,'2026-03-07 21:23:38.162267','2026-03-07 21:23:38.162267',6,10),(824,'2026-03-07',0,'2026-03-07 21:23:38.165373','2026-03-07 21:23:38.165373',15,10),(825,'2026-03-07',0,'2026-03-07 21:23:38.167383','2026-03-07 21:23:38.167383',3,10),(826,'2026-03-07',0,'2026-03-07 21:23:38.167383','2026-03-07 21:23:38.167383',18,10),(827,'2026-03-07',0,'2026-03-07 21:23:38.178883','2026-03-07 21:23:38.178883',12,10),(828,'2026-03-07',0,'2026-03-07 21:23:38.180890','2026-03-07 21:23:38.180890',25,10),(829,'2026-03-07',0,'2026-03-07 21:23:38.180890','2026-03-07 21:23:38.180890',11,10),(830,'2026-03-07',0,'2026-03-07 21:23:38.180890','2026-03-07 21:23:38.180890',1,10),(831,'2026-03-07',0,'2026-03-07 21:23:38.196559','2026-03-07 21:23:38.196559',5,10),(832,'2026-03-07',0,'2026-03-07 21:23:38.196559','2026-03-07 21:23:38.196559',16,10),(833,'2026-03-07',0,'2026-03-07 21:23:38.196559','2026-03-07 21:23:38.196559',27,10),(834,'2026-03-07',0,'2026-03-07 21:23:38.212171','2026-03-07 21:23:38.212171',2,10),(835,'2026-03-07',0,'2026-03-07 21:23:38.213522','2026-03-07 21:23:38.213522',23,10),(836,'2026-03-07',0,'2026-03-07 21:23:38.222175','2026-03-07 21:23:38.222175',9,10),(837,'2026-03-07',0,'2026-03-07 21:23:38.226208','2026-03-07 21:23:38.226208',17,10),(838,'2026-03-07',0,'2026-03-07 21:23:38.229905','2026-03-07 21:23:38.229905',10,10),(839,'2026-03-07',0,'2026-03-07 21:23:38.231582','2026-03-07 21:23:38.231582',14,10),(840,'2026-03-07',0,'2026-03-07 21:23:38.231582','2026-03-07 21:23:38.231582',8,10),(841,'2026-03-08',0,'2026-03-08 14:44:51.480643','2026-03-08 14:44:51.480643',21,10),(842,'2026-03-08',0,'2026-03-08 14:44:51.495212','2026-03-08 14:44:51.495212',13,10),(843,'2026-03-08',0,'2026-03-08 14:44:51.500858','2026-03-08 14:44:51.500858',24,10),(844,'2026-03-08',0,'2026-03-08 14:44:51.508896','2026-03-08 14:44:51.508896',22,10),(845,'2026-03-08',0,'2026-03-08 14:44:51.520903','2026-03-08 14:44:51.520903',28,10),(846,'2026-03-08',0,'2026-03-08 14:44:51.528509','2026-03-08 14:44:51.528509',7,10),(847,'2026-03-08',0,'2026-03-08 14:44:51.536781','2026-03-08 14:44:51.536781',19,10),(848,'2026-03-08',0,'2026-03-08 14:44:51.544992','2026-03-08 14:44:51.544992',26,10),(849,'2026-03-08',0,'2026-03-08 14:44:51.544992','2026-03-08 14:44:51.544992',20,10),(850,'2026-03-08',0,'2026-03-08 14:44:51.553404','2026-03-08 14:44:51.553404',4,10),(851,'2026-03-08',0,'2026-03-08 14:44:51.565794','2026-03-08 14:44:51.565794',6,10),(852,'2026-03-08',0,'2026-03-08 14:44:51.580581','2026-03-08 14:44:51.580581',15,10),(853,'2026-03-08',0,'2026-03-08 14:44:51.588508','2026-03-08 14:44:51.588508',3,10),(854,'2026-03-08',0,'2026-03-08 14:44:51.598632','2026-03-08 14:44:51.598632',18,10),(855,'2026-03-08',0,'2026-03-08 14:44:51.604695','2026-03-08 14:44:51.604695',12,10),(856,'2026-03-08',0,'2026-03-08 14:44:51.618045','2026-03-08 14:44:51.618045',25,10),(857,'2026-03-08',0,'2026-03-08 14:44:51.619062','2026-03-08 14:44:51.619062',11,10),(858,'2026-03-08',0,'2026-03-08 14:44:51.627531','2026-03-08 14:44:51.627531',1,10),(859,'2026-03-08',0,'2026-03-08 14:44:51.635738','2026-03-08 14:44:51.635738',5,10),(860,'2026-03-08',0,'2026-03-08 14:44:51.648062','2026-03-08 14:44:51.648062',16,10),(861,'2026-03-08',0,'2026-03-08 14:44:51.655065','2026-03-08 14:44:51.655065',27,10),(862,'2026-03-08',0,'2026-03-08 14:44:51.661710','2026-03-08 14:44:51.661710',2,10),(863,'2026-03-08',0,'2026-03-08 14:44:51.668928','2026-03-08 14:44:51.668928',23,10),(864,'2026-03-08',0,'2026-03-08 14:44:51.680721','2026-03-08 14:44:51.680721',9,10),(865,'2026-03-08',0,'2026-03-08 14:44:51.687241','2026-03-08 14:44:51.687241',17,10),(866,'2026-03-08',0,'2026-03-08 14:44:51.695010','2026-03-08 14:44:51.695010',10,10),(867,'2026-03-08',0,'2026-03-08 14:44:51.701929','2026-03-08 14:44:51.701929',14,10),(868,'2026-03-08',0,'2026-03-08 14:44:51.710095','2026-03-08 14:44:51.710095',8,10),(869,'2026-03-10',0,'2026-03-10 16:19:43.439086','2026-03-10 16:19:43.439086',21,10),(870,'2026-03-10',0,'2026-03-10 16:19:43.455459','2026-03-10 16:19:43.455459',13,10),(871,'2026-03-10',0,'2026-03-10 16:19:43.465208','2026-03-10 16:19:43.465208',24,10),(872,'2026-03-10',0,'2026-03-10 16:19:43.472730','2026-03-10 16:19:43.472730',22,10),(873,'2026-03-10',0,'2026-03-10 16:19:43.483087','2026-03-10 16:19:43.483087',28,10),(874,'2026-03-10',0,'2026-03-10 16:19:43.491123','2026-03-10 16:19:43.491123',7,10),(875,'2026-03-10',0,'2026-03-10 16:19:43.498880','2026-03-10 16:19:43.498880',19,10),(876,'2026-03-10',0,'2026-03-10 16:19:43.506047','2026-03-10 16:19:43.506047',26,10),(877,'2026-03-10',0,'2026-03-10 16:19:43.514667','2026-03-10 16:19:43.514667',20,10),(878,'2026-03-10',0,'2026-03-10 16:19:43.526613','2026-03-10 16:19:43.526613',4,10),(879,'2026-03-10',0,'2026-03-10 16:19:43.534622','2026-03-10 16:19:43.534622',6,10),(880,'2026-03-10',0,'2026-03-10 16:19:43.540269','2026-03-10 16:19:43.540269',15,10),(881,'2026-03-10',0,'2026-03-10 16:19:43.552114','2026-03-10 16:19:43.552114',3,10),(882,'2026-03-10',0,'2026-03-10 16:19:43.558636','2026-03-10 16:19:43.558636',18,10),(883,'2026-03-10',0,'2026-03-10 16:19:43.568508','2026-03-10 16:19:43.568508',12,10),(884,'2026-03-10',0,'2026-03-10 16:19:43.576393','2026-03-10 16:19:43.576393',25,10),(885,'2026-03-10',0,'2026-03-10 16:19:43.586195','2026-03-10 16:19:43.586195',11,10),(886,'2026-03-10',0,'2026-03-10 16:19:43.592709','2026-03-10 16:19:43.592709',1,10),(887,'2026-03-10',0,'2026-03-10 16:19:43.602705','2026-03-10 16:19:43.602705',5,10),(888,'2026-03-10',0,'2026-03-10 16:19:43.608445','2026-03-10 16:19:43.608445',16,10),(889,'2026-03-10',0,'2026-03-10 16:19:43.616466','2026-03-10 16:19:43.616466',27,10),(890,'2026-03-10',0,'2026-03-10 16:19:43.625204','2026-03-10 16:19:43.625204',2,10),(891,'2026-03-10',0,'2026-03-10 16:19:43.634096','2026-03-10 16:19:43.634096',23,10),(892,'2026-03-10',0,'2026-03-10 16:19:43.641097','2026-03-10 16:19:43.641097',9,10),(893,'2026-03-10',0,'2026-03-10 16:19:43.647760','2026-03-10 16:19:43.647760',17,10),(894,'2026-03-10',0,'2026-03-10 16:19:43.655006','2026-03-10 16:19:43.655006',10,10),(895,'2026-03-10',0,'2026-03-10 16:19:43.661010','2026-03-10 16:19:43.661010',14,10),(896,'2026-03-10',0,'2026-03-10 16:19:43.666558','2026-03-10 16:19:43.666558',8,10);
/*!40000 ALTER TABLE `main_attendancerecord` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_attendancestatus`
--

DROP TABLE IF EXISTS `main_attendancestatus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_attendancestatus` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `code` varchar(30) NOT NULL,
  `label` varchar(100) NOT NULL,
  `sort_order` smallint unsigned NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`),
  CONSTRAINT `main_attendancestatus_chk_1` CHECK ((`sort_order` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_attendancestatus`
--

LOCK TABLES `main_attendancestatus` WRITE;
/*!40000 ALTER TABLE `main_attendancestatus` DISABLE KEYS */;
INSERT INTO `main_attendancestatus` VALUES (1,'extern','Extern (behandeling)',1,1,'2026-02-19 09:42:57.947161'),(2,'ziek','Ziek',2,1,'2026-02-19 09:42:57.951137'),(3,'training_aangepast','Training aangepast',3,1,'2026-02-19 09:42:57.953603'),(4,'training_uitgevallen','Training uitgevallen',4,1,'2026-02-19 09:42:57.955613'),(5,'training','Training',5,1,'2026-02-19 09:42:57.957678'),(6,'wedstrijd','Wedstrijd',6,1,'2026-02-19 09:42:57.959685'),(7,'training_o21','Training O21',7,1,'2026-02-19 09:42:57.960689'),(8,'wedstrijd_o21','Wedstrijd O21',8,1,'2026-02-19 09:42:57.961689'),(9,'fysio','Fysio',9,1,'2026-02-19 09:42:57.962993'),(10,'overig','Overig',10,1,'2026-02-19 09:42:57.964013');
/*!40000 ALTER TABLE `main_attendancestatus` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_beweeganalysebeoordeling`
--

DROP TABLE IF EXISTS `main_beweeganalysebeoordeling`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_beweeganalysebeoordeling` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `score` smallint unsigned DEFAULT NULL,
  `comment` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `punt_id` bigint NOT NULL,
  `sessie_id` bigint NOT NULL,
  `priority_flag` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_beweeganalyse_sessie_punt` (`sessie_id`,`punt_id`),
  KEY `main_beweeganalysebe_punt_id_c4846d64_fk_main_bewe` (`punt_id`),
  CONSTRAINT `main_beweeganalysebe_punt_id_c4846d64_fk_main_bewe` FOREIGN KEY (`punt_id`) REFERENCES `main_beweeganalysepunt` (`id`),
  CONSTRAINT `main_beweeganalysebe_sessie_id_e14587c7_fk_main_bewe` FOREIGN KEY (`sessie_id`) REFERENCES `main_beweeganalysesessie` (`id`),
  CONSTRAINT `ck_beweeganalyse_score_1_4` CHECK (((`score` is null) or ((`score` >= 1) and (`score` <= 4)))),
  CONSTRAINT `main_beweeganalysebeoordeling_chk_1` CHECK ((`score` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_beweeganalysebeoordeling`
--

LOCK TABLES `main_beweeganalysebeoordeling` WRITE;
/*!40000 ALTER TABLE `main_beweeganalysebeoordeling` DISABLE KEYS */;
/*!40000 ALTER TABLE `main_beweeganalysebeoordeling` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_beweeganalyseoefening`
--

DROP TABLE IF EXISTS `main_beweeganalyseoefening`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_beweeganalyseoefening` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `sort_order` smallint unsigned NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `punt_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_beweeganalyse_oefening_punt_name` (`punt_id`,`name`),
  CONSTRAINT `main_beweeganalyseoe_punt_id_408c80ef_fk_main_bewe` FOREIGN KEY (`punt_id`) REFERENCES `main_beweeganalysepunt` (`id`),
  CONSTRAINT `main_beweeganalyseoefening_chk_1` CHECK ((`sort_order` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_beweeganalyseoefening`
--

LOCK TABLES `main_beweeganalyseoefening` WRITE;
/*!40000 ALTER TABLE `main_beweeganalyseoefening` DISABLE KEYS */;
INSERT INTO `main_beweeganalyseoefening` VALUES (1,'TRX fall out',10,1,'2026-03-06 13:34:05.857810',1),(2,'Resisted sprints',20,1,'2026-03-06 13:34:05.859797',1),(3,'Weighted hip flexor lift',10,1,'2026-03-06 13:34:05.861796',2),(4,'0 deg hops',20,1,'2026-03-06 13:34:05.862813',2),(5,'Drop/depth jumps',10,1,'2026-03-06 13:34:05.864810',3),(6,'Split stance jumps (90 graden) / switch jumps',20,1,'2026-03-06 13:34:05.865811',3),(7,'Pogo switch jump',10,1,'2026-03-06 13:34:05.869797',4),(8,'Awkward farmer carries (met gewicht, arm boven/onder) + A-marches',20,1,'2026-03-06 13:34:05.870823',4),(9,'Hamstring switches (vanuit glute bridge) / SL hamstring eccentrisch falls',30,1,'2026-03-06 13:34:05.871811',4),(10,'Loopwerk/loopscholing met stok boven het hoofd',40,1,'2026-03-06 13:34:05.872811',4),(11,'Bounding',10,1,'2026-03-06 13:34:05.874535',5),(12,'Wall drills (verticaal)',20,1,'2026-03-06 13:34:05.875534',5),(13,'Pogo\'s (double leg/single leg, split stance)',10,1,'2026-03-06 13:34:05.877534',6),(14,'Bounding (horizontal) op snelheid',20,1,'2026-03-06 13:34:05.878532',6),(15,'Max effort 90 degree hop',10,1,'2026-03-06 13:34:05.880533',7),(16,'Depth jump (zijwaarts landen)',20,1,'2026-03-06 13:34:05.881533',7),(17,'Broad jump max effort zero degree turn',30,1,'2026-03-06 13:34:05.882534',7),(18,'Max effort 90 degree hop',10,1,'2026-03-06 13:34:05.884535',10),(19,'Depth jump (zijwaarts landen)',20,1,'2026-03-06 13:34:05.886534',10),(20,'Broad jump max effort zero degree turn',30,1,'2026-03-06 13:34:05.887090',10),(21,'Skater jumps (variant kiezen)',10,1,'2026-03-06 13:34:05.887090',8),(22,'Inner decel (depth jump) / running direction change',20,1,'2026-03-06 13:34:05.887090',8),(23,'Broad jump max effort zero degree turn',30,1,'2026-03-06 13:34:05.887090',8),(24,'Extra (rotatie): oblique oefeningen, alleen inzetten als speler er klaar voor is',40,1,'2026-03-06 13:34:05.887090',8),(25,'Skater jumps (variant kiezen)',10,1,'2026-03-06 13:34:05.887090',11),(26,'Inner decel (depth jump) / running direction change',20,1,'2026-03-06 13:34:05.887090',11),(27,'Broad jump max effort zero degree turn',30,1,'2026-03-06 13:34:05.887090',11),(28,'Extra (rotatie): oblique oefeningen, alleen inzetten als speler er klaar voor is',40,1,'2026-03-06 13:34:05.887090',11);
/*!40000 ALTER TABLE `main_beweeganalyseoefening` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_beweeganalyseonderdeel`
--

DROP TABLE IF EXISTS `main_beweeganalyseonderdeel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_beweeganalyseonderdeel` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(120) NOT NULL,
  `sort_order` smallint unsigned NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  CONSTRAINT `main_beweeganalyseonderdeel_chk_1` CHECK ((`sort_order` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_beweeganalyseonderdeel`
--

LOCK TABLES `main_beweeganalyseonderdeel` WRITE;
/*!40000 ALTER TABLE `main_beweeganalyseonderdeel` DISABLE KEYS */;
INSERT INTO `main_beweeganalyseonderdeel` VALUES (1,'Sprint – Acceleratie (0–10m)',10,1,'2026-03-06 09:17:50.882057'),(2,'Sprint – Top Speed (20–30m)',20,1,'2026-03-06 09:17:50.892059'),(3,'COD – 180° -> 180° (Links)',30,1,'2026-03-06 09:17:50.898574'),(4,'COD – 180° -> 180° (Rechts)',40,1,'2026-03-06 09:17:50.902588'),(5,'Medisch',50,1,'2026-03-06 11:58:48.270612');
/*!40000 ALTER TABLE `main_beweeganalyseonderdeel` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_beweeganalysepunt`
--

DROP TABLE IF EXISTS `main_beweeganalysepunt`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_beweeganalysepunt` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(80) NOT NULL,
  `focus_text` varchar(255) NOT NULL,
  `sort_order` smallint unsigned NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `onderdeel_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_beweeganalyse_punt_template` (`onderdeel_id`,`title`,`sort_order`),
  CONSTRAINT `main_beweeganalysepu_onderdeel_id_cba4b035_fk_main_bewe` FOREIGN KEY (`onderdeel_id`) REFERENCES `main_beweeganalyseonderdeel` (`id`),
  CONSTRAINT `main_beweeganalysepunt_chk_1` CHECK ((`sort_order` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_beweeganalysepunt`
--

LOCK TABLES `main_beweeganalysepunt` WRITE;
/*!40000 ALTER TABLE `main_beweeganalysepunt` DISABLE KEYS */;
INSERT INTO `main_beweeganalysepunt` VALUES (1,'Posture','Diagonale Lijn, Rechte Rug',10,1,'2026-03-06 09:17:50.885061',1),(2,'Hiplock','Knee Drive',20,1,'2026-03-06 09:17:50.888058',1),(3,'Footplant','Ankle Stiffness',30,1,'2026-03-06 09:17:50.890066',1),(4,'Posture','12:05 Height, Core Control',10,1,'2026-03-06 09:17:50.893576',2),(5,'Hiplock','Knee Drive',20,1,'2026-03-06 09:17:50.894575',2),(6,'Footplant','Ankle Stiffness, Voetpositie Neutraal',30,1,'2026-03-06 09:17:50.896575',2),(7,'Posture','Diagonale Lijn, Low Stance, Trunk Position',10,1,'2026-03-06 09:17:50.899572',3),(8,'Hiplock','Vervolg Stap, Volledige Draai (Geen Overstap)',20,1,'2026-03-06 09:17:50.900593',3),(9,'Footplant','Ankle Stiffness, Voetpositie Neutraal',30,1,'2026-03-06 09:17:50.901573',3),(10,'Posture','Diagonale Lijn, Low Stance, Trunk Position',10,1,'2026-03-06 09:17:50.904576',4),(11,'Hiplock','Vervolg Stap, Volledige Draai (Geen Overstap)',20,1,'2026-03-06 09:17:50.905916',4),(12,'Footplant','Ankle Stiffness, Voetpositie Neutraal',30,1,'2026-03-06 09:17:50.907926',4),(13,'Zittende loopstijl','Lopen op de hakken, been voor zich leidt tot een overmatig gebruik van de quadriceps.',10,1,'2026-03-06 11:58:48.282218',5),(14,'Knie lijn (180 graden)','Gasbeen strikt in de looprichting houden; knie in lijn houden zonder afwijking naar binnen of buiten.',20,1,'2026-03-06 11:58:48.282218',5);
/*!40000 ALTER TABLE `main_beweeganalysepunt` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_beweeganalysesessie`
--

DROP TABLE IF EXISTS `main_beweeganalysesessie`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_beweeganalysesessie` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `player_id` bigint NOT NULL,
  `video_file` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_beweeganalyse_sessie_player_date` (`player_id`,`date`),
  CONSTRAINT `main_beweeganalysesessie_player_id_2645f0e8_fk_main_player_id` FOREIGN KEY (`player_id`) REFERENCES `main_player` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_beweeganalysesessie`
--

LOCK TABLES `main_beweeganalysesessie` WRITE;
/*!40000 ALTER TABLE `main_beweeganalysesessie` DISABLE KEYS */;
INSERT INTO `main_beweeganalysesessie` VALUES (1,'2026-03-06','2026-03-06 14:01:17.133815','2026-03-06 14:02:37.463564',21,'');
/*!40000 ALTER TABLE `main_beweeganalysesessie` ENABLE KEYS */;
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
-- Table structure for table `main_fieldrehabcomponent`
--

DROP TABLE IF EXISTS `main_fieldrehabcomponent`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_fieldrehabcomponent` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_fieldrehabcomponent`
--

LOCK TABLES `main_fieldrehabcomponent` WRITE;
/*!40000 ALTER TABLE `main_fieldrehabcomponent` DISABLE KEYS */;
INSERT INTO `main_fieldrehabcomponent` VALUES (1,'Slalom loop 100m met bal',1,'2026-02-23 11:00:32.533672'),(2,'Hardlopen tot 12 km/u rechte stukken',1,'2026-02-23 11:00:32.535185'),(3,'Hardlopen tot 15 km/u rechte stukken',1,'2026-02-23 11:00:32.535185'),(4,'Slalom loop 100m zonder bal',1,'2026-02-23 11:00:32.535185');
/*!40000 ALTER TABLE `main_fieldrehabcomponent` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_fieldrehabmetric`
--

DROP TABLE IF EXISTS `main_fieldrehabmetric`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_fieldrehabmetric` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `value` int unsigned NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `metric_type_id` bigint NOT NULL,
  `session_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_fieldrehab_metric_per_session` (`session_id`,`metric_type_id`),
  KEY `main_fieldr_session_143f39_idx` (`session_id`,`metric_type_id`),
  KEY `main_fieldr_metric__0a182e_idx` (`metric_type_id`,`value`),
  CONSTRAINT `main_fieldrehabmetri_metric_type_id_126f2619_fk_main_fiel` FOREIGN KEY (`metric_type_id`) REFERENCES `main_fieldrehabmetrictype` (`id`),
  CONSTRAINT `main_fieldrehabmetri_session_id_7693929a_fk_main_fiel` FOREIGN KEY (`session_id`) REFERENCES `main_fieldrehabsession` (`id`),
  CONSTRAINT `main_fieldrehabmetric_chk_1` CHECK ((`value` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_fieldrehabmetric`
--

LOCK TABLES `main_fieldrehabmetric` WRITE;
/*!40000 ALTER TABLE `main_fieldrehabmetric` DISABLE KEYS */;
INSERT INTO `main_fieldrehabmetric` VALUES (1,45,'2026-02-26 07:15:15.122229','2026-02-26 07:15:15.122229',1,2),(2,8,'2026-02-26 07:15:15.122229','2026-02-26 07:15:15.122229',2,2),(3,4500,'2026-02-26 07:15:15.122229','2026-02-26 07:15:15.122229',3,2),(4,45,'2026-02-26 07:15:15.122229','2026-02-26 07:15:15.122229',1,1);
/*!40000 ALTER TABLE `main_fieldrehabmetric` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_fieldrehabmetrictype`
--

DROP TABLE IF EXISTS `main_fieldrehabmetrictype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_fieldrehabmetrictype` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `code` varchar(50) NOT NULL,
  `name` varchar(100) NOT NULL,
  `unit` varchar(20) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_fieldrehabmetrictype`
--

LOCK TABLES `main_fieldrehabmetrictype` WRITE;
/*!40000 ALTER TABLE `main_fieldrehabmetrictype` DISABLE KEYS */;
INSERT INTO `main_fieldrehabmetrictype` VALUES (1,'duur','Duur','min',1,'2026-02-26 07:15:15.106169'),(2,'rpe','RPE',NULL,1,'2026-02-26 07:15:15.108181'),(3,'totale_afstand','Totale afstand','m',1,'2026-02-26 07:15:15.110476'),(4,'afstand_20','Afstand >20','m',1,'2026-02-26 07:15:15.111335'),(5,'afstand_25','Afstand >25','m',1,'2026-02-26 07:15:15.113344'),(6,'acceleraties','Acceleraties',NULL,1,'2026-02-26 07:15:15.116024'),(7,'deceleraties','Deceleraties',NULL,1,'2026-02-26 07:15:15.116024');
/*!40000 ALTER TABLE `main_fieldrehabmetrictype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_fieldrehabphase`
--

DROP TABLE IF EXISTS `main_fieldrehabphase`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_fieldrehabphase` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_fieldrehabphase`
--

LOCK TABLES `main_fieldrehabphase` WRITE;
/*!40000 ALTER TABLE `main_fieldrehabphase` DISABLE KEYS */;
INSERT INTO `main_fieldrehabphase` VALUES (1,'Fase 1',1,'2026-02-23 11:00:32.531655');
/*!40000 ALTER TABLE `main_fieldrehabphase` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_fieldrehabsession`
--

DROP TABLE IF EXISTS `main_fieldrehabsession`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_fieldrehabsession` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `afgevinkt` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `player_id` bigint NOT NULL,
  `onderdeel_ref_id` bigint DEFAULT NULL,
  `phase_ref_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `main_fieldrehabsessi_onderdeel_ref_id_ef70932c_fk_main_fiel` (`onderdeel_ref_id`),
  KEY `main_fieldr_player__292ad7_idx` (`player_id`,`created_at`),
  KEY `main_fieldr_phase_r_edbaf4_idx` (`phase_ref_id`,`onderdeel_ref_id`),
  CONSTRAINT `main_fieldrehabsessi_onderdeel_ref_id_ef70932c_fk_main_fiel` FOREIGN KEY (`onderdeel_ref_id`) REFERENCES `main_fieldrehabcomponent` (`id`),
  CONSTRAINT `main_fieldrehabsessi_phase_ref_id_42844274_fk_main_fiel` FOREIGN KEY (`phase_ref_id`) REFERENCES `main_fieldrehabphase` (`id`),
  CONSTRAINT `main_fieldrehabsession_player_id_a4093375_fk_main_player_id` FOREIGN KEY (`player_id`) REFERENCES `main_player` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_fieldrehabsession`
--

LOCK TABLES `main_fieldrehabsession` WRITE;
/*!40000 ALTER TABLE `main_fieldrehabsession` DISABLE KEYS */;
INSERT INTO `main_fieldrehabsession` VALUES (1,1,'2025-11-13 06:29:56.198906',24,1,1),(2,1,'2025-11-13 06:37:48.550663',13,2,1),(3,1,'2025-11-13 06:37:48.566406',13,3,1),(4,1,'2025-11-13 06:37:48.570737',13,4,1),(5,0,'2025-11-13 06:37:48.575610',13,1,1);
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
-- Table structure for table `main_hitasrplanentry`
--

DROP TABLE IF EXISTS `main_hitasrplanentry`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_hitasrplanentry` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `mss_kmh` decimal(5,2) NOT NULL,
  `mas_kmh` decimal(5,2) NOT NULL,
  `target_speed_kmh` decimal(6,2) NOT NULL,
  `asr_kmh` decimal(5,2) NOT NULL,
  `pct_mas` decimal(6,2) NOT NULL,
  `pct_asr` decimal(6,2) DEFAULT NULL,
  `indication` varchar(40) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `player_id` bigint NOT NULL,
  `session_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_hit_asr_plan_session_player` (`session_id`,`player_id`),
  KEY `main_hitasr_session_33b779_idx` (`session_id`,`player_id`),
  KEY `main_hitasr_player__061754_idx` (`player_id`,`created_at`),
  CONSTRAINT `main_hitasrplanentry_player_id_c75959bf_fk_main_player_id` FOREIGN KEY (`player_id`) REFERENCES `main_player` (`id`),
  CONSTRAINT `main_hitasrplanentry_session_id_dfc72a5d_fk_main_hita` FOREIGN KEY (`session_id`) REFERENCES `main_hitasrplansession` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_hitasrplanentry`
--

LOCK TABLES `main_hitasrplanentry` WRITE;
/*!40000 ALTER TABLE `main_hitasrplanentry` DISABLE KEYS */;
/*!40000 ALTER TABLE `main_hitasrplanentry` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_hitasrplansession`
--

DROP TABLE IF EXISTS `main_hitasrplansession`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_hitasrplansession` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `session_date` date NOT NULL,
  `mas_percent` decimal(6,2) NOT NULL,
  `reference_speed_kmh` decimal(6,2) DEFAULT NULL,
  `notes` varchar(255) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `main_hitasr_session_3026b4_idx` (`session_date`),
  KEY `main_hitasr_created_9656eb_idx` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_hitasrplansession`
--

LOCK TABLES `main_hitasrplansession` WRITE;
/*!40000 ALTER TABLE `main_hitasrplansession` DISABLE KEYS */;
/*!40000 ALTER TABLE `main_hitasrplansession` ENABLE KEYS */;
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
-- Table structure for table `main_individualdayplan`
--

DROP TABLE IF EXISTS `main_individualdayplan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_individualdayplan` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `player_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_individual_day_plan_player_date` (`player_id`,`date`),
  CONSTRAINT `main_individualdayplan_player_id_c10f55ec_fk_main_player_id` FOREIGN KEY (`player_id`) REFERENCES `main_player` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_individualdayplan`
--

LOCK TABLES `main_individualdayplan` WRITE;
/*!40000 ALTER TABLE `main_individualdayplan` DISABLE KEYS */;
INSERT INTO `main_individualdayplan` VALUES (1,'2025-11-21','2026-02-19 09:42:58.242132','2026-02-19 09:42:58.242132',6),(2,'2025-11-25','2026-02-19 09:42:58.292009','2026-02-19 09:42:58.292009',7),(3,'2025-11-21','2026-02-19 09:42:58.377449','2026-02-19 09:42:58.377449',9),(4,'2025-11-21','2026-02-19 09:42:58.539748','2026-02-19 09:42:58.539748',13),(5,'2025-11-21','2026-02-19 09:42:58.868748','2026-02-19 09:42:58.868748',21),(6,'2025-11-22','2026-02-19 09:42:58.870744','2026-02-19 09:42:58.870744',21),(7,'2025-11-24','2026-02-19 09:42:58.875169','2026-02-19 09:42:58.875169',21),(8,'2025-11-26','2026-02-19 09:42:58.878149','2026-02-19 09:42:58.878149',21),(9,'2025-11-28','2026-02-19 09:42:58.881151','2026-02-19 09:42:58.881151',21),(10,'2025-12-02','2026-02-19 09:42:58.883151','2026-02-19 09:42:58.883151',21),(11,'2025-12-06','2026-02-19 09:42:58.885150','2026-02-19 09:42:58.885150',21),(12,'2025-12-13','2026-02-19 09:42:58.887147','2026-02-19 09:42:58.888147',21),(13,'2025-12-18','2026-02-19 09:42:58.892027','2026-02-19 09:42:58.892027',21),(14,'2025-12-12','2026-02-19 09:42:58.932456','2026-02-19 09:42:58.932456',22),(15,'2025-11-22','2026-02-19 09:42:58.975070','2026-02-19 09:42:58.975070',23),(16,'2026-02-06','2026-02-19 09:42:58.977070','2026-02-19 09:42:58.977070',23),(17,'2026-02-12','2026-02-19 09:42:58.979071','2026-02-19 09:42:58.979071',23),(18,'2025-11-21','2026-02-19 09:42:59.019122','2026-02-19 09:42:59.019122',24),(19,'2025-11-21','2026-02-19 09:42:59.184860','2026-02-19 09:42:59.184860',28),(20,'2026-03-06','2026-03-06 15:44:19.031709','2026-03-06 15:44:19.031709',11),(21,'2026-03-08','2026-03-08 14:53:40.379235','2026-03-08 14:53:40.379235',21);
/*!40000 ALTER TABLE `main_individualdayplan` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_individualdayplannote`
--

DROP TABLE IF EXISTS `main_individualdayplannote`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_individualdayplannote` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `content` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `plan_id` bigint NOT NULL,
  `note_type_ref_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_individual_day_plan_note_type` (`plan_id`,`note_type_ref_id`),
  KEY `main_individualdayplannote_plan_id_77a3ed5f` (`plan_id`),
  KEY `main_individualdaypl_note_type_ref_id_d66197a7_fk_main_indi` (`note_type_ref_id`),
  CONSTRAINT `main_individualdaypl_note_type_ref_id_d66197a7_fk_main_indi` FOREIGN KEY (`note_type_ref_id`) REFERENCES `main_individualdayplannotetype` (`id`),
  CONSTRAINT `main_individualdaypl_plan_id_77a3ed5f_fk_main_indi` FOREIGN KEY (`plan_id`) REFERENCES `main_individualdayplan` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_individualdayplannote`
--

LOCK TABLES `main_individualdayplannote` WRITE;
/*!40000 ALTER TABLE `main_individualdayplannote` DISABLE KEYS */;
INSERT INTO `main_individualdayplannote` VALUES (1,'','2026-02-19 09:42:58.244130','2026-02-19 09:42:58.244130',1,1),(2,'','2026-02-19 09:42:58.294014','2026-02-19 09:42:58.294014',2,1),(3,'','2026-02-19 09:42:58.378439','2026-02-19 09:42:58.378439',3,1),(4,'','2026-02-19 09:42:58.539748','2026-02-19 09:42:58.539748',4,1),(5,'','2026-02-19 09:42:58.869745','2026-02-19 09:42:58.869745',5,1),(6,'','2026-02-19 09:42:58.873002','2026-02-19 09:42:58.873002',6,1),(7,'','2026-02-19 09:42:58.877151','2026-02-19 09:42:58.877151',7,1),(8,'','2026-02-19 09:42:58.879147','2026-02-19 09:42:58.879147',8,1),(9,'','2026-02-19 09:42:58.882148','2026-02-19 09:42:58.882148',9,1),(10,'','2026-02-19 09:42:58.884148','2026-02-19 09:42:58.884148',10,1),(11,'','2026-02-19 09:42:58.886148','2026-02-19 09:42:58.887147',11,1),(12,'','2026-02-19 09:42:58.889616','2026-02-19 09:42:58.889616',12,1),(13,'','2026-02-19 09:42:58.893036','2026-02-19 09:42:58.893036',13,1),(14,'','2026-02-19 09:42:58.934456','2026-02-19 09:42:58.934456',14,1),(15,'','2026-02-19 09:42:58.976070','2026-02-19 09:42:58.976070',15,1),(16,'','2026-02-19 09:42:58.978070','2026-02-19 09:42:58.978070',16,1),(17,'','2026-02-19 09:42:58.980070','2026-02-19 09:42:58.980070',17,1),(18,'','2026-02-19 09:42:59.020122','2026-02-19 09:42:59.020122',18,1),(19,'Werken aan schouder','2026-02-19 09:42:59.185857','2026-02-19 09:42:59.185857',19,1),(20,'','2026-03-06 15:44:19.070002','2026-03-06 15:44:19.070002',20,1),(21,'','2026-03-08 14:53:40.397804','2026-03-08 14:53:40.397804',21,1);
/*!40000 ALTER TABLE `main_individualdayplannote` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_individualdayplannotetype`
--

DROP TABLE IF EXISTS `main_individualdayplannotetype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_individualdayplannotetype` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `code` varchar(50) NOT NULL,
  `label` varchar(100) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_individualdayplannotetype`
--

LOCK TABLES `main_individualdayplannotetype` WRITE;
/*!40000 ALTER TABLE `main_individualdayplannotetype` DISABLE KEYS */;
INSERT INTO `main_individualdayplannotetype` VALUES (1,'program_text','Programma tekst',1,'2026-03-03 14:01:06.358147');
/*!40000 ALTER TABLE `main_individualdayplannotetype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_injurycase`
--

DROP TABLE IF EXISTS `main_injurycase`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_injurycase` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `started_on` date DEFAULT NULL,
  `expected_return_on` date DEFAULT NULL,
  `closed_on` date DEFAULT NULL,
  `notes` longtext,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `player_id` bigint NOT NULL,
  `injury_type_ref_id` bigint DEFAULT NULL,
  `phase_ref_id` bigint DEFAULT NULL,
  `status_ref_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `main_injury_started_738f54_idx` (`started_on`),
  KEY `main_injurycase_injury_type_ref_id_7e18f7de_fk_main_inju` (`injury_type_ref_id`),
  KEY `main_injurycase_phase_ref_id_b061a012_fk_main_injuryphase_id` (`phase_ref_id`),
  KEY `main_injurycase_status_ref_id_63c206e8_fk_main_injurystatus_id` (`status_ref_id`),
  KEY `main_injury_player__503bda_idx` (`player_id`,`status_ref_id`),
  CONSTRAINT `main_injurycase_injury_type_ref_id_7e18f7de_fk_main_inju` FOREIGN KEY (`injury_type_ref_id`) REFERENCES `main_injurytype` (`id`),
  CONSTRAINT `main_injurycase_phase_ref_id_b061a012_fk_main_injuryphase_id` FOREIGN KEY (`phase_ref_id`) REFERENCES `main_injuryphase` (`id`),
  CONSTRAINT `main_injurycase_player_id_8fdf68a6_fk_main_player_id` FOREIGN KEY (`player_id`) REFERENCES `main_player` (`id`),
  CONSTRAINT `main_injurycase_status_ref_id_63c206e8_fk_main_injurystatus_id` FOREIGN KEY (`status_ref_id`) REFERENCES `main_injurystatus` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_injurycase`
--

LOCK TABLES `main_injurycase` WRITE;
/*!40000 ALTER TABLE `main_injurycase` DISABLE KEYS */;
INSERT INTO `main_injurycase` VALUES (1,'2025-10-25','2025-11-15',NULL,'Backfill vanuit legacy Injury','2026-02-18 10:31:10.932017','2026-02-18 10:31:10.932017',10,1,1,1),(2,'2025-11-21','2025-12-15',NULL,'Backfill vanuit legacy Injury','2026-02-18 10:31:10.941690','2026-02-18 10:31:10.941690',13,2,2,1),(3,'2025-12-15','2026-01-09',NULL,'Backfill vanuit legacy Injury','2026-02-18 10:31:10.943690','2026-02-18 10:31:10.943690',5,3,1,1);
/*!40000 ALTER TABLE `main_injurycase` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_injuryphase`
--

DROP TABLE IF EXISTS `main_injuryphase`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_injuryphase` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `code` varchar(50) NOT NULL,
  `label` varchar(100) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_injuryphase`
--

LOCK TABLES `main_injuryphase` WRITE;
/*!40000 ALTER TABLE `main_injuryphase` DISABLE KEYS */;
INSERT INTO `main_injuryphase` VALUES (1,'early','Vroege fase',1,'2026-02-23 10:54:52.721460'),(2,'mid','Middenfase',1,'2026-02-23 10:54:52.723471'),(3,'final','Laatste fase',1,'2026-02-23 10:54:52.725481');
/*!40000 ALTER TABLE `main_injuryphase` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_injurystatus`
--

DROP TABLE IF EXISTS `main_injurystatus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_injurystatus` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `code` varchar(30) NOT NULL,
  `label` varchar(100) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_injurystatus`
--

LOCK TABLES `main_injurystatus` WRITE;
/*!40000 ALTER TABLE `main_injurystatus` DISABLE KEYS */;
INSERT INTO `main_injurystatus` VALUES (1,'active','Actief',1,'2026-02-23 10:54:52.725481'),(2,'closed','Afgesloten',1,'2026-02-23 10:54:52.725481');
/*!40000 ALTER TABLE `main_injurystatus` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_injurytype`
--

DROP TABLE IF EXISTS `main_injurytype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_injurytype` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_injurytype`
--

LOCK TABLES `main_injurytype` WRITE;
/*!40000 ALTER TABLE `main_injurytype` DISABLE KEYS */;
INSERT INTO `main_injurytype` VALUES (1,'Kuitblessure (scheurtje)',1,'2026-02-23 10:54:52.737164'),(2,'Heup',1,'2026-02-23 10:54:52.743204'),(3,'Knieblessure',1,'2026-02-23 10:54:52.745213');
/*!40000 ALTER TABLE `main_injurytype` ENABLE KEYS */;
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
  `away_team_id` bigint NOT NULL,
  `home_team_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_match` (`kickoff`,`home_team_id`,`away_team_id`),
  KEY `main_match_away_team_id_9618ee13_fk_main_team_id` (`away_team_id`),
  KEY `main_match_home_team_id_56ccfad5_fk_main_team_id` (`home_team_id`),
  CONSTRAINT `main_match_away_team_id_9618ee13_fk_main_team_id` FOREIGN KEY (`away_team_id`) REFERENCES `main_team` (`id`),
  CONSTRAINT `main_match_home_team_id_56ccfad5_fk_main_team_id` FOREIGN KEY (`home_team_id`) REFERENCES `main_team` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=52 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_match`
--

LOCK TABLES `main_match` WRITE;
/*!40000 ALTER TABLE `main_match` DISABLE KEYS */;
INSERT INTO `main_match` VALUES (27,'2025-11-03 19:00:00.000000',2,1),(28,'2025-11-07 19:00:00.000000',3,2),(29,'2025-11-15 20:00:00.000000',4,2),(30,'2025-11-21 19:00:00.000000',2,5),(31,'2025-11-28 19:00:00.000000',2,6),(32,'2025-12-06 15:30:00.000000',7,2),(33,'2025-12-12 19:00:00.000000',8,2),(34,'2025-12-18 20:00:00.000000',9,2),(35,'2025-12-21 13:30:00.000000',2,10),(36,'2026-01-09 19:00:00.000000',11,2),(37,'2026-01-23 19:00:00.000000',5,2),(38,'2026-02-02 19:00:00.000000',2,12),(39,'2026-02-08 13:30:00.000000',13,2),(40,'2026-02-16 19:00:00.000000',2,14),(41,'2026-02-20 19:00:00.000000',15,2),(42,'2026-02-27 19:00:00.000000',2,4),(43,'2026-03-08 13:30:00.000000',6,2),(44,'2026-03-13 19:00:00.000000',2,3),(45,'2026-03-22 15:45:00.000000',2,16),(46,'2026-03-27 11:00:00.000000',17,2),(47,'2026-04-03 18:00:00.000000',1,2),(48,'2026-04-06 14:45:00.000000',2,18),(49,'2026-04-12 14:45:00.000000',19,2),(50,'2026-04-17 18:00:00.000000',20,2),(51,'2026-04-24 18:00:00.000000',2,7);
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
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_nutritionintakeitem`
--

LOCK TABLES `main_nutritionintakeitem` WRITE;
/*!40000 ALTER TABLE `main_nutritionintakeitem` DISABLE KEYS */;
INSERT INTO `main_nutritionintakeitem` VALUES (1,'breakfast','','2026-02-18 11:47:42.695563',1),(2,'snack1','','2026-02-18 11:47:42.695563',1),(3,'lunch','','2026-02-18 11:47:42.695563',1),(4,'snack2','','2026-02-18 11:47:42.695563',1),(5,'dinner','','2026-02-18 11:47:42.695563',1),(6,'snack3','','2026-02-18 11:47:42.695563',1),(7,'supplements','','2026-02-18 11:47:42.695563',1),(8,'breakfast','Fruit + yoghurt','2026-02-18 11:49:45.010002',2),(9,'snack1','Banaan','2026-02-18 11:49:45.013824',2),(10,'lunch','Pannenkoeken','2026-02-18 11:49:45.015701',2),(11,'snack2','Noten','2026-02-18 11:49:45.019147',2),(12,'dinner','Pasta met kip','2026-02-18 11:49:45.021492',2),(13,'snack3','Kwark','2026-02-18 11:49:45.023657',2),(14,'supplements','','2026-02-18 11:49:45.026403',2),(15,'breakfast','Fruit + yoghurt','2026-02-18 12:07:41.770433',3),(16,'snack1','Banaan','2026-02-18 12:07:41.773356',3),(17,'lunch','Pannenkoeken','2026-02-18 12:07:41.775713',3),(18,'snack2','Noten','2026-02-18 12:07:41.776722',3),(19,'dinner','Pasta met kip','2026-02-18 12:07:41.782342',3),(20,'snack3','Kwark','2026-02-18 12:07:41.784349',3),(21,'supplements','','2026-02-18 12:07:41.786357',3),(22,'breakfast','Kwark','2026-02-18 13:45:38.235000',4),(23,'snack1','Noten','2026-02-18 13:45:38.249744',4),(24,'lunch','Kwark','2026-02-18 13:45:38.251661',4),(25,'snack2','Brood met ei','2026-02-18 13:45:38.251661',4),(26,'dinner','pasta met kip','2026-02-18 13:45:38.251661',4),(27,'snack3','Kwark met noten','2026-02-18 13:45:38.251661',4),(28,'supplements','','2026-02-18 13:45:38.251661',4);
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
  UNIQUE KEY `uniq_nutri_session_player_date` (`player_id`,`date`),
  KEY `main_nutrit_player__b27b72_idx` (`player_id`,`date`),
  CONSTRAINT `main_nutritionintakesession_player_id_5606b94f_fk_main_player_id` FOREIGN KEY (`player_id`) REFERENCES `main_player` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_nutritionintakesession`
--

LOCK TABLES `main_nutritionintakesession` WRITE;
/*!40000 ALTER TABLE `main_nutritionintakesession` DISABLE KEYS */;
INSERT INTO `main_nutritionintakesession` VALUES (1,NULL,'','','2026-02-18 11:47:42.692664','2026-02-18 11:47:42.692664',21),(2,NULL,'aankomen','','2026-02-18 11:49:45.010002','2026-02-18 11:49:45.010002',12),(3,NULL,'aankomen','','2026-02-18 12:07:41.766411','2026-02-18 12:07:41.766411',19),(4,NULL,'Spiermassa','','2026-02-18 13:45:38.235000','2026-02-18 13:45:38.235000',5);
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
  `exercise` varchar(150) DEFAULT NULL,
  `description` text,
  `sets_reps` varchar(50) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `focus_point_ref_id` bigint DEFAULT NULL,
  `phase_ref_id` bigint DEFAULT NULL,
  `program_type_ref_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `main_oefening_player_id_fk` (`player_id`),
  KEY `main_oefening_focus_point_ref_id_c6bf00e3_fk_main_oefe` (`focus_point_ref_id`),
  KEY `main_oefening_phase_ref_id_2dedce82_fk_main_oefeningphase_id` (`phase_ref_id`),
  KEY `main_oefeni_program_6fa76b_idx` (`program_type_ref_id`,`phase_ref_id`),
  CONSTRAINT `main_oefening_focus_point_ref_id_c6bf00e3_fk_main_oefe` FOREIGN KEY (`focus_point_ref_id`) REFERENCES `main_oefeningfocuspoint` (`id`),
  CONSTRAINT `main_oefening_phase_ref_id_2dedce82_fk_main_oefeningphase_id` FOREIGN KEY (`phase_ref_id`) REFERENCES `main_oefeningphase` (`id`),
  CONSTRAINT `main_oefening_player_id_fk` FOREIGN KEY (`player_id`) REFERENCES `main_player` (`id`),
  CONSTRAINT `main_oefening_program_type_ref_id_3d1dd87e_fk_main_oefe` FOREIGN KEY (`program_type_ref_id`) REFERENCES `main_oefeningprogramtype` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_oefening`
--

LOCK TABLES `main_oefening` WRITE;
/*!40000 ALTER TABLE `main_oefening` DISABLE KEYS */;
INSERT INTO `main_oefening` VALUES (1,NULL,NULL,NULL,NULL,NULL,'Nordic hamstring ','Rustig uitvoeren','3x8','2025-11-10 10:38:42',NULL,1,NULL);
/*!40000 ALTER TABLE `main_oefening` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_oefeningfocuspoint`
--

DROP TABLE IF EXISTS `main_oefeningfocuspoint`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_oefeningfocuspoint` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_oefeningfocuspoint`
--

LOCK TABLES `main_oefeningfocuspoint` WRITE;
/*!40000 ALTER TABLE `main_oefeningfocuspoint` DISABLE KEYS */;
/*!40000 ALTER TABLE `main_oefeningfocuspoint` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_oefeningphase`
--

DROP TABLE IF EXISTS `main_oefeningphase`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_oefeningphase` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_oefeningphase`
--

LOCK TABLES `main_oefeningphase` WRITE;
/*!40000 ALTER TABLE `main_oefeningphase` DISABLE KEYS */;
INSERT INTO `main_oefeningphase` VALUES (1,'Fase 1 – Pijnvrij bewegen',1,'2026-02-26 07:15:14.919837');
/*!40000 ALTER TABLE `main_oefeningphase` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_oefeningprogramtype`
--

DROP TABLE IF EXISTS `main_oefeningprogramtype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_oefeningprogramtype` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_oefeningprogramtype`
--

LOCK TABLES `main_oefeningprogramtype` WRITE;
/*!40000 ALTER TABLE `main_oefeningprogramtype` DISABLE KEYS */;
/*!40000 ALTER TABLE `main_oefeningprogramtype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_overignote`
--

DROP TABLE IF EXISTS `main_overignote`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_overignote` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `note_type` varchar(20) NOT NULL,
  `page_key` varchar(50) DEFAULT NULL,
  `section_key` varchar(50) DEFAULT NULL,
  `text` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `main_overig_note_ty_12667b_idx` (`note_type`,`page_key`,`section_key`),
  KEY `main_overig_created_a44713_idx` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_overignote`
--

LOCK TABLES `main_overignote` WRITE;
/*!40000 ALTER TABLE `main_overignote` DISABLE KEYS */;
/*!40000 ALTER TABLE `main_overignote` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_performancemetric`
--

DROP TABLE IF EXISTS `main_performancemetric`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_performancemetric` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `value` double NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `metric_type_id` bigint NOT NULL,
  `session_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_perf_metric_per_session_type` (`session_id`,`metric_type_id`),
  KEY `main_perfor_metric__11adaa_idx` (`metric_type_id`,`value`),
  CONSTRAINT `main_performancemetr_metric_type_id_c103db62_fk_main_perf` FOREIGN KEY (`metric_type_id`) REFERENCES `main_performancemetrictype` (`id`),
  CONSTRAINT `main_performancemetr_session_id_35325180_fk_main_perf` FOREIGN KEY (`session_id`) REFERENCES `main_performancesession` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=181 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_performancemetric`
--

LOCK TABLES `main_performancemetric` WRITE;
/*!40000 ALTER TABLE `main_performancemetric` DISABLE KEYS */;
INSERT INTO `main_performancemetric` VALUES (1,4923.07,'2026-02-20 09:28:14.147962',1,1),(2,252.66,'2026-02-20 09:28:14.150964',2,1),(3,18,'2026-02-20 09:28:14.154178',3,1),(4,0,'2026-02-20 09:28:14.157192',4,1),(5,2562.99,'2026-02-20 09:28:14.161481',1,2),(6,107.92,'2026-02-20 09:28:14.164483',2,2),(7,7,'2026-02-20 09:28:14.166481',3,2),(8,0,'2026-02-20 09:28:14.169817',4,2),(9,5553.05,'2026-02-20 09:28:14.173925',1,3),(10,327.84,'2026-02-20 09:28:14.175924',2,3),(11,22,'2026-02-20 09:28:14.177925',3,3),(12,0,'2026-02-20 09:28:14.179925',4,3),(13,4539.43,'2026-02-20 09:28:14.184449',1,4),(14,319.49,'2026-02-20 09:28:14.187769',2,4),(15,21,'2026-02-20 09:28:14.190767',3,4),(16,0,'2026-02-20 09:28:14.191772',4,4),(17,4888.68,'2026-02-20 09:28:14.196770',1,5),(18,215.04,'2026-02-20 09:28:14.198771',2,5),(19,16,'2026-02-20 09:28:14.200771',3,5),(20,0,'2026-02-20 09:28:14.204209',4,5),(21,6059.09,'2026-02-20 09:28:14.208221',1,6),(22,196.09,'2026-02-20 09:28:14.211219',2,6),(23,16,'2026-02-20 09:28:14.213219',3,6),(24,0,'2026-02-20 09:28:14.215221',4,6),(25,5139.88,'2026-02-20 09:28:14.220831',1,7),(26,368.85,'2026-02-20 09:28:14.223834',2,7),(27,27,'2026-02-20 09:28:14.225832',3,7),(28,0,'2026-02-20 09:28:14.227833',4,7),(29,5063.12,'2026-02-20 09:28:14.232834',1,8),(30,260.89,'2026-02-20 09:28:14.234830',2,8),(31,22,'2026-02-20 09:28:14.237832',3,8),(32,0,'2026-02-20 09:28:14.240927',4,8),(33,2394.74,'2026-02-20 09:28:14.247127',1,9),(34,132.09,'2026-02-20 09:28:14.249139',2,9),(35,8,'2026-02-20 09:28:14.252829',3,9),(36,0,'2026-02-20 09:28:14.257026',4,9),(37,2585.49,'2026-02-20 09:28:14.262397',1,10),(38,87.45,'2026-02-20 09:28:14.264747',2,10),(39,6,'2026-02-20 09:28:14.267060',3,10),(40,0,'2026-02-20 09:28:14.270695',4,10),(41,4302.78,'2026-02-20 09:28:14.275078',1,11),(42,261.5,'2026-02-20 09:28:14.278077',2,11),(43,22,'2026-02-20 09:28:14.281081',3,11),(44,0,'2026-02-20 09:28:14.283615',4,11),(45,5306.3,'2026-02-20 09:28:14.289681',1,12),(46,251.13,'2026-02-20 09:28:14.292682',2,12),(47,17,'2026-02-20 09:28:14.295681',3,12),(48,0,'2026-02-20 09:28:14.298685',4,12),(49,72,'2026-02-20 09:28:14.309864',5,13),(50,92,'2026-02-20 09:28:14.311859',6,13),(51,683.04,'2026-02-20 09:28:14.314447',2,13),(52,85.51,'2026-02-20 09:28:14.318517',7,13),(53,10395.69,'2026-02-20 09:28:14.321766',1,13),(54,48,'2026-02-20 09:28:14.323766',3,13),(55,2144,'2026-02-20 09:28:14.325900',4,13),(56,78,'2026-02-20 09:28:14.332083',5,14),(57,131,'2026-02-20 09:28:14.334529',6,14),(58,1477.46,'2026-02-20 09:28:14.337673',2,14),(59,324.06,'2026-02-20 09:28:14.341458',7,14),(60,13070.4,'2026-02-20 09:28:14.345063',1,14),(61,87,'2026-02-20 09:28:14.347094',3,14),(62,3560,'2026-02-20 09:28:14.351053',4,14),(63,46,'2026-02-20 09:28:14.357999',5,15),(64,47,'2026-02-20 09:28:14.360999',6,15),(65,498.8,'2026-02-20 09:28:14.364003',2,15),(66,107.56,'2026-02-20 09:28:14.368486',7,15),(67,8153.06,'2026-02-20 09:28:14.374954',1,15),(68,30,'2026-02-20 09:28:14.378096',3,15),(69,1641.24,'2026-02-20 09:28:14.383869',4,15),(70,61,'2026-02-20 09:28:14.390186',5,16),(71,82,'2026-02-20 09:28:14.392514',6,16),(72,1037.2,'2026-02-20 09:28:14.395519',2,16),(73,201.6,'2026-02-20 09:28:14.397979',7,16),(74,9672.27,'2026-02-20 09:28:14.401104',1,16),(75,58,'2026-02-20 09:28:14.404894',3,16),(76,2316.3,'2026-02-20 09:28:14.407893',4,16),(77,70,'2026-02-20 09:28:14.413174',5,17),(78,87,'2026-02-20 09:28:14.417185',6,17),(79,994.07,'2026-02-20 09:28:14.420993',2,17),(80,205.54,'2026-02-20 09:28:14.422996',7,17),(81,10536.81,'2026-02-20 09:28:14.426996',1,17),(82,58,'2026-02-20 09:28:14.428995',3,17),(83,2394.36,'2026-02-20 09:28:14.431997',4,17),(84,98,'2026-02-20 09:28:14.438207',5,18),(85,131,'2026-02-20 09:28:14.441209',6,18),(86,1210.73,'2026-02-20 09:28:14.443211',2,18),(87,222.17,'2026-02-20 09:28:14.446210',7,18),(88,11690.13,'2026-02-20 09:28:14.449206',1,18),(89,72,'2026-02-20 09:28:14.451206',3,18),(90,2852.4,'2026-02-20 09:28:14.454371',4,18),(91,58,'2026-02-20 09:28:14.460372',5,19),(92,103,'2026-02-20 09:28:14.462881',6,19),(93,877.89,'2026-02-20 09:28:14.465898',2,19),(94,183.46,'2026-02-20 09:28:14.467909',7,19),(95,10810.53,'2026-02-20 09:28:14.472091',1,19),(96,56,'2026-02-20 09:28:14.474091',3,19),(97,2261.28,'2026-02-20 09:28:14.476090',4,19),(98,110,'2026-02-20 09:28:14.482969',5,20),(99,138,'2026-02-20 09:28:14.484983',6,20),(100,899.46,'2026-02-20 09:28:14.488265',2,20),(101,52.81,'2026-02-20 09:28:14.490338',7,20),(102,12797.51,'2026-02-20 09:28:14.493278',1,20),(103,64,'2026-02-20 09:28:14.495280',3,20),(104,3171.49,'2026-02-20 09:28:14.497279',4,20),(105,70,'2026-02-20 09:28:14.503250',5,21),(106,79,'2026-02-20 09:28:14.505353',6,21),(107,653.83,'2026-02-20 09:28:14.507354',2,21),(108,106.06,'2026-02-20 09:28:14.509354',7,21),(109,11145.48,'2026-02-20 09:28:14.511355',1,21),(110,47,'2026-02-20 09:28:14.513355',3,21),(111,2217.52,'2026-02-20 09:28:14.517355',4,21),(112,22,'2026-02-20 09:28:14.523401',5,22),(113,24,'2026-02-20 09:28:14.525400',6,22),(114,244.05,'2026-02-20 09:28:14.527403',2,22),(115,86,'2026-02-20 09:28:14.529398',7,22),(116,2310.38,'2026-02-20 09:28:14.532403',1,22),(117,13,'2026-02-20 09:28:14.535405',3,22),(118,609.39,'2026-02-20 09:28:14.538581',4,22),(119,28,'2026-02-20 09:28:14.543580',5,23),(120,40,'2026-02-20 09:28:14.545582',6,23),(121,176.01,'2026-02-20 09:28:14.548580',2,23),(122,11.38,'2026-02-20 09:28:14.551833',7,23),(123,4107.92,'2026-02-20 09:28:14.554343',1,23),(124,14,'2026-02-20 09:28:14.556398',3,23),(125,908.79,'2026-02-20 09:28:14.558399',4,23),(126,87,'2026-02-20 09:28:14.563402',5,24),(127,125,'2026-02-20 09:28:14.565396',6,24),(128,898.64,'2026-02-20 09:28:14.568404',2,24),(129,192.75,'2026-02-20 09:28:14.571885',7,24),(130,11391.48,'2026-02-20 09:28:14.573410',1,24),(131,55,'2026-02-20 09:28:14.575425',3,24),(132,2486.95,'2026-02-20 09:28:14.577427',4,24),(133,11,'2026-02-20 09:28:14.582305',5,25),(134,15,'2026-02-20 09:28:14.585332',6,25),(135,82.65,'2026-02-20 09:28:14.588327',2,25),(136,28.76,'2026-02-20 09:28:14.590355',7,25),(137,1288.78,'2026-02-20 09:28:14.592354',1,25),(138,4,'2026-02-20 09:28:14.595360',3,25),(139,295.48,'2026-02-20 09:28:14.597359',4,25),(140,3.8,'2026-02-20 09:28:14.607046',8,26),(141,4.5,'2026-02-20 09:28:14.610045',9,26),(142,34,'2026-02-20 09:28:14.613046',10,26),(143,34,'2026-02-20 09:28:14.615048',11,26),(144,22,'2026-02-20 09:28:14.618049',12,26),(145,1.22,'2026-02-20 09:28:14.623682',8,27),(146,4,'2026-02-20 09:28:14.625680',9,27),(147,3,'2026-02-20 09:28:14.627681',10,27),(148,34,'2026-02-20 09:28:14.630681',11,27),(149,120,'2026-02-20 09:28:14.632681',12,27),(150,1.72,'2026-02-20 09:28:14.639273',8,28),(151,4.35,'2026-02-20 09:28:14.641273',9,28),(152,41.2,'2026-02-20 09:28:14.644284',10,28),(153,122,'2026-02-20 09:28:14.647284',12,28),(154,87.5,'2026-02-20 09:28:14.649283',13,28),(155,72.4,'2026-02-20 09:28:14.653972',14,29),(156,55,'2026-02-20 09:28:14.657211',16,29),(157,1.72,'2026-02-20 09:28:14.661922',8,30),(158,4.35,'2026-02-20 09:28:14.664605',9,30),(159,41.2,'2026-02-20 09:28:14.666621',10,30),(160,1780,'2026-02-20 09:28:14.668702',12,30),(161,87.5,'2026-02-20 09:28:14.671004',13,30),(162,72.4,'2026-02-20 09:28:14.672518',14,30),(163,52,'2026-02-20 09:28:14.677737',16,30),(164,72.2,'2026-02-20 09:28:14.683281',14,31),(165,44,'2026-02-20 09:28:14.686070',16,31),(166,72.8,'2026-02-20 09:28:14.691081',14,32),(167,63.5,'2026-02-20 09:28:14.693704',16,32),(168,72,'2026-02-20 09:28:14.698712',14,33),(169,63.4,'2026-02-20 09:28:14.700712',16,33),(170,72.2,'2026-02-20 09:28:14.706851',14,34),(171,64,'2026-02-20 09:28:14.709853',16,34),(172,71.6,'2026-02-20 09:28:14.713854',14,35),(173,59,'2026-02-20 09:28:14.716857',16,35),(174,72,'2026-02-20 09:28:14.721705',14,36),(175,60,'2026-02-20 09:28:14.724706',16,36),(176,1.72,'2026-02-20 09:28:14.729707',8,37),(177,4.25,'2026-02-20 09:28:14.731707',9,37),(178,41,'2026-02-20 09:28:14.733703',10,37),(179,122,'2026-02-20 09:28:14.737241',12,37),(180,87.4,'2026-02-20 09:28:14.739246',13,37);
/*!40000 ALTER TABLE `main_performancemetric` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_performancemetrictype`
--

DROP TABLE IF EXISTS `main_performancemetrictype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_performancemetrictype` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `code` varchar(50) NOT NULL,
  `label` varchar(120) NOT NULL,
  `unit` varchar(30) NOT NULL,
  `category` varchar(30) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_performancemetrictype`
--

LOCK TABLES `main_performancemetrictype` WRITE;
/*!40000 ALTER TABLE `main_performancemetrictype` DISABLE KEYS */;
INSERT INTO `main_performancemetrictype` VALUES (1,'total_distance','Totale afstand','m','load',1,'2026-02-20 09:28:14.107273'),(2,'hsd','High-speed distance','m','load',1,'2026-02-20 09:28:14.109272'),(3,'sprints','Sprints','count','load',1,'2026-02-20 09:28:14.111467'),(4,'load','Belasting','au','load',1,'2026-02-20 09:28:14.114576'),(5,'accelerations','Acceleraties','count','load',1,'2026-02-20 09:28:14.116105'),(6,'decelerations','Deceleraties','count','load',1,'2026-02-20 09:28:14.117123'),(7,'his','High intensity sprint distance','m','load',1,'2026-02-20 09:28:14.119849'),(8,'sprint_10','10m sprint','s','test',1,'2026-02-20 09:28:14.122048'),(9,'sprint_30','30m sprint','s','test',1,'2026-02-20 09:28:14.124218'),(10,'cmj','CMJ','cm','test',1,'2026-02-20 09:28:14.125225'),(11,'squat_jump','Squat jump','cm','test',1,'2026-02-20 09:28:14.126230'),(12,'isrt','ISRT','m','test',1,'2026-02-20 09:28:14.127542'),(13,'submax','Submax','pct','test',1,'2026-02-20 09:28:14.129796'),(14,'curr_weight','Gewicht','kg','test',1,'2026-02-20 09:28:14.131806'),(15,'length','Lengte','cm','test',1,'2026-02-20 09:28:14.134818'),(16,'sum_skinfolds','Som huidplooien','mm','test',1,'2026-02-20 09:28:14.137446');
/*!40000 ALTER TABLE `main_performancemetrictype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_performancesession`
--

DROP TABLE IF EXISTS `main_performancesession`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_performancesession` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `session_date` date NOT NULL,
  `week` int unsigned DEFAULT NULL,
  `source_legacy_table` varchar(50) DEFAULT NULL,
  `source_legacy_id` int unsigned DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `player_id` bigint NOT NULL,
  `session_kind_ref_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_perf_session_per_source` (`player_id`,`session_kind_ref_id`,`session_date`,`source_legacy_table`,`source_legacy_id`),
  KEY `main_perfor_player__4b4079_idx` (`player_id`,`session_date`),
  KEY `main_perfor_session_f2abd8_idx` (`session_kind_ref_id`,`session_date`),
  CONSTRAINT `main_performancesess_session_kind_ref_id_7495e701_fk_main_perf` FOREIGN KEY (`session_kind_ref_id`) REFERENCES `main_performancesessionkind` (`id`),
  CONSTRAINT `main_performancesession_player_id_05976bf3_fk_main_player_id` FOREIGN KEY (`player_id`) REFERENCES `main_player` (`id`),
  CONSTRAINT `main_performancesession_chk_1` CHECK ((`week` >= 0)),
  CONSTRAINT `main_performancesession_chk_2` CHECK ((`source_legacy_id` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_performancesession`
--

LOCK TABLES `main_performancesession` WRITE;
/*!40000 ALTER TABLE `main_performancesession` DISABLE KEYS */;
INSERT INTO `main_performancesession` VALUES (1,'2025-11-10',46,'main_trainingdata',274,'2026-02-20 09:28:14.145963','2026-02-20 09:28:14.145963',2,3),(2,'2025-11-10',46,'main_trainingdata',275,'2026-02-20 09:28:14.159466','2026-02-20 09:28:14.159466',6,3),(3,'2025-11-10',46,'main_trainingdata',276,'2026-02-20 09:28:14.171926','2026-02-20 09:28:14.171926',3,3),(4,'2025-11-10',46,'main_trainingdata',277,'2026-02-20 09:28:14.182433','2026-02-20 09:28:14.182433',4,3),(5,'2025-11-10',46,'main_trainingdata',278,'2026-02-20 09:28:14.194772','2026-02-20 09:28:14.194772',19,3),(6,'2025-11-10',46,'main_trainingdata',279,'2026-02-20 09:28:14.206219','2026-02-20 09:28:14.206219',9,3),(7,'2025-11-10',46,'main_trainingdata',280,'2026-02-20 09:28:14.218219','2026-02-20 09:28:14.218219',1,3),(8,'2025-11-10',46,'main_trainingdata',281,'2026-02-20 09:28:14.229834','2026-02-20 09:28:14.229834',11,3),(9,'2025-11-10',46,'main_trainingdata',282,'2026-02-20 09:28:14.243938','2026-02-20 09:28:14.243938',27,3),(10,'2025-11-10',46,'main_trainingdata',283,'2026-02-20 09:28:14.261045','2026-02-20 09:28:14.261045',24,3),(11,'2025-11-10',46,'main_trainingdata',284,'2026-02-20 09:28:14.273076','2026-02-20 09:28:14.273076',23,3),(12,'2025-11-10',46,'main_trainingdata',285,'2026-02-20 09:28:14.286599','2026-02-20 09:28:14.286599',21,3),(13,'2025-11-15',46,'main_wedstrijddata',52,'2026-02-20 09:28:14.306861','2026-02-20 09:28:14.306861',2,2),(14,'2025-11-15',46,'main_wedstrijddata',53,'2026-02-20 09:28:14.329072','2026-02-20 09:28:14.329072',14,2),(15,'2025-11-15',46,'main_wedstrijddata',54,'2026-02-20 09:28:14.354907','2026-02-20 09:28:14.354907',4,2),(16,'2025-11-15',46,'main_wedstrijddata',55,'2026-02-20 09:28:14.387188','2026-02-20 09:28:14.387188',19,2),(17,'2025-11-15',46,'main_wedstrijddata',56,'2026-02-20 09:28:14.410893','2026-02-20 09:28:14.410893',9,2),(18,'2025-11-15',46,'main_wedstrijddata',57,'2026-02-20 09:28:14.434253','2026-02-20 09:28:14.434253',1,2),(19,'2025-11-15',46,'main_wedstrijddata',58,'2026-02-20 09:28:14.457372','2026-02-20 09:28:14.457372',11,2),(20,'2025-11-15',46,'main_wedstrijddata',59,'2026-02-20 09:28:14.479438','2026-02-20 09:28:14.479438',20,2),(21,'2025-11-15',46,'main_wedstrijddata',60,'2026-02-20 09:28:14.499783','2026-02-20 09:28:14.499783',26,2),(22,'2025-11-15',46,'main_wedstrijddata',61,'2026-02-20 09:28:14.521398','2026-02-20 09:28:14.521398',22,2),(23,'2025-11-15',46,'main_wedstrijddata',62,'2026-02-20 09:28:14.541580','2026-02-20 09:28:14.541580',24,2),(24,'2025-11-15',46,'main_wedstrijddata',63,'2026-02-20 09:28:14.560399','2026-02-20 09:28:14.560399',21,2),(25,'2025-11-15',46,'main_wedstrijddata',64,'2026-02-20 09:28:14.579423','2026-02-20 09:28:14.579423',25,2),(26,'2025-12-10',NULL,'main_playertest',1,'2026-02-20 09:28:14.604046','2026-02-20 09:28:14.604046',1,1),(27,'2025-12-10',NULL,'main_playertest',2,'2026-02-20 09:28:14.620685','2026-02-20 09:28:14.620685',1,1),(28,'2025-12-10',NULL,'main_playertest',3,'2026-02-20 09:28:14.635679','2026-02-20 09:28:14.635679',21,1),(29,'2025-12-10',NULL,'main_playertest',4,'2026-02-20 09:28:14.651283','2026-02-20 09:28:14.651283',21,1),(30,'2025-12-10',NULL,'main_playertest',5,'2026-02-20 09:28:14.659213','2026-02-20 09:28:14.659213',21,1),(31,'2025-12-10',NULL,'main_playertest',6,'2026-02-20 09:28:14.679750','2026-02-20 09:28:14.679750',21,1),(32,'2025-12-10',NULL,'main_playertest',7,'2026-02-20 09:28:14.689084','2026-02-20 09:28:14.689084',21,1),(33,'2025-12-10',NULL,'main_playertest',8,'2026-02-20 09:28:14.696712','2026-02-20 09:28:14.696712',21,1),(34,'2025-12-10',NULL,'main_playertest',9,'2026-02-20 09:28:14.703713','2026-02-20 09:28:14.703713',21,1),(35,'2025-12-09',NULL,'main_playertest',10,'2026-02-20 09:28:14.711854','2026-02-20 09:28:14.711854',21,1),(36,'2025-12-10',NULL,'main_playertest',11,'2026-02-20 09:28:14.719424','2026-02-20 09:28:14.719424',21,1),(37,'2025-12-11',NULL,'main_playertest',12,'2026-02-20 09:28:14.726702','2026-02-20 09:28:14.727702',12,1);
/*!40000 ALTER TABLE `main_performancesession` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_performancesessionkind`
--

DROP TABLE IF EXISTS `main_performancesessionkind`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_performancesessionkind` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `code` varchar(20) NOT NULL,
  `label` varchar(60) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_performancesessionkind`
--

LOCK TABLES `main_performancesessionkind` WRITE;
/*!40000 ALTER TABLE `main_performancesessionkind` DISABLE KEYS */;
INSERT INTO `main_performancesessionkind` VALUES (1,'test','Test',1,'2026-03-03 12:15:20.566344'),(2,'match','Wedstrijd',1,'2026-03-03 12:15:20.586455'),(3,'training','Training',1,'2026-03-03 12:15:20.601055');
/*!40000 ALTER TABLE `main_performancesessionkind` ENABLE KEYS */;
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
  `image` varchar(100) DEFAULT NULL,
  `position_ref_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `main_player_position_ref_id_5d3aeeee_fk_main_playerposition_id` (`position_ref_id`),
  CONSTRAINT `main_player_position_ref_id_5d3aeeee_fk_main_playerposition_id` FOREIGN KEY (`position_ref_id`) REFERENCES `main_playerposition` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=84 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_player`
--

LOCK TABLES `main_player` WRITE;
/*!40000 ALTER TABLE `main_player` DISABLE KEYS */;
INSERT INTO `main_player` VALUES (1,'Nick Doodeman','player_images/463449_nick_doodeman_20241202233119.jpg',3),(2,'Raffael Behounek','player_images/552060_raffael_behounek_20241202131159.jpg',6),(3,'Justin Hoogma','player_images/432766.png',6),(4,'Jari Schuurman','player_images/268333.jpg',4),(5,'Niels van Berkel','player_images/436789.jpg',7),(6,'Jens Mathijsen','player_images/1099155.jpg',6),(7,'Devin Haen','player_images/704771-1723629105.webp',1),(8,'Wouter van der Steen','player_images/159896-1658911757.webp',NULL),(9,'Siegert Baartmans','player_images/images_6.jpg',2),(10,'Thomas Verheydt','player_images/images_5.jpg',1),(11,'Nathan Tjoe-A-On','player_images/images_4.jpg',7),(12,'Max de Waal','player_images/438732.jpg',5),(13,'Amine Lachkar','player_images/11637722_amine_lachkar_20241202221159_XTR8rXd.jpg',5),(14,'Uriël van Aalst','player_images/956285.png',4),(15,'Junior Poortvliet','player_images/junior-poortvliet-heeft-zijn-eerste-contract-getekend-bij-willem-ii.webp',6),(16,'Per van Loon','player_images/694201.jpg',3),(17,'Thomas Didilion Hödl','player_images/302013_thomas_didillon_20241202012645.jpg',NULL),(18,'Karst de Leeuw','player_images/31._Karst_de_Leeuw.png.webp',NULL),(19,'Emilio Kehrer','player_images/396410.jpg',3),(20,'Gijs Besselink','player_images/655248.png',5),(21,'Alessandro Ciranni','player_images/295662.jpg',7),(22,'Armin Culum','player_images/56245-Fotoburo-Toin-Damen.jpg',3),(23,'Samuel Bamba','player_images/424811.jpg',3),(24,'Anass Zarrouk','player_images/55994-Geert-van-Erven.jpg',4),(25,'Mounir el Allouchi','player_images/267781.jpg',4),(26,'Finn Stams','player_images/531195.jpg',6),(27,'Pieter van Maarschalkerwaard','player_images/1797867.png',4),(28,'Boet van der Linden','player_images/2757282_boet_van_der_linden__20250901001022.png',NULL);
/*!40000 ALTER TABLE `main_player` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_playermonitoringprofile`
--

DROP TABLE IF EXISTS `main_playermonitoringprofile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_playermonitoringprofile` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `prev_weight` double DEFAULT NULL,
  `curr_weight` double DEFAULT NULL,
  `sum_skinfolds` double DEFAULT NULL,
  `fat_perc` double DEFAULT NULL,
  `nutrition_focus` longtext,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `player_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `player_id` (`player_id`),
  CONSTRAINT `main_playermonitorin_player_id_cf470ad0_fk_main_play` FOREIGN KEY (`player_id`) REFERENCES `main_player` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_playermonitoringprofile`
--

LOCK TABLES `main_playermonitoringprofile` WRITE;
/*!40000 ALTER TABLE `main_playermonitoringprofile` DISABLE KEYS */;
INSERT INTO `main_playermonitoringprofile` VALUES (1,NULL,NULL,NULL,NULL,'Eiwitten hoger','2026-02-25 08:59:52.187271','2026-02-25 08:59:52.187271',4),(2,NULL,NULL,NULL,NULL,'Hij moet vooral aankomen','2026-02-25 08:59:52.194636','2026-02-25 08:59:52.194636',5),(3,NULL,NULL,NULL,NULL,'Moet meer ruimte maken om te eten','2026-02-25 08:59:52.201896','2026-02-25 08:59:52.201896',6),(4,NULL,65,70,NULL,'','2026-02-25 08:59:52.205510','2026-02-25 08:59:52.205510',16),(5,73,80,65,11,'','2026-02-25 08:59:52.206521','2026-02-25 08:59:52.206521',21);
/*!40000 ALTER TABLE `main_playermonitoringprofile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_playerposition`
--

DROP TABLE IF EXISTS `main_playerposition`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_playerposition` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_playerposition`
--

LOCK TABLES `main_playerposition` WRITE;
/*!40000 ALTER TABLE `main_playerposition` DISABLE KEYS */;
INSERT INTO `main_playerposition` VALUES (1,'Spits',1,'2026-02-26 07:15:14.468060'),(2,'Targetman',1,'2026-02-26 07:15:14.468060'),(3,'Buitenspeler',1,'2026-02-26 07:15:14.476571'),(4,'Dynamische middenvelder',1,'2026-02-26 07:15:14.478549'),(5,'Controlerende middenvelder',1,'2026-02-26 07:15:14.479741'),(6,'Centrale verdediger',1,'2026-02-26 07:15:14.481752'),(7,'Vleugelverdediger',1,'2026-02-26 07:15:14.481752');
/*!40000 ALTER TABLE `main_playerposition` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_playerspeedtest`
--

DROP TABLE IF EXISTS `main_playerspeedtest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_playerspeedtest` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `test_date` date NOT NULL,
  `mss_kmh` decimal(5,2) NOT NULL,
  `mas_kmh` decimal(5,2) NOT NULL,
  `notes` varchar(255) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `player_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_speed_test_player_date` (`player_id`,`test_date`),
  KEY `main_player_player__54dc7a_idx` (`player_id`,`test_date`),
  KEY `main_player_test_da_19ee67_idx` (`test_date`),
  CONSTRAINT `main_playerspeedtest_player_id_91e42287_fk_main_player_id` FOREIGN KEY (`player_id`) REFERENCES `main_player` (`id`),
  CONSTRAINT `ck_speedtest_mas_pos` CHECK ((`mas_kmh` > 0)),
  CONSTRAINT `ck_speedtest_mss_pos` CHECK ((`mss_kmh` > 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_playerspeedtest`
--

LOCK TABLES `main_playerspeedtest` WRITE;
/*!40000 ALTER TABLE `main_playerspeedtest` DISABLE KEYS */;
/*!40000 ALTER TABLE `main_playerspeedtest` ENABLE KEYS */;
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
-- Table structure for table `main_programmaduurunit`
--

DROP TABLE IF EXISTS `main_programmaduurunit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_programmaduurunit` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_programmaduurunit`
--

LOCK TABLES `main_programmaduurunit` WRITE;
/*!40000 ALTER TABLE `main_programmaduurunit` DISABLE KEYS */;
/*!40000 ALTER TABLE `main_programmaduurunit` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_programmafrequentie`
--

DROP TABLE IF EXISTS `main_programmafrequentie`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_programmafrequentie` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_programmafrequentie`
--

LOCK TABLES `main_programmafrequentie` WRITE;
/*!40000 ALTER TABLE `main_programmafrequentie` DISABLE KEYS */;
/*!40000 ALTER TABLE `main_programmafrequentie` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_programmaoefening`
--

DROP TABLE IF EXISTS `main_programmaoefening`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_programmaoefening` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `opmerkingen` longtext,
  `programma_id` bigint NOT NULL,
  `frequentie_ref_id` bigint DEFAULT NULL,
  `rpe_value` smallint unsigned DEFAULT NULL,
  `duur_text_override` varchar(50) DEFAULT NULL,
  `duur_unit_ref_id` bigint DEFAULT NULL,
  `duur_value` decimal(8,2) DEFAULT NULL,
  `naam_ref_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `main_programmaoefeni_programma_id_5c7695cf_fk_main_prog` (`programma_id`),
  KEY `main_programmaoefening_frequentie_ref_id_3565796c` (`frequentie_ref_id`),
  KEY `main_programmaoefening_duur_unit_ref_id_78ab4bc6` (`duur_unit_ref_id`),
  KEY `main_programmaoefening_naam_ref_id_a988b491` (`naam_ref_id`),
  CONSTRAINT `main_programmaoefeni_duur_unit_ref_id_78ab4bc6_fk_main_prog` FOREIGN KEY (`duur_unit_ref_id`) REFERENCES `main_programmaduurunit` (`id`),
  CONSTRAINT `main_programmaoefeni_frequentie_ref_id_3565796c_fk_main_prog` FOREIGN KEY (`frequentie_ref_id`) REFERENCES `main_programmafrequentie` (`id`),
  CONSTRAINT `main_programmaoefeni_naam_ref_id_a988b491_fk_main_prog` FOREIGN KEY (`naam_ref_id`) REFERENCES `main_programmaoefeningnaam` (`id`),
  CONSTRAINT `main_programmaoefeni_programma_id_5c7695cf_fk_main_prog` FOREIGN KEY (`programma_id`) REFERENCES `main_programma` (`id`),
  CONSTRAINT `main_programmaoefening_chk_1` CHECK ((`rpe_value` >= 0))
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
-- Table structure for table `main_programmaoefeningnaam`
--

DROP TABLE IF EXISTS `main_programmaoefeningnaam`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_programmaoefeningnaam` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_programmaoefeningnaam`
--

LOCK TABLES `main_programmaoefeningnaam` WRITE;
/*!40000 ALTER TABLE `main_programmaoefeningnaam` DISABLE KEYS */;
/*!40000 ALTER TABLE `main_programmaoefeningnaam` ENABLE KEYS */;
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
  `rpe` int NOT NULL,
  `session_load` int DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `player_id` bigint NOT NULL,
  `training_type_ref_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_rpe_player_date` (`player_id`,`date`),
  KEY `main_rpeent_date_fbec02_idx` (`date`,`player_id`),
  KEY `main_rpeentry_training_type_ref_id_f1f73fd0` (`training_type_ref_id`),
  CONSTRAINT `main_rpeentry_player_id_d9a3e014_fk_main_player_id` FOREIGN KEY (`player_id`) REFERENCES `main_player` (`id`),
  CONSTRAINT `main_rpeentry_training_type_ref_id_f1f73fd0_fk_main_rpet` FOREIGN KEY (`training_type_ref_id`) REFERENCES `main_rpetrainingtype` (`id`),
  CONSTRAINT `ck_rpe_between_1_10` CHECK (((`rpe` >= 1) and (`rpe` <= 10))),
  CONSTRAINT `ck_rpe_session_load_nonneg` CHECK (((`session_load` is null) or (`session_load` >= 0)))
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_rpeentry`
--

LOCK TABLES `main_rpeentry` WRITE;
/*!40000 ALTER TABLE `main_rpeentry` DISABLE KEYS */;
INSERT INTO `main_rpeentry` VALUES (1,'2025-11-22',10,NULL,'2025-11-22 20:02:06.259262',21,1),(2,'2025-12-04',10,NULL,'2025-12-05 10:52:38.709562',21,1),(3,'2025-12-05',1,NULL,'2025-12-05 11:15:46.050787',21,1),(4,'2025-12-18',8,NULL,'2025-12-18 06:27:46.109584',21,1),(5,'2026-01-23',10,NULL,'2026-02-23 11:06:48.443595',21,1),(6,'2026-02-21',9,NULL,'2026-02-23 11:15:31.928559',21,2),(7,'2026-02-23',9,NULL,'2026-02-23 11:15:48.725871',13,1);
/*!40000 ALTER TABLE `main_rpeentry` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_rpetrainingtype`
--

DROP TABLE IF EXISTS `main_rpetrainingtype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_rpetrainingtype` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_rpetrainingtype`
--

LOCK TABLES `main_rpetrainingtype` WRITE;
/*!40000 ALTER TABLE `main_rpetrainingtype` DISABLE KEYS */;
INSERT INTO `main_rpetrainingtype` VALUES (1,'Training',1,'2026-02-23 11:06:02.030365'),(2,'Wedstrijd',1,'2026-02-23 11:06:02.030365'),(3,'Individueel',1,'2026-02-23 11:06:02.030365');
/*!40000 ALTER TABLE `main_rpetrainingtype` ENABLE KEYS */;
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
  `role_ref_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `main_staff_role_ref_id_d2233a04_fk_main_staffrole_id` (`role_ref_id`),
  CONSTRAINT `main_staff_role_ref_id_d2233a04_fk_main_staffrole_id` FOREIGN KEY (`role_ref_id`) REFERENCES `main_staffrole` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_staff`
--

LOCK TABLES `main_staff` WRITE;
/*!40000 ALTER TABLE `main_staff` DISABLE KEYS */;
INSERT INTO `main_staff` VALUES (1,'John Stegeman',1),(2,'Freek Heerkens',2),(3,'Merijn Goris',3),(4,'Sam Strijbosch',4),(5,'Kristof Aalbrecht',5),(6,'Pascal Diender',5),(7,'Peter den Otter',6),(8,'Ilse Driessen',7),(9,'Henry van Amelsfoort',8),(10,'Nils Thörner',9),(11,'Jos de Kruijf',10),(12,'Martin van den Heuvel',11),(13,'Adrie Koster',12),(14,'Steven Aptroot',13),(15,'Pieter Vioen',14),(16,'Sep Bierkens',15),(17,'Michel de Gruijter',16),(18,'Jasper de Langen',15),(19,'Jos van Nieuwstadt',17);
/*!40000 ALTER TABLE `main_staff` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_staffrole`
--

DROP TABLE IF EXISTS `main_staffrole`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_staffrole` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_staffrole`
--

LOCK TABLES `main_staffrole` WRITE;
/*!40000 ALTER TABLE `main_staffrole` DISABLE KEYS */;
INSERT INTO `main_staffrole` VALUES (1,'Hoofdtrainer',1,'2026-02-26 07:15:14.491010'),(2,'Technisch directeur',1,'2026-02-26 07:15:14.491010'),(3,'Algemeen directeur',1,'2026-02-26 07:15:14.506653'),(4,'Recruitment coördinator',1,'2026-02-26 07:15:14.508657'),(5,'Assistent trainer',1,'2026-02-26 07:15:14.508657'),(6,'Keeperstrainer',1,'2026-02-26 07:15:14.508657'),(7,'Kok',1,'2026-02-26 07:15:14.508657'),(8,'Verzorger',1,'2026-02-26 07:15:14.508657'),(9,'Head of Performance',1,'2026-02-26 07:15:14.517918'),(10,'Commercieel manager',1,'2026-02-26 07:15:14.519929'),(11,'Financieel directeur',1,'2026-02-26 07:15:14.524246'),(12,'Technisch adviseur',1,'2026-02-26 07:15:14.526261'),(13,'Hoofd scouting',1,'2026-02-26 07:15:14.526261'),(14,'Clubarts',1,'2026-02-26 07:15:14.528842'),(15,'Fysiotherapeut',1,'2026-02-26 07:15:14.530853'),(16,'Hoofd medisch',1,'2026-02-26 07:15:14.532912'),(17,'Teammanager',1,'2026-02-26 07:15:14.532912');
/*!40000 ALTER TABLE `main_staffrole` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_team`
--

LOCK TABLES `main_team` WRITE;
/*!40000 ALTER TABLE `main_team` DISABLE KEYS */;
INSERT INTO `main_team` VALUES (1,'JONG_PSV','Jong PSV',1,'2026-02-23 10:21:02.760709'),(2,'WILLEM_II','Willem II',1,'2026-02-23 10:21:02.764242'),(3,'TOP_OSS','TOP Oss',1,'2026-02-23 10:21:02.764242'),(4,'FC_EMMEN','FC Emmen',1,'2026-02-23 10:21:02.770741'),(5,'VVV_VENLO','VVV-Venlo',1,'2026-02-23 10:21:02.772814'),(6,'FC_DEN_BOSCH','FC Den Bosch',1,'2026-02-23 10:21:02.774829'),(7,'FC_DORDRECHT','FC Dordrecht',1,'2026-02-23 10:21:02.776844'),(8,'SC_CAMBUUR','SC Cambuur',1,'2026-02-23 10:21:02.780374'),(9,'SPARTA_ROTTERDAM','Sparta Rotterdam',1,'2026-02-23 10:21:02.781943'),(10,'HELMOND_SPORT','Helmond Sport',1,'2026-02-23 10:21:02.781943'),(11,'ADO_DEN_HAAG','ADO Den Haag',1,'2026-02-23 10:21:02.781943'),(12,'JONG_AJAX','Jong Ajax',1,'2026-02-23 10:21:02.781943'),(13,'RKC_WAALWIJK','RKC Waalwijk',1,'2026-02-23 10:21:02.781943'),(14,'JONG_FC_UTRECHT','Jong FC Utrecht',1,'2026-02-23 10:21:02.790935'),(15,'VITESSE','Vitesse',1,'2026-02-23 10:21:02.792986'),(16,'MVV','MVV',1,'2026-02-23 10:21:02.798045'),(17,'DE_GRAAFSCHAP','De Graafschap',1,'2026-02-23 10:21:02.800932'),(18,'RODA_JC','Roda JC',1,'2026-02-23 10:21:02.800932'),(19,'ALMERE_CITY_FC','Almere City FC',1,'2026-02-23 10:21:02.800932'),(20,'JONG_AZ','Jong AZ',1,'2026-02-23 10:21:02.800932');
/*!40000 ALTER TABLE `main_team` ENABLE KEYS */;
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
  CONSTRAINT `main_weightentry_player_id_326dccd1_fk_main_player_id` FOREIGN KEY (`player_id`) REFERENCES `main_player` (`id`),
  CONSTRAINT `ck_weight_pos` CHECK ((`weight` > 0.0e0))
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
  UNIQUE KEY `uniq_wellness_player_date` (`player_id`,`date`),
  KEY `main_wellne_date_cc439a_idx` (`date`,`player_id`),
  CONSTRAINT `main_wellnessentry_player_id_fk` FOREIGN KEY (`player_id`) REFERENCES `main_player` (`id`),
  CONSTRAINT `ck_well_fit_1_5` CHECK (((`fitness` is null) or ((`fitness` >= 1) and (`fitness` <= 5)))),
  CONSTRAINT `ck_well_mood_1_5` CHECK (((`mood` is null) or ((`mood` >= 1) and (`mood` <= 5)))),
  CONSTRAINT `ck_well_sleep_1_5` CHECK (((`sleep` is null) or ((`sleep` >= 1) and (`sleep` <= 5)))),
  CONSTRAINT `ck_well_sore_1_5` CHECK (((`soreness` is null) or ((`soreness` >= 1) and (`soreness` <= 5))))
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
-- Table structure for table `main_youthguestprofile`
--

DROP TABLE IF EXISTS `main_youthguestprofile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_youthguestprofile` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `team_ref_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_youthguest_profile_name_team_ref` (`name`,`team_ref_id`),
  KEY `main_youthguestprofile_team_ref_id_89b5a777` (`team_ref_id`),
  CONSTRAINT `main_youthguestprofi_team_ref_id_89b5a777_fk_main_yout` FOREIGN KEY (`team_ref_id`) REFERENCES `main_youthguestteam` (`id`)
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
-- Table structure for table `main_youthguestteam`
--

DROP TABLE IF EXISTS `main_youthguestteam`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_youthguestteam` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_youthguestteam`
--

LOCK TABLES `main_youthguestteam` WRITE;
/*!40000 ALTER TABLE `main_youthguestteam` DISABLE KEYS */;
/*!40000 ALTER TABLE `main_youthguestteam` ENABLE KEYS */;
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
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-03-11 14:11:50
