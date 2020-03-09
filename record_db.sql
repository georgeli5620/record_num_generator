-- MySQL dump 10.13  Distrib 8.0.19, for Win64 (x86_64)
--
-- Host: localhost    Database: mydatabase
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
  `title` varchar(255) NOT NULL,
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
INSERT INTO `records` VALUES (20,21,8,21081111,'my title','Look, a summary!'),(20,21,8,21081112,'Next title','NA'),(20,21,8,21081113,'Next next title','NA'),(20,21,8,21081114,'largest','NA'),(20,21,8,21081115,'TIIITLE','NA'),(20,21,8,21081116,'AAAA TIIIITLE','NA'),(20,21,8,21081117,'NEWEST TITLE','NA'),(20,21,8,210800008,'new record','NA'),(20,22,8,220800001,'New permits','NA');
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

-- Dump completed on 2020-03-09 13:26:53
