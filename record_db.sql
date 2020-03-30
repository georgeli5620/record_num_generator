-- MySQL dump 10.13  Distrib 8.0.19, for Win64 (x86_64)
--
-- Host: localhost    Database: record
-- ------------------------------------------------------
-- Server version	8.0.19

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `business_series`
--

DROP TABLE IF EXISTS `business_series`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `business_series` (
  `title` varchar(255) NOT NULL,
  `business_series_index` int NOT NULL,
  PRIMARY KEY (`business_series_index`),
  UNIQUE KEY `title` (`title`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `business_series`
--

LOCK TABLES `business_series` WRITE;
/*!40000 ALTER TABLE `business_series` DISABLE KEYS */;
INSERT INTO `business_series` VALUES ('Corporate',10),('Engineering',40),('Export Controls',20),('IT',60),('Office General',90),('Operations',50),('Project Controls',30),('QMS',70),('unassigned',80);
/*!40000 ALTER TABLE `business_series` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `business_units`
--

DROP TABLE IF EXISTS `business_units`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `business_units` (
  `title` varchar(255) NOT NULL,
  `summary` varchar(255) DEFAULT NULL,
  `business_code` int NOT NULL,
  `business_series_index` int NOT NULL,
  PRIMARY KEY (`business_code`),
  KEY `business_series_index` (`business_series_index`),
  CONSTRAINT `business_units_ibfk_1` FOREIGN KEY (`business_series_index`) REFERENCES `business_series` (`business_series_index`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `business_units`
--

LOCK TABLES `business_units` WRITE;
/*!40000 ALTER TABLE `business_units` DISABLE KEYS */;
INSERT INTO `business_units` VALUES ('Corporate Management','NA',10,10),('Training','NA',11,10),('Administration','NA',12,10),('Human Resources','NA',13,10),('Legal','NA',14,10),('TalentAcquisition & Management','NA',15,10),('Export Control Management','NA',20,20),('Training','NA',21,20),('Permits','NA',22,20),('Audits','NA',23,20),('Agreements','NA',24,20),('Regulatory','NA',25,20),('Project Management','NA',30,30),('Training','NA',31,30),('Planning','NA',32,30),('Cost Control','NA',33,30),('Cost Accounting','NA',34,30),('Engineering Management','NA',40,40),('Analysis and Mechanical Integrity','NA',41,40),('Design, Verification and Validation','NA',42,40),('Materials and Manufacturing','NA',43,40),('Product Definition Engineering','NA',44,40),('Software and Embedded Systems','NA',45,40),('Operations Management','NA',50,50),('Training','NA',51,50),('QMS','NA',52,50),('Tiers','NA',53,50),('Audits','NA',54,50),('IT Management','NA',60,60),('Training','NA',61,60),('Applications','NA',62,60),('Licenses','NA',63,60),('Tools','NA',64,60),('QMS Management','NA',70,70),('Training','NA',71,70),('Documents','NA',72,70),('Audits','NA',73,70),('CAPA','NA',74,70),('','NA',80,80),('General Management','NA',90,90),('Training','NA',91,90),('Administration','NA',92,90),('Meetings','NA',93,90);
/*!40000 ALTER TABLE `business_units` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `document_files`
--

DROP TABLE IF EXISTS `document_files`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `document_files` (
  `title` varchar(255) NOT NULL,
  `document_path` varchar(255) NOT NULL,
  `full_serial_number` int NOT NULL,
  `business_code` int NOT NULL,
  `document_code` int NOT NULL,
  PRIMARY KEY (`title`),
  UNIQUE KEY `document_path` (`document_path`),
  KEY `business_code` (`business_code`),
  KEY `document_code` (`document_code`),
  KEY `full_serial_number` (`full_serial_number`),
  CONSTRAINT `document_files_ibfk_1` FOREIGN KEY (`business_code`) REFERENCES `business_units` (`business_code`),
  CONSTRAINT `document_files_ibfk_2` FOREIGN KEY (`document_code`) REFERENCES `document_types` (`document_code`),
  CONSTRAINT `document_files_ibfk_3` FOREIGN KEY (`full_serial_number`) REFERENCES `records` (`full_serial_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `document_files`
--

LOCK TABLES `document_files` WRITE;
/*!40000 ALTER TABLE `document_files` DISABLE KEYS */;
INSERT INTO `document_files` VALUES ('A test title','Test Document Path',21081111,21,8);
/*!40000 ALTER TABLE `document_files` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `document_types`
--

DROP TABLE IF EXISTS `document_types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `document_types` (
  `title` varchar(255) NOT NULL,
  `summary` varchar(255) DEFAULT NULL,
  `document_code` int NOT NULL,
  PRIMARY KEY (`document_code`),
  UNIQUE KEY `title` (`title`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `document_types`
--

LOCK TABLES `document_types` WRITE;
/*!40000 ALTER TABLE `document_types` DISABLE KEYS */;
INSERT INTO `document_types` VALUES ('Template','NA',0),('Manuals/Policies','NA',1),('Workflow','NA',2),('Process/Procedure','NA',3),('Work Instruction','NA',4),('Form/Checklist','NA',5),('Presentation','NA',6),('Specification','NA',7),('Report','NA',8),('Drawing','NA',9),('Logs','NA',97),('Emails and Communication Records','NA',98),('Non-Communication Records','NA',99);
/*!40000 ALTER TABLE `document_types` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `records`
--

DROP TABLE IF EXISTS `records`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `records` (
  `business_series_index` int NOT NULL,
  `business_code` int NOT NULL,
  `document_code` int NOT NULL,
  `full_serial_number` int NOT NULL,
  `status` varchar(255) DEFAULT NULL,
  `title` varchar(255) NOT NULL,
  `custodian` varchar(255) DEFAULT NULL,
  `revision` varchar(255) DEFAULT NULL,
  `link` varchar(255) DEFAULT NULL,
  `sow_no` varchar(255) DEFAULT NULL,
  `issue_date` varchar(255) DEFAULT NULL,
  `effective_date` varchar(255) DEFAULT NULL,
  `reaffirmation_date` varchar(255) DEFAULT NULL,
  `protection_lvl` varchar(255) DEFAULT NULL,
  `ec_technical_data` tinyint(1) DEFAULT NULL,
  `permit` varchar(255) DEFAULT NULL,
  `ecl` varchar(255) DEFAULT NULL,
  `eccn` varchar(255) DEFAULT NULL,
  `usml` varchar(255) DEFAULT NULL,
  `cg` varchar(255) DEFAULT NULL,
  `us_exemption` varchar(255) DEFAULT NULL,
  `ca_exemption` varchar(255) DEFAULT NULL,
  `exp_date` varchar(255) DEFAULT NULL,
  `summary` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`full_serial_number`),
  UNIQUE KEY `title` (`title`),
  KEY `business_code` (`business_code`),
  KEY `document_code` (`document_code`),
  KEY `business_series_index` (`business_series_index`),
  CONSTRAINT `records_ibfk_1` FOREIGN KEY (`business_code`) REFERENCES `business_units` (`business_code`),
  CONSTRAINT `records_ibfk_2` FOREIGN KEY (`document_code`) REFERENCES `document_types` (`document_code`),
  CONSTRAINT `records_ibfk_3` FOREIGN KEY (`business_series_index`) REFERENCES `business_series` (`business_series_index`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `records`
--

LOCK TABLES `records` WRITE;
/*!40000 ALTER TABLE `records` DISABLE KEYS */;
INSERT INTO `records` VALUES (20,21,8,21081111,'Record','my title','','','','','','','','',1,'','','','','','','','','Look, a summary!'),(20,21,8,21081112,'Record','Next title','','','','','','','','',1,'','','','','','','','','NA'),(20,21,8,21081113,'Record','Next next title','','','','','','','','',1,'','','','','','','','','NA'),(20,21,8,21081114,'Record','largest','','','','','','','','',1,'','','','','','','','','NA'),(20,21,8,21081115,'Record','TIIITLE','','','','','','','','',1,'','','','','','','','','NA'),(20,21,8,21081116,'Record','AAAA TIIIITLE','','','','','','','','',1,'','','','','','','','','NA'),(20,21,8,21081117,'Record','NEWEST TITLE','','','','','','','','',1,'','','','','','','','','NA'),(20,21,8,210800008,'Record','new record','','','','','','','','',1,'','','','','','','','','NA'),(20,21,8,210800009,'Record','test_status','','','','','','','','',1,'','','','','','','','','NA'),(20,21,8,210800010,'Record','test_and','','','','','','','','',1,'','','','','','','','','NA'),(20,21,8,210800011,'WIP','fdasf','dsfads','dasf','asdf','352354','2020-03-20','2020-04-02','2020-03-17','Public: Public',1,'wegtarwa','rgrew','resgres','gsreresg','gregresg','gsgs','gergres','2020-03-18','NA'),(20,21,8,210800012,'Record','edfewwaf','fewafwef','dasfew','ewgrg','352353454','2020-04-01','2020-03-11','2020-03-11','Classified: Technical Private',1,'fwefwef','fewafafew','fewfwe','faferew','rgeregre','rgargwr','gawgrgreg','2020-04-07','NA'),(20,21,8,210800013,'Record','13','13','13','13','3543534','2020-03-10','2020-03-31','2020-03-10','Confidential: Non-Tech Private',1,'dfawegf','gregre','gergg','regreg','werewr','agreg','gesger','2020-03-07','NA'),(20,21,8,210800014,'Release','gesre','rgreswg','rgewrg','gwergreg','13433423423','2020-03-20','2020-04-03','2020-03-10','Public: Public',1,'trg3etge','regre','gregr','egre','rw','rwg','ggwre','2020-03-05','NA'),(20,22,1,220100001,'Obsolete','test_status_2','dsaf','dfasf','fas','4523465','2020-03-12','2020-03-24','2020-03-25','Classified: Technical Private',1,'regre','grewg','rewgre','rge','ewrgrew','rewgre','gwerg','2020-03-18','NA'),(20,22,8,220800001,'Record','New permits','','','','','','','','',1,'','','','','','','','','NA'),(20,23,3,230300001,'Record','test_option_3','','','','','','','','',1,'','','','','','','','','NA'),(20,23,4,230400001,'Record','test','','','','','','','','',1,'','','','','','','','','NA'),(20,23,4,230400002,'Record','I don\'t know','','','','','','','','',1,'','','','','','','','','NA'),(20,23,4,230400003,'Record','dsfadsf','','','','','','','','',1,'','','','','','','','','NA'),(20,23,4,230400004,'Record','test_date','','','','','','','','',1,'','','','','','','','','NA'),(30,31,2,310200001,'Record','','','','','','','','','',1,'','','','','','','','','NA'),(30,31,2,310200002,'Record','test_radio','','','','','','','','',1,'','','','','','','','','NA'),(30,31,2,310200003,'Record','test_option_2','','','','','','','','',1,'','','','','','','','','NA'),(30,32,1,320100001,'Record','test_all','','','','','','','','',1,'','','','','','','','','NA'),(30,32,3,320300001,'Record','test_title','test_custodian','test_revision','test_link','6666666666','2020-04-01','2020-04-01','2020-04-01','Public: Public',1,'test_permit','test_ecl','test_eccn','test_usml','test_cg','test_us','test_ca','2020-04-01','NA'),(30,33,2,330200001,'Record','test_option','','','','','','','','',1,'','','','','','','','','NA');
/*!40000 ALTER TABLE `records` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-03-30  0:17:43
