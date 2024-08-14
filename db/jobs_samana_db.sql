-- MySQL dump 10.13  Distrib 9.0.1, for macos14.4 (arm64)
--
-- Host: 127.0.0.1    Database: jobs_samana_db
-- ------------------------------------------------------
-- Server version	8.0.39

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
-- Table structure for table `admin_roles`
--

DROP TABLE IF EXISTS `admin_roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admin_roles` (
  `id` int NOT NULL AUTO_INCREMENT,
  `functionName` text NOT NULL,
  `authrole` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=67 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin_roles`
--

LOCK TABLES `admin_roles` WRITE;
/*!40000 ALTER TABLE `admin_roles` DISABLE KEYS */;
INSERT INTO `admin_roles` VALUES (1,'getUser',3),(2,'getUserDetails',3),(3,'listUsers',3),(4,'testDbConnection',3),(5,'listCandidateProfiles',3),(6,'listCandidateSkillsets',3),(7,'listCandidateReviews',3),(8,'listJobPostings',3),(9,'getCandidate',3),(10,'listCandidateCertifications',3),(11,'jobDetails',3),(12,'getCandidatesByProcess',3),(13,'getCandidateReviews',3),(14,'listJobCategories',3),(15,'addJobCategory',3),(16,'updateJobCategory',3),(17,'deleteJobCategory',3),(18,'listJobSkillsets',3),(19,'addJobSkillset',3),(20,'updateJobSkillset',3),(21,'deleteJobSkillset',3),(22,'listJobCategoriesAndSkillsets',3),(23,'listCertifications',3),(24,'addCertification',3),(25,'updateCertification',3),(26,'deleteCertification',3),(27,'getReviewerName',3),(28,'setCandidateSkillSet',3),(29,'getCandidateSkillset',3),(30,'deleteCandidateSkillset',3),(31,'getSkillsetCategory',3),(32,'createInterview',3),(33,'getInterviews',3),(34,'updateInterview',3),(35,'deleteInterview',3),(36,'addSystemUser',3),(37,'updateSystemUser',3),(38,'deleteSystemUser',3),(39,'listSystemUsers',3),(40,'listEmployees',3),(41,'addEmployee',3),(42,'getEmployee',3),(43,'updateEmployee',3),(44,'deleteEmployee',3),(45,'listEmployeeCertifications',3),(46,'addEmployeeCertification',3),(47,'deleteEmployeeCertification',3),(48,'listEmployeeSkillsets',3),(49,'addEmployeeSkillset',3),(50,'deleteEmployeeSkillset',3),(51,'listEmployeeReviews',3),(52,'addEmployeeReview',3),(53,'deleteEmployeeReview',3),(54,'updateEmployeeReview',3),(55,'addCandidateCertification',5),(56,'deleteCandidateCertification',3),(57,'addCandidateReview',3),(58,'removeCandidateReview',5),(59,'getJobProcess',3),(60,'getCandidateSalaryExpectation',3),(62,'listAdminRoles',3),(63,'addAdminRole',3),(64,'updateAdminRole',3),(65,'deleteAdminRole',3),(66,'getAdminRole',3);
/*!40000 ALTER TABLE `admin_roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `candidate_certifications`
--

DROP TABLE IF EXISTS `candidate_certifications`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `candidate_certifications` (
  `email` varchar(255) NOT NULL,
  `certification` varchar(255) NOT NULL,
  PRIMARY KEY (`email`,`certification`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `candidate_certifications`
--

LOCK TABLES `candidate_certifications` WRITE;
/*!40000 ALTER TABLE `candidate_certifications` DISABLE KEYS */;
INSERT INTO `candidate_certifications` VALUES ('','CCE-V Citrix Certified Expert - Virtualization'),('andrea.vanessa.giraldo@gmail.com','CCA-AppDS - Citrix Certified Associate – App Delivery and Security'),('andrea.vanessa.giraldo@gmail.com','CCA-N Citrix Certified Associate - Networking'),('andrea.vanessa.giraldo@gmail.com','FortiAnalyzer 7.0 Administrator'),('andrea.vanessa.giraldo@gmail.com','Fortinet Certified Professional Network Security'),('andrea.vanessa.giraldo@gmail.com','HCNA - Huawei technologies'),('andrea.vanessa.giraldo@gmail.com','HCNA WLAN - Huawei technologies'),('andrea.vanessa.giraldo@gmail.com','IBM Cloud Technical Advocate Foundations'),('andrea.vanessa.giraldo@gmail.com','ITIL v3 Foundation Certified'),('andrea.vanessa.giraldo@gmail.com','PMP'),('andrea.vanessa.giraldo@gmail.com','SCRUM MASTER PROFESSIONAL CERTIFICATE (SMPC)'),('estebanx00@gmail.com','AWS Certified Cloud Practitioner'),('juan.otalvaro@samanagroup.co','AWS Certified Cloud Practitioner'),('juan.otalvaro@samanagroup.co','AWS Certified Solutions Architect – Associate'),('juan.otalvaro@samanagroup.co','CCA-N Citrix Certified Associate - Networking'),('juan.otalvaro@samanagroup.co','CCP-N Citrix Certified Professional - Networking'),('juan.pablootalvaro@cloud.com','AWS Certified Cloud Practitioner'),('juan.pablootalvaro@cloud.com','AWS Certified Solutions Architect – Associate'),('juan.pablootalvaro@cloud.com','CCA-N Citrix Certified Associate - Networking'),('juan.pablootalvaro@cloud.com','CCP-N Citrix Certified Professional - Networking'),('lemoncho@gmail.com','CCA-V Citrix Certified Associate - Virtualization'),('lemoncho@gmail.com','CCE-V Citrix Certified Expert - Virtualization'),('lemoncho@gmail.com','CCP-V Citrix Certified Professional - Virtualization'),('marlonpachecoc@gmail.com','CCNA-Cisco Certified Network Associate'),('stban.acosta@gmail.com','Microsoft Certified: Azure Administrator Associate'),('ttbass@gmail.com','CCA-V Citrix Certified Associate - Virtualization'),('viru8589@gmail.com','CCA-V Citrix Certified Associate - Virtualization'),('viru8589@gmail.com','CCP-V Citrix Certified Professional - Virtualization'),('viru8589@gmail.com','Microsoft Certified: Azure Administrator Associate'),('wilmar.9220@gmail.com','Microsoft Certified: Azure Fundamentals'),('wilmar.9220@gmail.com','Microsoft Certified: Security, Compliance, and Identity Fundamentals'),('xencerra@gmail.com',''),('xencerra@gmail.com','AWS Certified Cloud Practitioner'),('xencerra@gmail.com','CCA-AppDS - Citrix Certified Associate – App Delivery and Security'),('xencerra@gmail.com','CCA-N Citrix Certified Associate - Networking'),('xencerra@gmail.com','CCA-V Citrix Certified Associate - Virtualization'),('xencerra@gmail.com','CCE-N Citrix Certified Expert - Networking'),('xencerra@gmail.com','CCE-V Citrix Certified Expert - Virtualization'),('xencerra@gmail.com','CCNA-Cisco Certified Network Associate'),('xencerra@gmail.com','CCP-AppDS - Citrix Certified Professional – App Delivery and Security'),('xencerra@gmail.com','CCP-N Citrix Certified Professional - Networking'),('xencerra@gmail.com','CCP-V Citrix Certified Professional - Virtualization'),('xencerra@gmail.com','Microsoft Certified: Azure Administrator Associate'),('xencerra@gmail.com','Microsoft Certified: Azure Fundamentals');
/*!40000 ALTER TABLE `candidate_certifications` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `candidate_profiles`
--

DROP TABLE IF EXISTS `candidate_profiles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `candidate_profiles` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `phone_number` varchar(50) DEFAULT NULL,
  `location` varchar(255) DEFAULT NULL,
  `english_level` varchar(255) DEFAULT NULL,
  `profile_photo` varchar(255) DEFAULT NULL,
  `candidate_cv` varchar(255) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `enabled` int DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=59 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `candidate_profiles`
--

LOCK TABLES `candidate_profiles` WRITE;
/*!40000 ALTER TABLE `candidate_profiles` DISABLE KEYS */;
INSERT INTO `candidate_profiles` VALUES (14,'Eric Pardo','ericjpardo@gmail.com','+573027020822','Barranquila, Atlantico','C1','0',NULL,'2024-05-22 12:44:46',1),(19,'Nicolas Rodriguez E','nico.rodriguez824@gmail.com','+573026609825','Medellin-Colombia','C1','0','https://drive.google.com/open?id=1xHBJQyDmXBxEE3HclGJBUCnlE4W8gqbZ','2024-05-25 17:16:47',0),(20,'Viralkumar Godhani','viru8589@gmail.com','5148033514','Montreal','C2','0','https://drive.google.com/open?id=1hucXfAukhnvdZJ3jex0ZybyfQS8lf8Da','2024-05-29 01:43:04',0),(22,'Alexandre Chaves','ttbass@gmail.com','4388691294','Canada ','B2','0','https://drive.google.com/open?id=1o4j3N9nPEc_a7sYt-h7_IE7igxvL1viW','2024-05-30 03:13:52',0),(23,'Jair Becerra Espinosa','xencerra@gmail.com','+525534660573','Mexico','C1',NULL,'https://drive.google.com/open?id=11dhxLK6aEM9xaCOpcNGWi9gKutUJGwEz','2024-05-30 14:08:43',1),(26,'Bhanu Prakash Reddy Thoppi Reddy','bhanuthoppireddy@gmail.com','+15145494377','Montreal. Canada','B2','0','https://drive.google.com/open?id=1PebY9V2gLihwsYKO1QQI5NYFIxHmxvc3','2024-05-30 22:01:20',0),(27,'Sergio Esteban Acosta Garzon','stban.acosta@gmail.com','+573004012809','Bogotá, Colombia','B2',NULL,'https://drive.google.com/open?id=15ewEC4PtSwDUhXiy8am11TsqgLY1rp1_','2024-05-30 22:50:27',0),(37,'JOYN FREDY ARAGON','jfaragon100@gmail.com','+573125785934','Bogotá','B1','',NULL,'2024-06-19 23:03:35',1),(40,'Geovanny Francisco Belalcazar','franciscobelalcazar@gmail.com','+593 994514856','Ecuador','B1','0','https://drive.google.com/open?id=1fH0o0QDiLW1mUFH224wC3F8a5u-GPGIy','2024-06-19 23:22:23',1),(41,'Eric Wang','likewang0325@gmail.com','+8613918021212','China','C1','','https://drive.google.com/open?id=1KQfBbEkUZNsmCr4Lj1qvdgvI-J6er1k3','2024-06-19 23:27:56',1),(42,'Andrea Vanessa Giraldo Barrera','andrea.vanessa.giraldo@gmail.com','+573127518718','Envigado','B1','','https://drive.google.com/open?id=1cefCWimLNHNxuXclsrdO46PMm1FGNRNe','2024-06-19 23:29:56',1),(43,'Wilmar Giovanny Cardenas Escobar','wilmar.9220@gmail.com','+57 3174925220','Cali, Valle del Cauca, Colombia','B1','','https://drive.google.com/open?id=1FHqeEm8D-6psL0KFV0jlSbZoFJtR9_18','2024-06-20 01:31:19',1),(44,'Juan Esteban','estebanx00@gmail.com','+573153989844','Girón, Santander, COL','B2','','https://drive.google.com/open?id=1r9TPlAkN7sIXVXEElwcloGXrGZCwt5ro','2024-06-20 13:19:05',1),(45,'Marlon Pacheco','marlonpachecoc@gmail.com','+57 3243651976','Barranquilla','B2','0','https://drive.google.com/open?id=1E9VB4JqdJR_UmJ2Qg3G9OOY48q3hm84M','2024-06-20 14:53:01',1),(46,'Henry Marquez','henry.marquez.baez@gmail.com','+573218619234','Medellin, colombia','C2','0',NULL,'2024-06-20 18:39:15',1),(47,'Fiodor C','ficero18@gmail.com','+573003944326','Colombia','C1',NULL,'https://drive.google.com/open?id=1sQRMCx2Y4xh_8RreAElpfOxkvsSFc5EN','2024-06-20 20:37:04',1),(49,'Henry Marquez','henry.marquez.b@gmail.com','+573218619234','Medellin Colombia ','C2',NULL,'https://drive.google.com/open?id=1to3mounaS8eW6tIi87OY03yuF9b2E9Nx','2024-06-20 21:11:07',1),(50,'FRANCISCO JAVIER CASTRO ALZATE','fjca82@gmail.com','+573136847650','Colombia','A1','',NULL,'2024-06-20 23:05:02',1),(54,'Juan Pablo Otalvaro','otalvaroj@gmail.com','+573138060575','Manizales- Caldas','B2','0',NULL,'2024-06-24 18:10:46',0),(55,'Juan Pablo Otalvaro','juan.otalvaro@samanagroup.co','+573138060575','Miami','C1','https://lh3.googleusercontent.com/a/ACg8ocJ63PiVOvjMOWzDg1Dq5DO0uxODftn7tmwUD5mj4DoJH4m3B2U=s96-c',NULL,'2024-06-24 19:54:35',1),(57,'Rafael Cortes','lemoncho@gmail.com','+57 3182543524','Cajica / Colombia','A1','https://lh3.googleusercontent.com/a/ACg8ocK3rNFQkfUk--dfeZ6lU-XMGRTEXZq_TqiexU2kSmrpMxNY=s96-c',NULL,'2024-06-27 23:41:34',1),(58,'Juan Pablo Otalvaro (C)','juan.pablootalvaro@cloud.com','3138060575','Manizales','B2','https://lh3.googleusercontent.com/a/ACg8ocLdrYhbffYz4rVnzK1F4iSI3Qf6KGZ-EF_eenDLTghhkn_xbPE=s96-c',NULL,'2024-06-28 14:58:52',1);
/*!40000 ALTER TABLE `candidate_profiles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `candidate_review`
--

DROP TABLE IF EXISTS `candidate_review`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `candidate_review` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(255) NOT NULL,
  `process` text,
  `salary_expectation` int DEFAULT NULL,
  `availability` text,
  `interview` text,
  `interviewer_name` varchar(255) DEFAULT NULL,
  `interviewer_email` varchar(255) DEFAULT NULL,
  `evaluation_field` text,
  `rating` int DEFAULT NULL,
  `observations` text,
  `approved` text,
  `review_date` date DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `candidate_review`
--

LOCK TABLES `candidate_review` WRITE;
/*!40000 ALTER TABLE `candidate_review` DISABLE KEYS */;
INSERT INTO `candidate_review` VALUES (1,'stban.acosta@gmail.com','14',5000,'Within one month','First Interview','Juan Pablo Otalvaro','juan.otalvaro@samanagroup.co','Technical Evaluation',4,'Demonstrates a solid mid-level understanding of English and has valuable experience with Citrix. This candidate is well-suited for advancement to an L2 role.','Yes','2024-05-30'),(2,'juan.pablootalvaro@cloud.com','12',5000,'Immediately','First Interview','Juan Pablo Otalvaro','juan.otalvaro@samanagroup.co','Portfolio Review',5,'0','Yes','2024-05-30'),(3,'juan.pablootalvaro@cloud.com','12',NULL,NULL,'Second Interview','Juan Pablo Otalvaro','juan.otalvaro@samanagroup.co','Initial filter',5,'0','Yes','2024-05-30'),(4,'juan.pablootalvaro@cloud.com','12',NULL,NULL,'Additional Interview','Juan Pablo Otalvaro','juan.otalvaro@samanagroup.co','Initial filter',4,'0','No','2024-05-30'),(8,'stban.acosta@gmail.com','14',NULL,NULL,'Second Interview','Danny Ruiz','danny.ruiz@samanagroup.co','Problem-Solving Skills',3,'He met the expectations regarding critical issues and other scenarios.','Yes','2024-05-30'),(12,'stban.acosta@gmail.com','14',NULL,NULL,'Second Interview','Juan Pablo Otalvaro','juan.otalvaro@samanagroup.co','Initial filter',3,'Good candidate for level 2. ','Yes','2024-05-31'),(13,'viru8589@gmail.com','12',9200,'Within two weeks','First Interview','Juan Pablo Otalvaro','juan.otalvaro@samanagroup.co','Initial filter',4,'Demonstrates good English proficiency and relevant Citrix experience. Has the potential to succeed in an L3 role with additional development.','Yes','2024-05-31'),(14,'ttbass@gmail.com','12',6000,'Immediately','First Interview','Juan Pablo Otalvaro','juan.otalvaro@samanagroup.co','Initial filter',3,'Possesses a good foundation in English communication and solid Citrix skills. With targeted training, this candidate could readily transition into an L2 position.','Yes','2024-05-31'),(15,'stban.acosta@gmail.com','14',NULL,NULL,'Second Interview','Fabian Baena','fabian.baena@samanagroup.co','Technical Evaluation',4,'Has good technical knowledge. \r\nGood CVAD knowledge with MCS, PVS. 4\r\nBasic knowledge on Netscaler 3\r\nGood AD knowledge 4','Yes','2024-05-31'),(16,'ttbass@gmail.com','12',NULL,NULL,'Second Interview','Jorge Gomez','Jorge.Gomez@samanagroup.co','Initial filter',2,'Samana cannot meet his salary expectations.','Yes','2024-05-31'),(17,'stban.acosta@gmail.com','14',NULL,NULL,'Second Interview','Jorge Gomez','Jorge.Gomez@samanagroup.co','Initial filter',3,'JP needs to have salary expectation discussions with him.','Yes','2024-05-31'),(18,'ttbass@gmail.com','12',NULL,NULL,'Second Interview','Danny Ruiz','danny.ruiz@samanagroup.co','Communication Skills',3,'Met the expectations','Yes','2024-05-31'),(19,'stban.acosta@gmail.com','14',NULL,NULL,'Additional Interview','Juan Pablo Otalvaro','juan.otalvaro@samanagroup.co','Initial filter',3,'During our conversation with the candidate, we suggested that he might be more suitable for a Level 2 role rather than the Level 3 Service Desk Engineer position, in an effort to align his salary expectations with the approved budget for this role. However, Sergio stated that his minimum acceptable salary is $4,500 USD, which exceeds the allocated budget.','No','2024-06-07'),(23,'nico.rodriguez824@gmail.com','14',8000000,'Immediately','First Interview','Juan Pablo Otalvaro','juan.otalvaro@samanagroup.co','Initial filter',2,'Good English Level, however, his technical background does not demonstrate his experience in Citrix. Not qualified to Second Interview. ','No','2024-06-18'),(24,'bhanuthoppireddy@gmail.com','12',100000,'Immediately','First Interview','Juan Pablo Otalvaro','juan.otalvaro@samanagroup.co','Initial filter',4,'Good Candidate, good level of english and Good Citrix Experience. Good Candidate to L3, however, his salary expectation is way higher than the salary Range.\r\n','No','2024-06-18'),(29,'estebanx00@gmail.com','19',800,'Immediately','First Interview','Juan Pablo Otalvaro','juan.otalvaro@samanagroup.co','Initial filter',3,'The candidate has knowledge in AWS; however, they do not have technical knowledge in Citrix technologies, so they would qualify for level 1. Their English proficiency is below the standard, so they are only recommended for clients in Latin America.','Yes','2024-06-20'),(30,'xencerra@gmail.com','12',4500,'Immediately','First Interview','Juan Pablo Otalvaro','juan.otalvaro@samanagroup.co','Initial filter',5,'The candidate has very good knowledge of Citrix, a good level of English, and experience with Microsoft technologies as well as MS Azure. A good candidate for level 2 or Level 3. His current salary is 4.000 but he might be able to negotiate up to $ 4.500 USD per month.','Yes','2024-06-20'),(31,'marlonpachecoc@gmail.com','19',2500,'Within two weeks','First Interview','Juan Pablo Otalvaro','juan.otalvaro@samanagroup.co','Initial filter',2,'The candidate has a good level of English; however, they do not have experience with Citrix technologies. The candidate has experience with VMWare. The candidate does not qualify for level 2; however, they are a good candidate for level 1. Salary Expectation between $1.500 -$2.500','Yes','2024-06-20'),(32,'henry.marquez.b@gmail.com','19',2000,'Immediately','First Interview','Juan Pablo Otalvaro','juan.otalvaro@samanagroup.co','Initial filter',3,'The candidate has a good level of English; however, they do not have experience with Citrix technologies. The candidate has experience with VMWare. The candidate does not qualify for level 2; however, they are a good candidate for level 1.  Salary expectation $1.500 - $2.300','Yes','2024-06-20'),(33,'andrea.vanessa.giraldo@gmail.com','19',1800,'More than a month','First Interview','Juan Pablo Otalvaro','juan.otalvaro@samanagroup.co','Initial filter',3,'Below average level of English, good experience in NetScaler and Networking, but not much experience in Citrix technologies. A good candidate for level 1, or possibly level 2 if it is for NetScaler.','Yes','2024-06-20'),(34,'viru8589@gmail.com','12',NULL,NULL,'Second Interview','Juan Pablo Otalvaro','juan.otalvaro@samanagroup.co','Initial filter',3,'Salary expectation is well above the range assigned for the role.','No','2024-06-20'),(35,'xencerra@gmail.com','12',NULL,NULL,'Second Interview','Felipe Bernal','felipe.bernal@samanagroup.co','Portfolio Review',4,'Good fit for the current needs of the managed services team and potential future needs (Azure and AVD certifications).  Extensive Citrix experience and would be ready to hit the ground running with our team and customers on day one. Has experience in CVAD and NetScaler. Also has certs in both CCA-N and CCP-V. Is looking for a new technical challenge from his current role.\r\n\r\nHas experience in the medical vertical - supporting Citrix environments for hospitals. \r\n\r\nEnglish is good but not outstanding. Has room for growth in this area. Adequate for supporting our customers in the US. This is probably the key point keeping him from being a 5/5.\r\n\r\nNext Steps from technical standpoint is to get CCE-V and hands on experience in Azure. ','Yes','2024-06-21'),(36,'xencerra@gmail.com','12',NULL,NULL,'Second Interview','Danny Ruiz','danny.ruiz@samanagroup.co','Initial filter',3,'Meets my expectations.','Yes','2024-06-21'),(37,'xencerra@gmail.com','12',NULL,NULL,'Second Interview','Juan Pablo Otalvaro','juan.otalvaro@samanagroup.co','Initial filter',5,'The candidate has very good knowledge of Citrix technologies, including NetScaler. Their English level needs some improvement, but they are a very good candidate for the L3 role. Candidate recommended for this role.','Yes','2024-06-21'),(38,'xencerra@gmail.com','12',NULL,NULL,'Second Interview','Alonso Maury Santana Torres','alonso.santana@samanagroup.co','Initial filter',3,'Highly motivated, wide proven experience. ','Yes','2024-06-22'),(39,'xencerra@gmail.com','12',NULL,NULL,'Second Interview','Jorge Gomez','Jorge.Gomez@samanagroup.co','Initial filter',3,'Had met Jair long ago and tried to hire him 10 years ago.  He did not accept the position because he wanted a Permanent Employee role.','Yes','2024-06-24'),(40,'ttbass@gmail.com','12',NULL,NULL,'Second Interview','Juan Pablo Otalvaro','juan.otalvaro@samanagroup.co','Initial filter',2,'The salary expectation is outside of the range for this role.','No','2024-06-24');
/*!40000 ALTER TABLE `candidate_review` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `candidate_skillsets`
--

DROP TABLE IF EXISTS `candidate_skillsets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `candidate_skillsets` (
  `id` int NOT NULL AUTO_INCREMENT,
  `candidate_id` int NOT NULL,
  `email` varchar(255) NOT NULL,
  `category` varchar(255) NOT NULL,
  `skillset` varchar(255) NOT NULL,
  `rating` int NOT NULL,
  `reviewer_id` int NOT NULL,
  `reviewer_email` varchar(255) NOT NULL,
  `comment` text,
  `timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `candidate_id` (`candidate_id`),
  KEY `reviewer_id` (`reviewer_id`),
  CONSTRAINT `candidate_skillsets_chk_1` CHECK (((`rating` >= 1) and (`rating` <= 5)))
) ENGINE=InnoDB AUTO_INCREMENT=335 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `candidate_skillsets`
--

LOCK TABLES `candidate_skillsets` WRITE;
/*!40000 ALTER TABLE `candidate_skillsets` DISABLE KEYS */;
INSERT INTO `candidate_skillsets` VALUES (1,13,'juan.otalvaro@samanagroup.co','Citrix Virtual Apps and Desktops','Installation and Configuration',5,1,'juan.otalvaro@samanagroup.co','','2024-06-13 23:05:03'),(6,13,'Juan.otalvaro@samanagroup.co','Windows Server Administration','Active Directory Management',3,1,'juan.otalvaro@samanagroup.co','','2024-06-13 23:10:09'),(12,13,'Juan.otalvaro@samanagroup.co','Citrix Virtual Apps and Desktops','Managing Machine Catalogs and Delivery Groups',5,1,'juan.otalvaro@samanagroup.co','','2024-06-13 23:13:46'),(13,13,'Juan.otalvaro@samanagroup.co','Citrix Virtual Apps and Desktops','Application Publishing',4,1,'juan.otalvaro@samanagroup.co','','2024-06-13 23:13:48'),(14,13,'Juan.otalvaro@samanagroup.co','Citrix Virtual Apps and Desktops','Profile Management',5,1,'juan.otalvaro@samanagroup.co','','2024-06-13 23:13:48'),(15,13,'Juan.otalvaro@samanagroup.co','Citrix Virtual Apps and Desktops','StoreFront Configuration',3,1,'juan.otalvaro@samanagroup.co','','2024-06-13 23:13:50'),(16,13,'Juan.otalvaro@samanagroup.co','Citrix Virtual Apps and Desktops','Citrix Policies',5,1,'juan.otalvaro@samanagroup.co','','2024-06-13 23:13:51'),(17,13,'Juan.otalvaro@samanagroup.co','Citrix Virtual Apps and Desktops','Monitoring and Troubleshooting',3,1,'juan.otalvaro@samanagroup.co','','2024-06-13 23:13:51'),(18,13,'Juan.otalvaro@samanagroup.co','Citrix Virtual Apps and Desktops','Citrix Director',5,1,'juan.otalvaro@samanagroup.co','','2024-06-13 23:13:53'),(59,20,'viru8589@gmail.com','Citrix Virtual Apps and Desktops','Installation and Configuration',4,1,'juan.otalvaro@samanagroup.co','','2024-06-13 23:39:26'),(60,20,'viru8589@gmail.com','Citrix Virtual Apps and Desktops','Managing Machine Catalogs and Delivery Groups',4,1,'juan.otalvaro@samanagroup.co','','2024-06-13 23:39:27'),(61,20,'viru8589@gmail.com','Citrix Virtual Apps and Desktops','Application Publishing',3,1,'juan.otalvaro@samanagroup.co','','2024-06-13 23:39:28'),(62,20,'viru8589@gmail.com','Citrix Virtual Apps and Desktops','Profile Management',4,1,'juan.otalvaro@samanagroup.co','','2024-06-13 23:39:28'),(63,20,'viru8589@gmail.com','Citrix Virtual Apps and Desktops','StoreFront Configuration',4,1,'juan.otalvaro@samanagroup.co','','2024-06-13 23:39:29'),(64,20,'viru8589@gmail.com','Citrix Virtual Apps and Desktops','Citrix Policies',4,1,'juan.otalvaro@samanagroup.co','','2024-06-13 23:39:30'),(65,20,'viru8589@gmail.com','Citrix Virtual Apps and Desktops','Monitoring and Troubleshooting',5,1,'juan.otalvaro@samanagroup.co','','2024-06-13 23:39:31'),(70,22,'ttbass@gmail.com','Citrix Virtual Apps and Desktops','Installation and Configuration',4,1,'juan.otalvaro@samanagroup.co','','2024-06-14 01:42:51'),(71,22,'ttbass@gmail.com','Citrix Virtual Apps and Desktops','Managing Machine Catalogs and Delivery Groups',5,1,'juan.otalvaro@samanagroup.co','','2024-06-14 01:42:52'),(72,22,'ttbass@gmail.com','Citrix Virtual Apps and Desktops','Application Publishing',4,1,'juan.otalvaro@samanagroup.co','','2024-06-14 01:42:53'),(73,22,'ttbass@gmail.com','Citrix Virtual Apps and Desktops','StoreFront Configuration',3,1,'juan.otalvaro@samanagroup.co','','2024-06-14 05:06:00'),(152,14,'ericjpardo@gmail.com','Citrix Virtual Apps and Desktops','Installation and Configuration',5,1,'juan.otalvaro@samanagroup.co','','2024-06-18 18:54:33'),(166,23,'xencerra@gmail.com','Citrix Virtual Apps and Desktops','Installation and Configuration',5,28,'fabian.baena@samanagroup.co','','2024-06-18 19:22:24'),(167,23,'xencerra@gmail.com','Citrix Virtual Apps and Desktops','Managing Machine Catalogs and Delivery Groups',3,1,'juan.otalvaro@samanagroup.co','','2024-06-18 19:22:25'),(194,44,'estebanx00@gmail.com','AWS','EC2 Management',4,1,'juan.otalvaro@samanagroup.co','','2024-06-20 21:40:16'),(195,44,'estebanx00@gmail.com','AWS','S3 Storage Solutions',3,1,'juan.otalvaro@samanagroup.co','','2024-06-20 21:40:17'),(196,44,'estebanx00@gmail.com','AWS','VPC Configuration',3,1,'juan.otalvaro@samanagroup.co','','2024-06-20 21:40:19'),(197,44,'estebanx00@gmail.com','AWS','IAM Policies and Roles',4,1,'juan.otalvaro@samanagroup.co','','2024-06-20 21:40:20'),(198,44,'estebanx00@gmail.com','Citrix Virtual Apps and Desktops','Installation and Configuration',1,1,'juan.otalvaro@samanagroup.co','','2024-06-20 21:40:26'),(199,44,'estebanx00@gmail.com','Citrix Virtual Apps and Desktops','Managing Machine Catalogs and Delivery Groups',1,1,'juan.otalvaro@samanagroup.co','','2024-06-20 21:40:26'),(200,44,'estebanx00@gmail.com','Citrix Virtual Apps and Desktops','Application Publishing',1,1,'juan.otalvaro@samanagroup.co','','2024-06-20 21:40:27'),(201,23,'xencerra@gmail.com','Windows Server Administration','Active Directory Management',4,1,'juan.otalvaro@samanagroup.co','','2024-06-20 21:45:45'),(202,23,'xencerra@gmail.com','Windows Server Administration','Installation and Configuration',4,1,'juan.otalvaro@samanagroup.co','','2024-06-20 21:45:46'),(203,23,'xencerra@gmail.com','Windows Server Administration','Group Policy Management',4,1,'juan.otalvaro@samanagroup.co','','2024-06-20 21:46:59'),(204,23,'xencerra@gmail.com','Windows Server Administration','DNS and DHCP Configuration',4,1,'juan.otalvaro@samanagroup.co','','2024-06-20 21:47:26'),(205,23,'xencerra@gmail.com','Windows Server Administration','File and Storage Services',3,1,'juan.otalvaro@samanagroup.co','','2024-06-20 21:47:42'),(206,23,'xencerra@gmail.com','Windows Server Administration','Remote Desktop Services (RDS)',5,1,'juan.otalvaro@samanagroup.co','','2024-06-20 21:47:51'),(207,23,'xencerra@gmail.com','Windows Server Administration','Backup and Restore',4,1,'juan.otalvaro@samanagroup.co','','2024-06-20 21:47:52'),(208,23,'xencerra@gmail.com','Windows Server Administration','PowerShell Scripting',3,1,'juan.otalvaro@samanagroup.co','','2024-06-20 21:48:09'),(209,23,'xencerra@gmail.com','Citrix Virtual Apps and Desktops','Application Publishing',5,28,'fabian.baena@samanagroup.co','','2024-06-20 21:48:29'),(210,23,'xencerra@gmail.com','Citrix Virtual Apps and Desktops','Profile Management',4,28,'fabian.baena@samanagroup.co','','2024-06-20 21:48:46'),(211,23,'xencerra@gmail.com','Citrix Virtual Apps and Desktops','StoreFront Configuration',5,28,'fabian.baena@samanagroup.co','','2024-06-20 21:48:52'),(212,23,'xencerra@gmail.com','Citrix Virtual Apps and Desktops','Citrix Policies',5,28,'fabian.baena@samanagroup.co','','2024-06-20 21:48:57'),(213,23,'xencerra@gmail.com','Citrix Virtual Apps and Desktops','Monitoring and Troubleshooting',5,28,'fabian.baena@samanagroup.co','','2024-06-20 21:49:03'),(214,23,'xencerra@gmail.com','Citrix Virtual Apps and Desktops','Citrix Director',5,28,'fabian.baena@samanagroup.co','','2024-06-20 21:49:08'),(215,23,'xencerra@gmail.com','Citrix Virtual Apps and Desktops','Citrix Studio',5,28,'fabian.baena@samanagroup.co','','2024-06-20 21:49:09'),(216,23,'xencerra@gmail.com','Citrix Virtual Apps and Desktops','Load Balancing',5,28,'fabian.baena@samanagroup.co','','2024-06-20 21:49:18'),(217,45,'marlonpachecoc@gmail.com','Windows Server Administration','Installation and Configuration',3,1,'juan.otalvaro@samanagroup.co','','2024-06-20 22:00:58'),(218,45,'marlonpachecoc@gmail.com','Windows Server Administration','Active Directory Management',5,1,'juan.otalvaro@samanagroup.co','','2024-06-20 22:01:47'),(219,45,'marlonpachecoc@gmail.com','Windows Server Administration','Group Policy Management',5,1,'juan.otalvaro@samanagroup.co','','2024-06-20 22:01:51'),(220,45,'marlonpachecoc@gmail.com','Windows Server Administration','DNS and DHCP Configuration',5,1,'juan.otalvaro@samanagroup.co','','2024-06-20 22:01:57'),(221,45,'marlonpachecoc@gmail.com','Windows Server Administration','File and Storage Services',3,1,'juan.otalvaro@samanagroup.co','','2024-06-20 22:02:05'),(222,45,'marlonpachecoc@gmail.com','Windows Server Administration','Windows Server Update Services (WSUS)',3,1,'juan.otalvaro@samanagroup.co','','2024-06-20 22:02:11'),(223,45,'marlonpachecoc@gmail.com','Windows Server Administration','Remote Desktop Services (RDS)',5,1,'juan.otalvaro@samanagroup.co','','2024-06-20 22:02:17'),(224,45,'marlonpachecoc@gmail.com','Windows Server Administration','Performance Monitoring and Tuning',4,1,'juan.otalvaro@samanagroup.co','','2024-06-20 22:02:21'),(225,45,'marlonpachecoc@gmail.com','Windows Server Administration','Backup and Restore',4,1,'juan.otalvaro@samanagroup.co','','2024-06-20 22:02:21'),(226,45,'marlonpachecoc@gmail.com','Windows Server Administration','PowerShell Scripting',2,1,'juan.otalvaro@samanagroup.co','','2024-06-20 22:02:29'),(227,45,'marlonpachecoc@gmail.com','Citrix Virtual Apps and Desktops','Installation and Configuration',1,1,'juan.otalvaro@samanagroup.co','','2024-06-20 22:02:52'),(228,45,'marlonpachecoc@gmail.com','Citrix Virtual Apps and Desktops','Managing Machine Catalogs and Delivery Groups',1,1,'juan.otalvaro@samanagroup.co','','2024-06-20 22:02:53'),(229,45,'marlonpachecoc@gmail.com','Citrix Virtual Apps and Desktops','Application Publishing',1,1,'juan.otalvaro@samanagroup.co','','2024-06-20 22:02:54'),(230,45,'marlonpachecoc@gmail.com','Citrix Virtual Apps and Desktops','Profile Management',1,1,'juan.otalvaro@samanagroup.co','','2024-06-20 22:02:54'),(231,45,'marlonpachecoc@gmail.com','Citrix Virtual Apps and Desktops','StoreFront Configuration',1,1,'juan.otalvaro@samanagroup.co','','2024-06-20 22:02:55'),(232,45,'marlonpachecoc@gmail.com','Citrix Virtual Apps and Desktops','Citrix Policies',1,1,'juan.otalvaro@samanagroup.co','','2024-06-20 22:02:56'),(233,45,'marlonpachecoc@gmail.com','Citrix Virtual Apps and Desktops','Monitoring and Troubleshooting',1,1,'juan.otalvaro@samanagroup.co','','2024-06-20 22:02:57'),(234,45,'marlonpachecoc@gmail.com','Citrix Virtual Apps and Desktops','Citrix Director',1,1,'juan.otalvaro@samanagroup.co','','2024-06-20 22:02:57'),(235,45,'marlonpachecoc@gmail.com','Citrix Virtual Apps and Desktops','Citrix Studio',1,1,'juan.otalvaro@samanagroup.co','','2024-06-20 22:02:58'),(236,45,'marlonpachecoc@gmail.com','Citrix Virtual Apps and Desktops','Load Balancing',1,1,'juan.otalvaro@samanagroup.co','','2024-06-20 22:02:59'),(237,45,'marlonpachecoc@gmail.com','Networking','Fundamentals',4,1,'juan.otalvaro@samanagroup.co','','2024-06-20 22:03:08'),(238,45,'marlonpachecoc@gmail.com','Networking','OSI and TCP/IP Models',5,1,'juan.otalvaro@samanagroup.co','','2024-06-20 22:03:09'),(239,45,'marlonpachecoc@gmail.com','Networking','Switching Concepts',3,1,'juan.otalvaro@samanagroup.co','','2024-06-20 22:03:10'),(240,45,'marlonpachecoc@gmail.com','Networking','IPv4 and IPv6 Addressing',4,1,'juan.otalvaro@samanagroup.co','','2024-06-20 22:03:11'),(241,45,'marlonpachecoc@gmail.com','Networking','VLANs',5,1,'juan.otalvaro@samanagroup.co','','2024-06-20 22:03:12'),(242,45,'marlonpachecoc@gmail.com','Networking','Routing',3,1,'juan.otalvaro@samanagroup.co','','2024-06-20 22:03:13'),(243,45,'marlonpachecoc@gmail.com','Networking','Troubleshooting',3,1,'juan.otalvaro@samanagroup.co','','2024-06-20 22:03:15'),(244,45,'marlonpachecoc@gmail.com','Networking','Cloud Networking',2,1,'juan.otalvaro@samanagroup.co','','2024-06-20 22:03:17'),(245,49,'henry.marquez.b@gmail.com','Citrix Virtual Apps and Desktops','Installation and Configuration',1,1,'juan.otalvaro@samanagroup.co','','2024-06-20 22:09:16'),(246,49,'henry.marquez.b@gmail.com','Citrix Virtual Apps and Desktops','Managing Machine Catalogs and Delivery Groups',1,1,'juan.otalvaro@samanagroup.co','','2024-06-20 22:09:16'),(247,49,'henry.marquez.b@gmail.com','Citrix Virtual Apps and Desktops','Application Publishing',1,1,'juan.otalvaro@samanagroup.co','','2024-06-20 22:09:17'),(248,49,'henry.marquez.b@gmail.com','Citrix Virtual Apps and Desktops','Profile Management',1,1,'juan.otalvaro@samanagroup.co','','2024-06-20 22:09:17'),(249,49,'henry.marquez.b@gmail.com','Citrix Virtual Apps and Desktops','StoreFront Configuration',1,1,'juan.otalvaro@samanagroup.co','','2024-06-20 22:09:18'),(250,49,'henry.marquez.b@gmail.com','Citrix Virtual Apps and Desktops','Citrix Policies',1,1,'juan.otalvaro@samanagroup.co','','2024-06-20 22:09:19'),(251,49,'henry.marquez.b@gmail.com','Citrix Virtual Apps and Desktops','Monitoring and Troubleshooting',1,1,'juan.otalvaro@samanagroup.co','','2024-06-20 22:09:19'),(252,49,'henry.marquez.b@gmail.com','Citrix Virtual Apps and Desktops','Citrix Director',1,1,'juan.otalvaro@samanagroup.co','','2024-06-20 22:09:21'),(253,49,'henry.marquez.b@gmail.com','Citrix Virtual Apps and Desktops','Citrix Studio',1,1,'juan.otalvaro@samanagroup.co','','2024-06-20 22:09:21'),(254,49,'henry.marquez.b@gmail.com','Citrix Virtual Apps and Desktops','Load Balancing',1,1,'juan.otalvaro@samanagroup.co','','2024-06-20 22:09:22'),(255,49,'henry.marquez.b@gmail.com','Windows Server Administration','Installation and Configuration',3,1,'juan.otalvaro@samanagroup.co','','2024-06-20 22:09:27'),(256,49,'henry.marquez.b@gmail.com','Windows Server Administration','Active Directory Management',5,1,'juan.otalvaro@samanagroup.co','','2024-06-20 22:09:28'),(257,49,'henry.marquez.b@gmail.com','Windows Server Administration','Group Policy Management',5,1,'juan.otalvaro@samanagroup.co','','2024-06-20 22:09:28'),(258,49,'henry.marquez.b@gmail.com','Windows Server Administration','DNS and DHCP Configuration',5,1,'juan.otalvaro@samanagroup.co','','2024-06-20 22:09:29'),(259,49,'henry.marquez.b@gmail.com','Windows Server Administration','File and Storage Services',4,1,'juan.otalvaro@samanagroup.co','','2024-06-20 22:09:30'),(260,49,'henry.marquez.b@gmail.com','Windows Server Administration','Windows Server Update Services (WSUS)',5,1,'juan.otalvaro@samanagroup.co','','2024-06-20 22:09:31'),(261,49,'henry.marquez.b@gmail.com','Windows Server Administration','Performance Monitoring and Tuning',5,1,'juan.otalvaro@samanagroup.co','','2024-06-20 22:09:32'),(262,49,'henry.marquez.b@gmail.com','Windows Server Administration','Backup and Restore',3,1,'juan.otalvaro@samanagroup.co','','2024-06-20 22:09:35'),(263,49,'henry.marquez.b@gmail.com','Windows Server Administration','Remote Desktop Services (RDS)',5,1,'juan.otalvaro@samanagroup.co','','2024-06-20 22:09:35'),(264,49,'henry.marquez.b@gmail.com','Windows Server Administration','PowerShell Scripting',3,1,'juan.otalvaro@samanagroup.co','','2024-06-20 22:09:37'),(265,42,'andrea.vanessa.giraldo@gmail.com','Windows Server Administration','Installation and Configuration',4,1,'juan.otalvaro@samanagroup.co','','2024-06-20 22:20:17'),(266,42,'andrea.vanessa.giraldo@gmail.com','Windows Server Administration','Active Directory Management',3,1,'juan.otalvaro@samanagroup.co','','2024-06-20 22:20:30'),(267,42,'andrea.vanessa.giraldo@gmail.com','Windows Server Administration','Group Policy Management',1,1,'juan.otalvaro@samanagroup.co','','2024-06-20 22:20:47'),(268,42,'andrea.vanessa.giraldo@gmail.com','Windows Server Administration','DNS and DHCP Configuration',5,1,'juan.otalvaro@samanagroup.co','','2024-06-20 22:20:54'),(269,42,'andrea.vanessa.giraldo@gmail.com','Windows Server Administration','File and Storage Services',1,1,'juan.otalvaro@samanagroup.co','','2024-06-20 22:21:03'),(270,42,'andrea.vanessa.giraldo@gmail.com','Windows Server Administration','Windows Server Update Services (WSUS)',1,1,'juan.otalvaro@samanagroup.co','','2024-06-20 22:21:04'),(271,42,'andrea.vanessa.giraldo@gmail.com','Windows Server Administration','Performance Monitoring and Tuning',2,1,'juan.otalvaro@samanagroup.co','','2024-06-20 22:21:06'),(272,42,'andrea.vanessa.giraldo@gmail.com','Windows Server Administration','Backup and Restore',4,1,'juan.otalvaro@samanagroup.co','','2024-06-20 22:21:08'),(273,42,'andrea.vanessa.giraldo@gmail.com','Windows Server Administration','Remote Desktop Services (RDS)',3,1,'juan.otalvaro@samanagroup.co','','2024-06-20 22:21:17'),(274,42,'andrea.vanessa.giraldo@gmail.com','Windows Server Administration','PowerShell Scripting',2,1,'juan.otalvaro@samanagroup.co','','2024-06-20 22:21:24'),(275,42,'andrea.vanessa.giraldo@gmail.com','NetScaler','Load Balancing Configuration',4,1,'juan.otalvaro@samanagroup.co','','2024-06-20 22:21:38'),(276,42,'andrea.vanessa.giraldo@gmail.com','NetScaler','SSL Offloading',5,1,'juan.otalvaro@samanagroup.co','','2024-06-20 22:21:44'),(277,42,'andrea.vanessa.giraldo@gmail.com','NetScaler','Content Switching',5,1,'juan.otalvaro@samanagroup.co','','2024-06-20 22:21:51'),(278,42,'andrea.vanessa.giraldo@gmail.com','NetScaler','Global Server Load Balancing (GSLB)',1,1,'juan.otalvaro@samanagroup.co','','2024-06-20 22:22:05'),(280,42,'andrea.vanessa.giraldo@gmail.com','NetScaler','NetScaler Gateway Setup',1,1,'juan.otalvaro@samanagroup.co','','2024-06-20 22:22:20'),(281,42,'andrea.vanessa.giraldo@gmail.com','NetScaler','High Availability',5,1,'juan.otalvaro@samanagroup.co','','2024-06-20 22:22:24'),(282,42,'andrea.vanessa.giraldo@gmail.com','NetScaler','Networking and TCP Optimization',5,1,'juan.otalvaro@samanagroup.co','','2024-06-20 22:22:34'),(283,42,'andrea.vanessa.giraldo@gmail.com','NetScaler','Monitoring and Logging',5,1,'juan.otalvaro@samanagroup.co','','2024-06-20 22:22:38'),(285,23,'xencerra@gmail.com','Communication Skills','Verbal Communication',4,22,'danny.ruiz@samanagroup.co','','2024-06-21 15:18:40'),(286,23,'xencerra@gmail.com','Communication Skills','Nonverbal Communication',4,22,'danny.ruiz@samanagroup.co','','2024-06-21 15:18:43'),(287,23,'xencerra@gmail.com','Communication Skills','Listening Skills',4,22,'danny.ruiz@samanagroup.co','','2024-06-21 15:18:47'),(288,23,'xencerra@gmail.com','Communication Skills','Public Speaking',4,22,'danny.ruiz@samanagroup.co','','2024-06-21 15:18:51'),(289,23,'xencerra@gmail.com','Communication Skills','Emotional Intelligence',4,22,'danny.ruiz@samanagroup.co','','2024-06-21 15:18:57'),(290,23,'xencerra@gmail.com','Communication Skills','Presentation Skills',4,22,'danny.ruiz@samanagroup.co','','2024-06-21 15:19:00'),(291,23,'xencerra@gmail.com','Communication Skills','Persuasion and Influence',4,22,'danny.ruiz@samanagroup.co','','2024-06-21 15:19:04'),(292,23,'xencerra@gmail.com','Communication Skills','Conflict Resolution',4,22,'danny.ruiz@samanagroup.co','','2024-06-21 15:19:07'),(293,23,'xencerra@gmail.com','Communication Skills','Interpersonal Skills',4,22,'danny.ruiz@samanagroup.co','','2024-06-21 15:19:14'),(294,23,'xencerra@gmail.com','Communication Skills','Written Communication',4,22,'danny.ruiz@samanagroup.co','','2024-06-21 15:19:22'),(295,23,'xencerra@gmail.com','Problem Solving Skills','Analytical Thinking',4,22,'danny.ruiz@samanagroup.co','','2024-06-21 15:20:17'),(296,23,'xencerra@gmail.com','Problem Solving Skills','Creative Problem Solving',4,22,'danny.ruiz@samanagroup.co','','2024-06-21 15:20:19'),(297,23,'xencerra@gmail.com','Problem Solving Skills','Decision Making',4,22,'danny.ruiz@samanagroup.co','','2024-06-21 15:20:21'),(298,23,'xencerra@gmail.com','Problem Solving Skills','Strategic Thinking',4,22,'danny.ruiz@samanagroup.co','','2024-06-21 15:20:22'),(299,23,'xencerra@gmail.com','Problem Solving Skills','Root Cause Analysis',4,22,'danny.ruiz@samanagroup.co','','2024-06-21 15:20:25'),(300,23,'xencerra@gmail.com','Problem Solving Skills','Troubleshooting',4,22,'danny.ruiz@samanagroup.co','','2024-06-21 15:20:27'),(301,23,'xencerra@gmail.com','Problem Solving Skills','Resourcefulness',4,22,'danny.ruiz@samanagroup.co','','2024-06-21 15:20:29'),(302,23,'xencerra@gmail.com','Problem Solving Skills','Risk Management',4,22,'danny.ruiz@samanagroup.co','','2024-06-21 15:20:32'),(303,23,'xencerra@gmail.com','Problem Solving Skills','Innovative Solutions',4,22,'danny.ruiz@samanagroup.co','','2024-06-21 15:20:34'),(304,23,'xencerra@gmail.com','Problem Solving Skills','Process Improvement',4,22,'danny.ruiz@samanagroup.co','','2024-06-21 15:20:38'),(305,23,'xencerra@gmail.com','English Level','Basic Understanding',4,1,'juan.otalvaro@samanagroup.co','','2024-06-21 15:21:00'),(306,23,'xencerra@gmail.com','English Level','Conversational Fluency',4,1,'juan.otalvaro@samanagroup.co','','2024-06-21 15:21:01'),(307,23,'xencerra@gmail.com','English Level','Professional Proficiency',4,22,'danny.ruiz@samanagroup.co','','2024-06-21 15:21:03'),(308,23,'xencerra@gmail.com','English Level','Advanced Vocabulary',3,1,'juan.otalvaro@samanagroup.co','','2024-06-21 15:21:05'),(309,23,'xencerra@gmail.com','English Level','Grammar Accuracy',4,1,'juan.otalvaro@samanagroup.co','','2024-06-21 15:21:07'),(310,23,'xencerra@gmail.com','English Level','Pronunciation Clarity',4,1,'juan.otalvaro@samanagroup.co','','2024-06-21 15:21:09'),(311,23,'xencerra@gmail.com','English Level','Reading Comprehension',4,22,'danny.ruiz@samanagroup.co','','2024-06-21 15:21:25'),(312,23,'xencerra@gmail.com','English Level','Writing Skills',4,22,'danny.ruiz@samanagroup.co','','2024-06-21 15:21:27'),(313,23,'xencerra@gmail.com','English Level','Listening Comprehension',4,1,'juan.otalvaro@samanagroup.co','','2024-06-21 15:21:39'),(314,23,'xencerra@gmail.com','English Level','Public Speaking Proficiency',4,22,'danny.ruiz@samanagroup.co','','2024-06-21 15:21:42'),(315,22,'ttbass@gmail.com','Windows Server Administration','Installation and Configuration',5,1,'juan.otalvaro@samanagroup.co','','2024-06-21 18:01:50'),(316,23,'xencerra@gmail.com','Citrix Virtual Apps and Desktops','Profile Management',4,1,'juan.otalvaro@samanagroup.co','','2024-06-24 23:28:31'),(317,23,'xencerra@gmail.com','Citrix Virtual Apps and Desktops','Installation and Configuration',5,1,'juan.otalvaro@samanagroup.co','','2024-06-24 23:28:51'),(318,23,'xencerra@gmail.com','Citrix Virtual Apps and Desktops','Application Publishing',5,1,'juan.otalvaro@samanagroup.co','','2024-06-24 23:28:52'),(319,23,'xencerra@gmail.com','Citrix Virtual Apps and Desktops','StoreFront Configuration',4,1,'juan.otalvaro@samanagroup.co','','2024-06-24 23:28:54'),(320,23,'xencerra@gmail.com','Citrix Virtual Apps and Desktops','Citrix Policies',5,1,'juan.otalvaro@samanagroup.co','','2024-06-24 23:28:56');
/*!40000 ALTER TABLE `candidate_skillsets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employee_certifications`
--

DROP TABLE IF EXISTS `employee_certifications`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employee_certifications` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(255) NOT NULL,
  `certification` varchar(255) NOT NULL,
  `date` date DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=94 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employee_certifications`
--

LOCK TABLES `employee_certifications` WRITE;
/*!40000 ALTER TABLE `employee_certifications` DISABLE KEYS */;
INSERT INTO `employee_certifications` VALUES (27,'julian.gomez@samanagroup.co','AWS Certified Cloud Practitioner','2024-07-22'),(28,'julian.gomez@samanagroup.co','CCE-N Citrix Certified Expert - Networking','2024-07-22'),(29,'julian.gomez@samanagroup.co','CCA-V Citrix Certified Associate - Virtualization','2024-07-22'),(30,'julian.gomez@samanagroup.co','Citrix Certified - Citrix Workspace Microapps Service','2024-07-22'),(31,'julian.gomez@samanagroup.co','Microsoft Certified: Azure Security Engineer Associate','2024-07-22'),(32,'juan.otalvaro@samanagroup.co','CCA-N Citrix Certified Associate - Networking','2024-07-22'),(33,'juan.otalvaro@samanagroup.co','CCP-N Citrix Certified Professional - Networking','2024-07-22'),(35,'juan.otalvaro@samanagroup.co','AWS Certified Solutions Architect – Associate','2024-07-22'),(36,'juan.otalvaro@samanagroup.co','AWS Certified Security – Specialty','2024-07-22'),(43,'carlos.posada@samanagroup.co','CCE-V Citrix Certified Expert - Virtualization','2024-07-23'),(44,'carlos.posada@samanagroup.co','CompTIA A+','2024-07-23'),(45,'carlos.posada@samanagroup.co','AWS Certified Solutions Architect – Associate','2024-07-23'),(46,'alonso.santana@samanagroup.co','PMP','2024-07-25'),(47,'Moises.Blanco@samanagroup.co','AWS Certified Cloud Practitioner','2024-07-26'),(48,'Moises.Blanco@samanagroup.co','CCA-N Citrix Certified Associate - Networking','2024-07-26'),(49,'Moises.Blanco@samanagroup.co','CCP-N Citrix Certified Professional - Networking','2024-07-26'),(50,'Moises.Blanco@samanagroup.co','CCE-N Citrix Certified Expert - Networking','2024-07-26'),(51,'Moises.Blanco@samanagroup.co','CCA-AppDS - Citrix Certified Associate – App Delivery and Security','2024-07-26'),(52,'Moises.Blanco@samanagroup.co','CCA-V Citrix Certified Associate - Virtualization','2024-07-26'),(57,'alex.preczewski@samanagroup.co','Microsoft Azure AZ-104 Azure Administrator','2024-07-30'),(58,'alex.preczewski@samanagroup.co',' Microsoft Azure AZ-140 Azure Virtual Desktop Speciality','2024-07-30'),(59,'alex.preczewski@samanagroup.co','AWS Certified Solutions Architect – Associate','2024-07-30'),(60,'alex.preczewski@samanagroup.co','CCA-V Citrix Certified Associate - Virtualization','2024-07-30'),(61,'alex.preczewski@samanagroup.co','CompTIA Net+ N10-008','2024-07-30'),(62,'felipe.valencia@samanagroup.co','CCP-V Citrix Certified Professional - Virtualization','2024-07-30'),(63,'felipe.valencia@samanagroup.co','CCE-V Citrix Certified Expert - Virtualization','2024-07-30'),(64,'felipe.valencia@samanagroup.co','AWS Certified Solutions Architect – Associate','2024-07-30'),(65,'felipe.valencia@samanagroup.co','Citrix Cloud Certified - Virtual Apps and Desktops Service','2024-07-30'),(66,'felipe.valencia@samanagroup.co','CCA-V Citrix Certified Associate - Virtualization','2024-07-30'),(67,'felipe.valencia@samanagroup.co','VMware Double VPC - Data Center Virtualization & Desktop Mobility','2024-07-30'),(68,'felipe.valencia@samanagroup.co','VMWare Certified Professional - Desktop Management','2024-07-30'),(69,'felipe.valencia@samanagroup.co','VMWare Certified Professional - Data Center Virtualization','2024-07-30'),(70,'felipe.valencia@samanagroup.co','AWS Partner: Technical Accredited','2024-07-30'),(71,'felipe.valencia@samanagroup.co','ITIL v3 Foundation Certified','2024-07-30'),(72,'julian.maldonado@samanagroup.co',' Microsoft Azure AZ-140 Azure Virtual Desktop Speciality','2024-07-30'),(73,'julian.maldonado@samanagroup.co','Microsoft Azure AZ-104 Azure Administrator','2024-07-30'),(74,'julian.maldonado@samanagroup.co','CompTIA Net+ N10-008','2024-07-30'),(75,'viviana.gutierrez@samanagroup.co','Microsoft Azure AZ-104 Azure Administrator','2024-07-30'),(76,'viviana.gutierrez@samanagroup.co','CompTIA Net+ N10-008','2024-07-30'),(77,'jorge.rodriguez@samanagroup.co','Microsoft Azure AZ-104 Azure Administrator','2024-07-30'),(78,'jorge.rodriguez@samanagroup.co','CompTIA Net+ N10-008','2024-07-30'),(79,'cesar.garcia@samanagroup.co','Microsoft Azure AZ-305 Azure Architect','2024-07-30'),(80,'cesar.garcia@samanagroup.co','Microsoft Azure AZ-104 Azure Administrator','2024-07-30'),(81,'cesar.garcia@samanagroup.co','AWS Certified Solutions Architect – Associate','2024-07-30'),(82,'danny.ruiz@samanagroup.co','AWS Certified Cloud Practitioner','2024-07-30'),(83,'viviana.gutierrez@samanagroup.co','CCE-V Citrix Certified Expert - Virtualization','2024-07-30'),(84,'danny.ruiz@samanagroup.co','Microsoft Azure AZ-900 Azure Fundamentals','2024-07-30'),(85,'danny.ruiz@samanagroup.co','CCA-V Citrix Certified Associate - Virtualization','2024-07-30'),(86,'jonathan.piedrahita@samanagroup.co','CCA-V Citrix Certified Associate - Virtualization','2024-07-30'),(87,'jonathan.piedrahita@samanagroup.co','Microsoft Azure AZ-104 Azure Administrator','2024-07-30'),(88,'jonathan.piedrahita@samanagroup.co','CompTIA Net+ N10-008','2024-07-30'),(89,'carlos.posada@samanagroup.co','Microsoft Azure AZ-104 Azure Administrator','2024-07-30'),(90,'alonso.santana@samanagroup.co','AWS Certified Cloud Practitioner','2024-07-30'),(91,'german.toro@samanagroup.co','Microsoft Azure AZ-800 Windows Hybrid ','2024-07-30'),(92,'german.toro@samanagroup.co','CCA-V Citrix Certified Associate - Virtualization','2024-07-30');
/*!40000 ALTER TABLE `employee_certifications` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employee_enrollment`
--

DROP TABLE IF EXISTS `employee_enrollment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employee_enrollment` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(255) NOT NULL,
  `step` int NOT NULL,
  `value` int NOT NULL,
  `date` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`,`step`)
) ENGINE=InnoDB AUTO_INCREMENT=229 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employee_enrollment`
--

LOCK TABLES `employee_enrollment` WRITE;
/*!40000 ALTER TABLE `employee_enrollment` DISABLE KEYS */;
INSERT INTO `employee_enrollment` VALUES (1,'alex.preczewski@samanagroup.co',1,1,'2024-08-06 18:09:13'),(4,'alex.preczewski@samanagroup.co',2,1,'2024-08-06 18:09:20'),(5,'alex.preczewski@samanagroup.co',3,1,'2024-08-06 18:09:23'),(6,'alex.preczewski@samanagroup.co',4,1,'2024-08-06 18:09:28'),(7,'alex.preczewski@samanagroup.co',5,1,'2024-08-06 18:10:03'),(8,'alex.preczewski@samanagroup.co',6,1,'2024-08-06 18:10:05'),(14,'alex.preczewski@samanagroup.co',7,1,'2024-08-06 18:12:52'),(15,'alex.preczewski@samanagroup.co',8,1,'2024-08-06 18:12:59'),(16,'alex.preczewski@samanagroup.co',9,1,'2024-08-06 18:13:30'),(17,'alex.preczewski@samanagroup.co',13,1,'2024-08-06 18:13:50'),(18,'alex.preczewski@samanagroup.co',12,1,'2024-08-06 18:13:54'),(19,'alex.preczewski@samanagroup.co',11,1,'2024-08-06 18:13:57'),(20,'alex.preczewski@samanagroup.co',10,1,'2024-08-06 18:14:00'),(45,'alonso.santana@samanagroup.co',1,1,'2024-08-06 23:57:37'),(46,'alonso.santana@samanagroup.co',2,1,'2024-08-06 23:57:38'),(47,'alonso.santana@samanagroup.co',3,1,'2024-08-06 23:57:41'),(48,'alonso.santana@samanagroup.co',4,1,'2024-08-06 23:57:42'),(49,'alonso.santana@samanagroup.co',5,1,'2024-08-06 23:57:44'),(50,'alonso.santana@samanagroup.co',6,1,'2024-08-06 23:57:46'),(51,'alonso.santana@samanagroup.co',7,1,'2024-08-06 23:57:48'),(52,'alonso.santana@samanagroup.co',8,1,'2024-08-06 23:57:50'),(53,'alonso.santana@samanagroup.co',9,1,'2024-08-06 23:57:52'),(54,'alonso.santana@samanagroup.co',10,1,'2024-08-06 23:57:54'),(55,'alonso.santana@samanagroup.co',11,1,'2024-08-06 23:57:56'),(56,'alonso.santana@samanagroup.co',12,1,'2024-08-06 23:57:58'),(57,'alonso.santana@samanagroup.co',13,1,'2024-08-06 23:58:00'),(58,'andres.cubas@samanagroup.co',1,1,'2024-08-06 23:58:38'),(59,'andres.cubas@samanagroup.co',2,1,'2024-08-06 23:58:40'),(60,'andres.cubas@samanagroup.co',3,1,'2024-08-06 23:58:43'),(61,'andres.cubas@samanagroup.co',4,1,'2024-08-06 23:58:45'),(62,'andres.cubas@samanagroup.co',5,1,'2024-08-06 23:58:46'),(63,'andres.cubas@samanagroup.co',6,1,'2024-08-06 23:58:48'),(64,'andres.cubas@samanagroup.co',7,1,'2024-08-06 23:58:50'),(65,'andres.cubas@samanagroup.co',8,1,'2024-08-06 23:58:53'),(66,'andres.cubas@samanagroup.co',9,1,'2024-08-06 23:58:55'),(67,'andres.cubas@samanagroup.co',10,1,'2024-08-06 23:58:57'),(68,'andres.cubas@samanagroup.co',11,1,'2024-08-06 23:58:58'),(69,'andres.cubas@samanagroup.co',12,1,'2024-08-06 23:59:00'),(70,'andres.cubas@samanagroup.co',13,1,'2024-08-06 23:59:02'),(71,'carlos.posada@samanagroup.co',1,1,'2024-08-07 00:07:39'),(72,'carlos.posada@samanagroup.co',2,1,'2024-08-07 00:08:02'),(75,'carlos.posada@samanagroup.co',3,1,'2024-08-07 00:29:17'),(76,'carlos.posada@samanagroup.co',4,1,'2024-08-07 00:29:20'),(77,'carlos.posada@samanagroup.co',5,1,'2024-08-07 00:29:22'),(78,'carlos.posada@samanagroup.co',7,1,'2024-08-07 00:29:29'),(79,'cesar.garcia@samanagroup.co',1,1,'2024-08-07 00:39:45'),(80,'cesar.garcia@samanagroup.co',2,1,'2024-08-07 00:39:48'),(81,'cesar.garcia@samanagroup.co',3,1,'2024-08-07 00:39:53'),(82,'cesar.garcia@samanagroup.co',4,1,'2024-08-07 00:39:58'),(83,'cesar.garcia@samanagroup.co',5,1,'2024-08-07 00:40:06'),(84,'cesar.garcia@samanagroup.co',6,1,'2024-08-07 00:40:08'),(85,'cesar.garcia@samanagroup.co',7,1,'2024-08-07 00:40:12'),(86,'cesar.garcia@samanagroup.co',8,1,'2024-08-07 00:40:15'),(87,'cesar.garcia@samanagroup.co',9,1,'2024-08-07 00:40:18'),(88,'cesar.garcia@samanagroup.co',10,1,'2024-08-07 00:40:22'),(89,'cesar.garcia@samanagroup.co',11,1,'2024-08-07 00:40:27'),(90,'cesar.garcia@samanagroup.co',12,1,'2024-08-07 00:40:29'),(91,'cesar.garcia@samanagroup.co',13,1,'2024-08-07 00:40:32'),(92,'cristhian.ramos@samanagroup.co',1,1,'2024-08-07 00:42:15'),(93,'cristhian.ramos@samanagroup.co',2,1,'2024-08-07 00:42:19'),(94,'cristhian.ramos@samanagroup.co',3,1,'2024-08-07 00:42:23'),(95,'cristhian.ramos@samanagroup.co',4,1,'2024-08-07 00:42:26'),(96,'cristhian.ramos@samanagroup.co',5,1,'2024-08-07 00:42:28'),(97,'cristhian.ramos@samanagroup.co',6,1,'2024-08-07 00:42:30'),(98,'cristhian.ramos@samanagroup.co',7,1,'2024-08-07 00:42:33'),(99,'cristhian.ramos@samanagroup.co',8,1,'2024-08-07 00:42:35'),(100,'cristhian.ramos@samanagroup.co',9,1,'2024-08-07 00:42:37'),(101,'cristhian.ramos@samanagroup.co',10,1,'2024-08-07 00:42:39'),(102,'cristhian.ramos@samanagroup.co',11,1,'2024-08-07 00:42:41'),(103,'cristhian.ramos@samanagroup.co',12,1,'2024-08-07 00:42:43'),(104,'cristhian.ramos@samanagroup.co',13,1,'2024-08-07 00:42:47'),(105,'danny.ruiz@samanagroup.co',1,1,'2024-08-07 00:45:49'),(106,'danny.ruiz@samanagroup.co',2,1,'2024-08-07 00:45:54'),(107,'danny.ruiz@samanagroup.co',3,1,'2024-08-07 00:45:58'),(108,'danny.ruiz@samanagroup.co',4,1,'2024-08-07 00:46:01'),(109,'danny.ruiz@samanagroup.co',5,1,'2024-08-07 00:46:03'),(110,'danny.ruiz@samanagroup.co',6,1,'2024-08-07 00:46:05'),(111,'danny.ruiz@samanagroup.co',7,1,'2024-08-07 00:46:08'),(112,'danny.ruiz@samanagroup.co',8,1,'2024-08-07 00:46:11'),(113,'danny.ruiz@samanagroup.co',9,1,'2024-08-07 00:46:12'),(114,'danny.ruiz@samanagroup.co',10,1,'2024-08-07 00:46:15'),(115,'danny.ruiz@samanagroup.co',11,1,'2024-08-07 00:46:16'),(116,'danny.ruiz@samanagroup.co',12,1,'2024-08-07 00:46:18'),(117,'danny.ruiz@samanagroup.co',13,1,'2024-08-07 00:46:20'),(118,'carlos.posada@samanagroup.co',6,1,'2024-08-07 00:50:20'),(119,'carlos.posada@samanagroup.co',8,1,'2024-08-07 00:50:25'),(120,'carlos.posada@samanagroup.co',9,1,'2024-08-07 00:50:27'),(121,'carlos.posada@samanagroup.co',10,1,'2024-08-07 00:50:29'),(122,'carlos.posada@samanagroup.co',11,1,'2024-08-07 00:50:30'),(123,'carlos.posada@samanagroup.co',12,1,'2024-08-07 00:50:33'),(124,'carlos.posada@samanagroup.co',13,1,'2024-08-07 00:50:35'),(125,'Moises.Blanco@samanagroup.co',1,1,'2024-08-07 00:54:43'),(126,'Moises.Blanco@samanagroup.co',2,1,'2024-08-07 00:54:46'),(127,'juan.otalvaro@samanagroup.co',1,1,'2024-08-07 17:20:54'),(128,'juan.otalvaro@samanagroup.co',2,1,'2024-08-07 17:20:57'),(129,'juan.otalvaro@samanagroup.co',3,1,'2024-08-07 17:20:59'),(130,'juan.otalvaro@samanagroup.co',4,1,'2024-08-07 17:21:01'),(131,'juan.otalvaro@samanagroup.co',5,1,'2024-08-07 17:21:03'),(132,'juan.otalvaro@samanagroup.co',6,1,'2024-08-07 17:21:05'),(133,'juan.otalvaro@samanagroup.co',7,1,'2024-08-07 17:21:07'),(134,'juan.otalvaro@samanagroup.co',8,1,'2024-08-07 17:21:09'),(135,'juan.otalvaro@samanagroup.co',9,1,'2024-08-07 17:21:10'),(136,'juan.otalvaro@samanagroup.co',10,1,'2024-08-07 17:21:12'),(137,'juan.otalvaro@samanagroup.co',11,1,'2024-08-07 17:21:13'),(138,'juan.otalvaro@samanagroup.co',12,1,'2024-08-07 17:21:15'),(139,'juan.otalvaro@samanagroup.co',13,1,'2024-08-07 17:21:17'),(140,'Moises.Blanco@samanagroup.co',3,1,'2024-08-07 18:05:56'),(141,'Moises.Blanco@samanagroup.co',4,1,'2024-08-07 18:05:58'),(142,'Moises.Blanco@samanagroup.co',5,1,'2024-08-07 18:05:59'),(143,'Moises.Blanco@samanagroup.co',6,1,'2024-08-07 18:06:01'),(144,'Moises.Blanco@samanagroup.co',7,1,'2024-08-07 18:06:03'),(145,'Moises.Blanco@samanagroup.co',8,1,'2024-08-07 18:06:06'),(146,'Moises.Blanco@samanagroup.co',9,1,'2024-08-07 18:06:08'),(147,'Moises.Blanco@samanagroup.co',10,1,'2024-08-07 18:06:09'),(148,'Moises.Blanco@samanagroup.co',11,1,'2024-08-07 18:06:11'),(149,'Moises.Blanco@samanagroup.co',12,1,'2024-08-07 18:06:12'),(150,'Moises.Blanco@samanagroup.co',13,1,'2024-08-07 18:06:14'),(151,'viviana.gutierrez@samanagroup.co',1,1,'2024-08-07 18:06:31'),(152,'viviana.gutierrez@samanagroup.co',2,1,'2024-08-07 18:06:32'),(153,'viviana.gutierrez@samanagroup.co',3,1,'2024-08-07 18:06:35'),(154,'viviana.gutierrez@samanagroup.co',4,1,'2024-08-07 18:06:36'),(155,'viviana.gutierrez@samanagroup.co',5,1,'2024-08-07 18:06:38'),(156,'viviana.gutierrez@samanagroup.co',6,1,'2024-08-07 18:06:40'),(157,'viviana.gutierrez@samanagroup.co',7,1,'2024-08-07 18:06:42'),(158,'viviana.gutierrez@samanagroup.co',8,1,'2024-08-07 18:06:44'),(159,'viviana.gutierrez@samanagroup.co',9,1,'2024-08-07 18:06:46'),(160,'viviana.gutierrez@samanagroup.co',10,1,'2024-08-07 18:06:47'),(161,'viviana.gutierrez@samanagroup.co',11,1,'2024-08-07 18:06:49'),(162,'viviana.gutierrez@samanagroup.co',12,1,'2024-08-07 18:06:50'),(163,'viviana.gutierrez@samanagroup.co',13,1,'2024-08-07 18:06:53'),(164,'jorge.rodriguez@samanagroup.co',1,1,'2024-08-07 18:07:23'),(165,'jorge.rodriguez@samanagroup.co',2,1,'2024-08-07 18:07:26'),(166,'jorge.rodriguez@samanagroup.co',3,1,'2024-08-07 18:07:29'),(167,'jorge.rodriguez@samanagroup.co',4,1,'2024-08-07 18:07:31'),(168,'jorge.rodriguez@samanagroup.co',5,1,'2024-08-07 18:07:32'),(169,'jorge.rodriguez@samanagroup.co',6,1,'2024-08-07 18:07:34'),(170,'jorge.rodriguez@samanagroup.co',7,1,'2024-08-07 18:07:36'),(171,'jorge.rodriguez@samanagroup.co',8,1,'2024-08-07 18:07:39'),(172,'jorge.rodriguez@samanagroup.co',9,1,'2024-08-07 18:07:41'),(173,'jorge.rodriguez@samanagroup.co',10,1,'2024-08-07 18:07:43'),(174,'jorge.rodriguez@samanagroup.co',11,1,'2024-08-07 18:07:44'),(175,'jorge.rodriguez@samanagroup.co',12,1,'2024-08-07 18:07:46'),(176,'jorge.rodriguez@samanagroup.co',13,1,'2024-08-07 18:07:48'),(177,'felipe.bernal@samanagroup.co',1,1,'2024-08-07 18:35:50'),(178,'felipe.bernal@samanagroup.co',2,1,'2024-08-07 18:35:52'),(179,'felipe.bernal@samanagroup.co',3,1,'2024-08-07 18:35:55'),(180,'felipe.bernal@samanagroup.co',4,1,'2024-08-07 18:35:56'),(181,'felipe.bernal@samanagroup.co',5,1,'2024-08-07 18:35:58'),(182,'felipe.bernal@samanagroup.co',6,1,'2024-08-07 18:36:00'),(183,'felipe.bernal@samanagroup.co',7,1,'2024-08-07 18:36:02'),(184,'felipe.bernal@samanagroup.co',8,1,'2024-08-07 18:36:05'),(185,'felipe.bernal@samanagroup.co',9,1,'2024-08-07 18:36:07'),(186,'felipe.bernal@samanagroup.co',10,1,'2024-08-07 18:36:08'),(187,'felipe.bernal@samanagroup.co',11,1,'2024-08-07 18:36:09'),(188,'felipe.bernal@samanagroup.co',12,1,'2024-08-07 18:36:12'),(189,'felipe.bernal@samanagroup.co',13,1,'2024-08-07 18:36:14'),(190,'felipe.valencia@samanagroup.co',1,1,'2024-08-07 18:36:28'),(191,'felipe.valencia@samanagroup.co',2,1,'2024-08-07 18:36:30'),(192,'felipe.valencia@samanagroup.co',3,1,'2024-08-07 18:36:33'),(193,'felipe.valencia@samanagroup.co',4,1,'2024-08-07 18:36:34'),(194,'felipe.valencia@samanagroup.co',5,1,'2024-08-07 18:36:36'),(195,'felipe.valencia@samanagroup.co',6,1,'2024-08-07 18:36:37'),(196,'felipe.valencia@samanagroup.co',7,1,'2024-08-07 18:36:40'),(197,'felipe.valencia@samanagroup.co',8,1,'2024-08-07 18:36:42'),(198,'felipe.valencia@samanagroup.co',9,1,'2024-08-07 18:36:43'),(199,'felipe.valencia@samanagroup.co',10,1,'2024-08-07 18:36:45'),(200,'felipe.valencia@samanagroup.co',11,1,'2024-08-07 18:36:47'),(201,'felipe.valencia@samanagroup.co',12,1,'2024-08-07 18:36:48'),(202,'felipe.valencia@samanagroup.co',13,1,'2024-08-07 18:36:54'),(203,'fernando.marin@samanagroup.co',1,1,'2024-08-07 20:42:52'),(204,'fernando.marin@samanagroup.co',2,1,'2024-08-07 20:42:54'),(205,'fernando.marin@samanagroup.co',3,1,'2024-08-07 20:42:56'),(206,'fernando.marin@samanagroup.co',4,1,'2024-08-07 20:42:57'),(207,'fernando.marin@samanagroup.co',5,1,'2024-08-07 20:42:58'),(208,'fernando.marin@samanagroup.co',6,1,'2024-08-07 20:43:00'),(209,'fernando.marin@samanagroup.co',7,1,'2024-08-07 20:43:03'),(210,'fernando.marin@samanagroup.co',8,1,'2024-08-07 20:43:06'),(211,'fernando.marin@samanagroup.co',9,1,'2024-08-07 20:43:07'),(212,'fernando.marin@samanagroup.co',10,1,'2024-08-07 20:43:09'),(213,'fernando.marin@samanagroup.co',11,1,'2024-08-07 20:43:10'),(214,'fernando.marin@samanagroup.co',12,1,'2024-08-07 20:43:12'),(215,'fernando.marin@samanagroup.co',13,1,'2024-08-07 20:43:14'),(216,'julian.maldonado@samanagroup.co',1,1,'2024-08-07 20:43:29'),(217,'julian.maldonado@samanagroup.co',2,1,'2024-08-07 20:43:31'),(218,'julian.maldonado@samanagroup.co',3,1,'2024-08-07 20:43:33'),(219,'julian.maldonado@samanagroup.co',4,1,'2024-08-07 20:43:35'),(220,'julian.maldonado@samanagroup.co',5,1,'2024-08-07 20:43:37'),(221,'julian.maldonado@samanagroup.co',6,1,'2024-08-07 20:43:39'),(222,'julian.maldonado@samanagroup.co',7,1,'2024-08-07 20:43:42'),(223,'julian.maldonado@samanagroup.co',8,1,'2024-08-07 20:43:44'),(224,'julian.maldonado@samanagroup.co',9,1,'2024-08-07 20:43:46'),(225,'julian.maldonado@samanagroup.co',10,1,'2024-08-07 20:43:48'),(226,'julian.maldonado@samanagroup.co',11,1,'2024-08-07 20:43:50'),(227,'julian.maldonado@samanagroup.co',12,1,'2024-08-07 20:43:51'),(228,'julian.maldonado@samanagroup.co',13,1,'2024-08-07 20:43:53');
/*!40000 ALTER TABLE `employee_enrollment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employee_profiles`
--

DROP TABLE IF EXISTS `employee_profiles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employee_profiles` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `primaryEmail` text NOT NULL,
  `recoveryEmail` text,
  `fullName` text NOT NULL,
  `phone_mobile` text,
  `thumbnailPhotoURL` text,
  `companyRole` text,
  `contractType` text,
  `suspended` text NOT NULL,
  `creationDate` date NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employee_profiles`
--

LOCK TABLES `employee_profiles` WRITE;
/*!40000 ALTER TABLE `employee_profiles` DISABLE KEYS */;
INSERT INTO `employee_profiles` VALUES (1,'alex.preczewski@samanagroup.co','alex.preczewski@gmail.com','Alex Preczewski','12345678901','https://lh3.googleusercontent.com/a-/ALV-UjV5bkP391y7a8OIJ4-lg3Yy8hnAvKhwvTUwtIrwnXuZMNGlQ-Q=s96-c','L3 - Service Desk Engineer','Full Time','False','2020-03-31'),(2,'alonso.santana@samanagroup.co','alonsosantanat92@gmail.com','Alonso Maury Santana Torres',NULL,'https://lh3.googleusercontent.com/a-/ALV-UjWs_CBWx-xl41MSdJkxwFYIajO6Kc8HJtMdsVj-0TIbiT6Q_ZM=s96-c','SDM','Full Time','False','2022-08-01'),(3,'andres.cubas@samanagroup.co','andresmcubas@gmail.com','Andres Cubas',NULL,NULL,'andresc@samana.local',NULL,'False','2020-07-01'),(4,'andres.monroy@samanagroup.co','tech.andresmonroy@gmail.com','Andres Mauricio Monroy Sicuariza',NULL,NULL,'L1 - Service Desk Engineer','Full Time','False','2023-01-16'),(5,'carlos.posada@samanagroup.co','carlosaposadac@outlook.com','Carlos Posada','+57-300-472-1380','https://lh3.googleusercontent.com/a-/ALV-UjV-r1iEDCJwgDoiJhWWKHko6SSQ3hxsEHZ6WIL0cNOY6z8Qlu8=s96-c','L3 - Service Desk Engineer','Full Time','False','2016-01-14'),(6,'cesar.garcia@samanagroup.co','cesaregarciam@gmail.com','Cesar Garcia',NULL,NULL,'Enterprise Architect','Full Time','False','2022-08-04'),(7,'cristhian.ramos@samanagroup.co','cristhian.ligio@gmail.com','Cristhian Camilo Ramos Ligio','+57-305-817-2566','https://lh3.googleusercontent.com/a-/ALV-UjXCvsiRTy6GI-KLkEMKYeZ0GVH2Uh2_S5fYmKHhz3x8q_UNq8NJ=s96-c','L2 - Service Desk Engineer','Full Time','False','2019-01-24'),(8,'daniel.linero@samanagroup.co','daniellinerohd@gmail.com','Daniel Alfredo Linero Vassallo',NULL,'https://lh3.googleusercontent.com/a-/ALV-UjWaLvieLgXp25DGDRGhpskrnhZDh1wMfv5SfHAlOEBephkAQCY=s96-c','L1 - Service Desk Engineer','Full Time','False','2024-05-20'),(9,'daniel.monsalve@samanagroup.co',NULL,'Daniel Felipe Monsalve Diaz',NULL,NULL,'L1 - Service Desk Engineer','Full Time','True','2024-04-01'),(10,'daniel.sanchez@samanagroup.co',NULL,'Daniel Sanchez Vasquez',NULL,NULL,'L1 - Service Desk Engineer','Full Time','True','2023-05-29'),(11,'danny.ruiz@samanagroup.co','dannyrupico@gmail.com','Danny Jose Ruiz Pico',NULL,'https://lh3.googleusercontent.com/a-/ALV-UjX7iu2qUHpeVC4g_sX-6jeHHLGHzw11WvDH3laQTPfy50uF0GW1=s96-c','SDM','Full Time','False','2022-03-22'),(12,'fabian.baena@samanagroup.co','fabbaena@gmail.com','Fabian Baena','+1786-385-6106','https://lh3.googleusercontent.com/a-/ALV-UjURGZQ8Sqyv2zD7e-OnGbxoUp_Rv6r1_0nb0DjHZNFDFV1PvONl=s96-c','CTO','owner','False','2012-05-09'),(13,'felipe.bernal@samanagroup.co','fbernalbarca@gmail.com','Felipe Bernal','+1-954-937-2592','https://lh3.googleusercontent.com/a-/ALV-UjU9jHZd3TahivAbonZ0I7x51W_8GBAwp1k2MXszyWUIQqFQrH0=s96-c','Service Delivery Director','Full Time','False','2018-10-15'),(14,'felipe.valencia@samanagroup.co',NULL,'Felipe Valencia','+57-311-561-5919',NULL,'Senior Consultant','Full Time','False','2016-03-28'),(15,'fernando.marin@samanagroup.co',NULL,'Fernando Marin','+57-310-769-0653','https://lh3.googleusercontent.com/a-/ALV-UjWD0deQ8zy72nH4jpWkPsDkNS2Xx27kfuRo8q7xYhQxfq0s07bM=s96-c','CFO','Full Time','False','2020-05-18'),(16,'german.toro@samanagroup.co','bgermanch@gmail.com','German Toro','+57-313-626-5284','https://lh3.googleusercontent.com/a-/ALV-UjUQCUXK2eM1ISdrXSmkEBEjswY_ufNv6W_xcM469h6WVtom_r4=s96-c','L2 - Service Desk Engineer','Full Time','False','2021-07-19'),(17,'Gonzalo.Rodriguez@samanagroup.co',NULL,'Gonzalo Rodriguez','+52-1-55-3561-8668','https://lh3.googleusercontent.com/a-/ALV-UjW7T3frcRNywFSzAreSUeBrwCX4y6ICSLqbcNd2mXqtBqiA50vx=s96-c','Consultant','Contractor','True','2013-03-08'),(19,'jair.becerra@samanagroup.com','xencerra@gmail.com','Jair Becerra Espinosa',NULL,NULL,'L3 - Service Desk Engineer','Full Time','False','2024-07-10'),(20,'jair.reyes@samanagroup.com','flink8711@hotmail.com','Jair Reyes','+57-322-700-0369',NULL,'L1 - Service Desk Engineer','Full Time','False','2021-03-11'),(21,'jonathan.piedrahita@samanagroup.co','jonathanpg3681@gmail.com','Jonathan Piedrahita','+1-469-602-1602','https://lh3.googleusercontent.com/a-/ALV-UjVr073dymkrkPRCYWg6GCpmqpGAiIbsMA0y8RBGkklqe1-0du4=s96-c','L3 - Service Desk Engineer','Full Time','True','2018-07-06'),(22,'Jorge.Gomez@samanagroup.co',NULL,'Jorge Gomez',NULL,'https://lh3.googleusercontent.com/a-/ALV-UjXiE3Kffg6S1ySSBWBmLtazYm_8jf4xIuu2GtvKB6OkSIp0mWM=s96-c','CEO','Owner','False','2012-05-09'),(23,'jorge.rodriguez@samanagroup.co',NULL,'Jorge Rodriguez','+33-76-788-8412',NULL,'L2 - Service Desk Engineer','Full Time','False','2022-02-28'),(24,'jose.curi@samanagroup.co',NULL,'Jose Curi',NULL,'https://lh3.googleusercontent.com/a-/ALV-UjWGp9usEuMP1ZdPCXaFi0SxtAXx0ol0mbUkGmWbsmWjUoH6XDQ=s96-c','Consultant','Contractor','False','2022-03-16'),(25,'juan.otalvaro@samanagroup.co','otalvaroj@gmail.com','Juan Pablo Otalvaro A','+57 313 806 0576','https://lh3.googleusercontent.com/a/ACg8ocJ63PiVOvjMOWzDg1Dq5DO0uxODftn7tmwUD5mj4DoJH4m3B2U=s96-c','Enterprise Architect','Full Time','False','2020-01-22'),(26,'juan.vega@samanagroup.co',NULL,'Juan Daniel Vega Bustos',NULL,NULL,'L1 - Service Desk Engineer','Full Time','False','2023-05-01'),(27,'julian.gomez@samanagroup.co','juliangomezr@gmail.com','Julian Gomez','+57-317-665-3505',NULL,'SDM','Full Time','False','2017-03-29'),(28,'julian.maldonado@samanagroup.co',NULL,'Julian David Maldonado Ramos','+57-304-491-0424',NULL,'L2 - Service Desk Engineer','Full Time','False','2019-01-24'),(29,'juliano.reckziegel@samanagroup.co','julianor@geniusconsulting.net','Juliano Reckziegel',NULL,NULL,'Consultant','Contractor','False','2024-06-06'),(30,'luiz.szente@samanagroup.co','l.szente@uol.com.br','Luiz Szente','+55-11-97173-4031','https://lh3.googleusercontent.com/a-/ALV-UjUtxByfT6VzznoMW6BIAVkP7aOTFeBDHvgyJCJ-Du8KQ4cQlRk=s96-c','SRM','Full Time','False','2018-06-05'),(31,'marcela.matos@samanagroup.co',NULL,'Marcela Matos Lasprilla',NULL,'https://lh3.googleusercontent.com/a-/ALV-UjX5LbZaY24J5pTrmNW_OQfiXIGR3tIxTKgY0MG3rSs9HC-DwQ=s96-c','L1 - Service Desk Engineer','Full Time','False','2024-02-21'),(32,'marcelo.schultheis@samanagroup.co','marcelo.schultheis@gmail.com','Marcelo Schultheis','+54-9-3436-45-3549',NULL,'Consultant','Contractor','False','2016-03-02'),(33,'mauricio.llano@samanagroup.co','mllano@hotmail.com','Mauricio Llano Lopez',NULL,'https://lh3.googleusercontent.com/a-/ALV-UjUZVncqA8VyZMUaevgYAoON8tDKyn4iIM0Jg99FjQ294Jg_lu8=s96-c','L1 - Service Desk Engineer','Full Time','False','2023-11-23'),(34,'miguel.ayala@samanagroup.co',NULL,'Miguel Geronimo Ayala Paez',NULL,NULL,'L1 - Service Desk Engineer','Full Time','False','2023-12-18'),(35,'Moises.Blanco@samanagroup.co','m_blanco_81@yahoo.com','Moises Blanco','+57-300-814-3276','https://lh3.google.com/ao/AHP4FtlBZrBx8Jli6PV9A4q9t2ta-6H3n-oJeDUr10pTfhiIxPlCOdHKEmVZB0iKNkOPTw1qwos=s96-c','SDM','Full Time','False','2013-05-10'),(36,'nicolas.alfaro@samanagroup.co',NULL,'Nicolas Alfaro Fonseca',NULL,NULL,'SRM','Full Time','True','2023-05-05'),(37,'nicolas.becerra@samanagroup.co',NULL,'Nicolas Becerra Gomez',NULL,NULL,'L1 - Service Desk Engineer','Full Time','False','2024-05-20'),(39,'siddarth.gopinath@samanagroup.com',NULL,'Siddarth Gopinath',NULL,NULL,'L2 - Service Desk Engineer','Full Time','False','2024-07-11'),(41,'viviana.gutierrez@samanagroup.co',NULL,'Viviana Gutierrez','+57-350-842-7992',NULL,'L2 - Service Desk Engineer','Full Time','False','2019-11-07');
/*!40000 ALTER TABLE `employee_profiles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employee_reviews`
--

DROP TABLE IF EXISTS `employee_reviews`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employee_reviews` (
  `id` int NOT NULL AUTO_INCREMENT,
  `employee_id` int DEFAULT NULL,
  `email` varchar(255) NOT NULL,
  `evaluation_field` varchar(255) NOT NULL,
  `rating` int DEFAULT NULL,
  `reviewer_email` varchar(255) NOT NULL,
  `observations` varchar(255) NOT NULL,
  `public` text,
  `date` date DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employee_reviews`
--

LOCK TABLES `employee_reviews` WRITE;
/*!40000 ALTER TABLE `employee_reviews` DISABLE KEYS */;
INSERT INTO `employee_reviews` VALUES (1,1,'alex.preczewski@samanagroup.co','Certification Goals',5,'juan.otalvaro@samanagroup.co','test1','YES','2024-08-07'),(2,1,'alex.preczewski@samanagroup.co','HR Evaluation',3,'juan.otalvaro@samanagroup.co','test2','NO','2024-08-07');
/*!40000 ALTER TABLE `employee_reviews` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employee_skillsets`
--

DROP TABLE IF EXISTS `employee_skillsets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employee_skillsets` (
  `id` int NOT NULL AUTO_INCREMENT,
  `employee_id` int DEFAULT NULL,
  `email` varchar(255) NOT NULL,
  `category` varchar(255) NOT NULL,
  `skillset` varchar(255) NOT NULL,
  `rating` int DEFAULT NULL,
  `reviewer_email` varchar(255) NOT NULL,
  `date` date DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employee_skillsets`
--

LOCK TABLES `employee_skillsets` WRITE;
/*!40000 ALTER TABLE `employee_skillsets` DISABLE KEYS */;
INSERT INTO `employee_skillsets` VALUES (10,2,'alonso.santana@samanagroup.co','AWS','EC2 Management',5,'juan.otalvaro@samanagroup.co','2024-07-24'),(11,2,'alonso.santana@samanagroup.co','AWS','S3 Storage Solutions',3,'juan.otalvaro@samanagroup.co','2024-07-25'),(12,2,'alonso.santana@samanagroup.co','AWS','VPC Configuration',4,'juan.otalvaro@samanagroup.co','2024-07-25'),(13,2,'alonso.santana@samanagroup.co','AWS','IAM Policies and Roles',3,'juan.otalvaro@samanagroup.co','2024-07-25'),(14,3,'andres.cubas@samanagroup.co','AWS','EC2 Management',5,'juan.otalvaro@samanagroup.co','2024-07-25'),(15,3,'andres.cubas@samanagroup.co','AWS','S3 Storage Solutions',4,'juan.otalvaro@samanagroup.co','2024-07-25'),(16,3,'andres.cubas@samanagroup.co','AWS','VPC Configuration',5,'juan.otalvaro@samanagroup.co','2024-07-25'),(17,3,'andres.cubas@samanagroup.co','AWS','IAM Policies and Roles',3,'juan.otalvaro@samanagroup.co','2024-07-25'),(18,3,'andres.cubas@samanagroup.co','NetScaler','Load Balancing Configuration',5,'juan.otalvaro@samanagroup.co','2024-07-25'),(19,3,'andres.cubas@samanagroup.co','NetScaler','SSL Offloading',4,'juan.otalvaro@samanagroup.co','2024-07-25'),(22,35,'Moises.Blanco@samanagroup.co','NetScaler','Load Balancing Configuration',5,'juan.otalvaro@samanagroup.co','2024-07-26'),(23,35,'Moises.Blanco@samanagroup.co','NetScaler','SSL Offloading',5,'juan.otalvaro@samanagroup.co','2024-07-26'),(24,35,'Moises.Blanco@samanagroup.co','NetScaler','Content Switching',5,'juan.otalvaro@samanagroup.co','2024-07-26'),(25,35,'Moises.Blanco@samanagroup.co','NetScaler','Global Server Load Balancing (GSLB)',5,'juan.otalvaro@samanagroup.co','2024-07-26'),(26,35,'Moises.Blanco@samanagroup.co','NetScaler','Application Firewall Configuration',5,'juan.otalvaro@samanagroup.co','2024-07-26'),(27,35,'Moises.Blanco@samanagroup.co','NetScaler','NetScaler Gateway Setup',5,'juan.otalvaro@samanagroup.co','2024-07-26'),(28,35,'Moises.Blanco@samanagroup.co','NetScaler','High Availability',5,'juan.otalvaro@samanagroup.co','2024-07-26'),(29,35,'Moises.Blanco@samanagroup.co','NetScaler','Networking and TCP Optimization',5,'juan.otalvaro@samanagroup.co','2024-07-26'),(30,35,'Moises.Blanco@samanagroup.co','NetScaler','Monitoring and Logging',5,'juan.otalvaro@samanagroup.co','2024-07-26'),(31,35,'Moises.Blanco@samanagroup.co','NetScaler','Authentication, Authorization, and Auditing (AAA)',5,'juan.otalvaro@samanagroup.co','2024-07-26');
/*!40000 ALTER TABLE `employee_skillsets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `job_categories`
--

DROP TABLE IF EXISTS `job_categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `job_categories` (
  `id` int NOT NULL AUTO_INCREMENT,
  `category_name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=47 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `job_categories`
--

LOCK TABLES `job_categories` WRITE;
/*!40000 ALTER TABLE `job_categories` DISABLE KEYS */;
INSERT INTO `job_categories` VALUES (1,'Citrix Virtual Apps and Desktops'),(2,'Citrix Cloud'),(3,'NetScaler'),(4,'Windows Server Administration'),(34,'AWS'),(35,'Microsoft Azure'),(37,'NetScaler - Advanced'),(41,'Communication Skills'),(42,'English Level'),(43,'Problem Solving Skills'),(46,'Networking');
/*!40000 ALTER TABLE `job_categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `job_certifications`
--

DROP TABLE IF EXISTS `job_certifications`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `job_certifications` (
  `id` int NOT NULL AUTO_INCREMENT,
  `certification` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=62 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `job_certifications`
--

LOCK TABLES `job_certifications` WRITE;
/*!40000 ALTER TABLE `job_certifications` DISABLE KEYS */;
INSERT INTO `job_certifications` VALUES (1,'AWS Certified Cloud Practitioner'),(2,'AWS Certified DevOps Engineer – Professional'),(3,'AWS Certified Developer – Associate'),(4,'AWS Certified Solutions Architect – Associate'),(5,'AWS Certified Solutions Architect – Professional'),(6,'AWS Certified SysOps Administrator – Associate'),(7,'CCA-AppDS - Citrix Certified Associate – App Delivery and Security'),(8,'CCA-N Citrix Certified Associate - Networking'),(9,'CCE-N Citrix Certified Expert - Networking'),(10,'CCE-V Citrix Certified Expert - Virtualization'),(11,'CCNA-Cisco Certified Network Associate'),(12,'CCP-AppDS - Citrix Certified Professional – App Delivery and Security'),(13,'CCP-N Citrix Certified Professional - Networking'),(14,'CCP-V Citrix Certified Professional - Virtualization'),(15,'CCP-W Citrix Certified Professional - Workspace'),(16,'CEH'),(17,'CISSP'),(18,'Certified Kubernetes Administrator (CKA)'),(19,'CompTIA A+'),(20,'CompTIA Network+  MS AZ-800 Windows Hybrid '),(21,'CompTIA Security+'),(22,'FortiAnalyzer 7.0 Administrator'),(23,'Fortinet Certified Professional Network Security'),(24,'Google Professional Cloud Architect'),(25,'HCNA - Huawei technologies'),(26,'HCNA WLAN - Huawei technologies'),(27,'IBM Cloud Technical Advocate Concepts'),(28,'IBM Cloud Technical Advocate Foundations'),(29,'ITIL v3 Foundation Certified'),(30,'Microsoft 365 Certified: Enterprise Administrator Expert'),(31,'Microsoft 365 Certified: Fundamentals'),(36,'Microsoft Certified: Dynamics 365 Sales Functional Consultant Associate'),(37,'Microsoft Certified: Security, Compliance, and Identity Fundamentals'),(38,'OCI Foundations Associate'),(39,'PMP'),(40,'SCRUM MASTER PROFESSIONAL CERTIFICATE (SMPC)'),(41,'CCA-V Citrix Certified Associate - Virtualization'),(47,'Citrix Certified - Citrix Workspace Microapps Service'),(49,'AWS Certified Security – Specialty'),(50,'Microsoft Azure AZ-800 Windows Hybrid '),(51,' Microsoft Azure AZ-140 Azure Virtual Desktop Speciality'),(52,'Microsoft Azure AZ-104 Azure Administrator'),(53,'Microsoft Azure AZ-305 Azure Architect'),(54,'VMware Double VPC - Data Center Virtualization & Desktop Mobility'),(55,'VMWare Certified Professional - Desktop Management'),(56,'VMWare Certified Professional - Data Center Virtualization'),(57,'AWS Partner: Technical Accredited'),(58,'AWS Certified Network – Specialty'),(59,'CompTIA Net+ N10-008'),(60,'Citrix Cloud Certified - Virtual Apps and Desktops Service'),(61,'Microsoft Azure AZ-900 Azure Fundamentals');
/*!40000 ALTER TABLE `job_certifications` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `job_postings`
--

DROP TABLE IF EXISTS `job_postings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `job_postings` (
  `id` int NOT NULL AUTO_INCREMENT,
  `job_category` varchar(255) NOT NULL,
  `job_title` varchar(255) NOT NULL,
  `job_details` text NOT NULL,
  `Workplace_type` text,
  `job_type` varchar(255) NOT NULL,
  `linkedin_url` varchar(255) DEFAULT NULL,
  `role_description` text,
  `responsibilities` text,
  `preferred_certifications` text,
  `qualifications` text,
  `salary_range` text,
  `post_date` date DEFAULT NULL,
  `enabled` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `job_postings`
--

LOCK TABLES `job_postings` WRITE;
/*!40000 ALTER TABLE `job_postings` DISABLE KEYS */;
INSERT INTO `job_postings` VALUES (10,'Citrix','L2 - Service Desk Engineer','Full-time position supporting & maintaining customer environments. Responsibilities include troubleshooting, system monitoring, and timely alert response as per SLAs.','Remote','Full-time','https://www.linkedin.com/jobs/view/3279204899','test','test','test','test','$2.000 - $3.000 USD based on the Skillsets.','2024-06-17',0),(12,'Citrix','L3 - Service Desk Engineer','As part of our service catalog, we are looking for candidates that will be part of our managed services team, that will be in charge of delivering continuous support to our customers. You will be part of a talented team of engineers that demonstrate great superb technical competency, delivery mission critical infrastructure and ensuring the highest level of availability, performance and security.','Remote','Full-time','https://www.linkedin.com/jobs/view/3953274821','Ticket Management:\r\nReceive and manage escalation tickets related to NetScaler and Citrix issues.\r\nPrioritize and respond to tickets in a timely manner, ensuring SLA compliance.\r\nTroubleshooting and Resolution:\r\nDiagnose and resolve complex technical issues involving NetScaler and Citrix environments.\r\nPerform root cause analysis to prevent recurrence of issues.\r\nUtilize advanced troubleshooting tools and techniques to address network, application, and system problems.','Ticket Management:\r\nReceive and manage escalation tickets related to NetScaler and Citrix issues.\r\nPrioritize and respond to tickets in a timely manner, ensuring SLA compliance.\r\nTroubleshooting and Resolution:\r\nDiagnose and resolve complex technical issues involving NetScaler and Citrix environments.\r\nPerform root cause analysis to prevent recurrence of issues.\r\nUtilize advanced troubleshooting tools and techniques to address network, application, and system problems.','-Citrix CCP-V\r\n-Citrix CCP-N\r\n-MSCA Windows Server/Windows 10','-Teamwork\r\n-Constant learning\r\n-Self-management\r\n-Good written and verbal communication\r\n-Detail oriented','$3.000 - $4.000 USD based on the Skillsets.','2024-06-18',0),(14,'Citrix','L2 - Service Desk Engineer','This is a full-time remote role for a L2 Engineer - Managed Services. As a L2 Engineer - Managed Services, you will be responsible for maintaining and supporting customer\'s environment by providing in-depth troubleshooting and resolution of issues, system monitoring, and response to alerts in accordance with the customer\'s Service Level Agreement.','Remote','Full-time','https://www.linkedin.com/jobs/view/3953274821','This is a full-time remote role for a L2 Engineer - Managed Services. As a L2 Engineer - Managed Services, you will be responsible for maintaining and supporting customer\'s environment by providing in-depth troubleshooting and resolution of issues, system monitoring, and response to alerts in accordance with the customer\'s Service Level Agreement.','This is a full-time remote role for a L2 Engineer - Managed Services. As a L2 Engineer - Managed Services, you will be responsible for maintaining and supporting customer\'s environment by providing in-depth troubleshooting and resolution of issues, system monitoring, and response to alerts in accordance with the customer\'s Service Level Agreement.','-Citrix Certified Associate - Virtualization\r\n-Citrix Certified Associate - App Delivery and Security\r\n-Citrix Certified Professional - Virtualization','-Level of English - B2 according to the Common European Framework of Reference for Languages (CEFR). All activities and interactions with the customers will be performed 100% in English.\r\n-2+ years of customer service experience in a managed services environment with solid skills in server administrations and ITIL operations\r\n-2+ years with Windows Server Roles (ADFS, FS, RDG, DNS, IIS) support experience\r\n-2+ years of Citrix Virtual Apps and Desktops\r\n-1 year of experience with VMWare vSphere, Citrix Hypervisor or Microsoft Hyper-V\r\n-Citrix Cloud Experience or knowledge is desirable\r\n-Active Directory and Group Policy management experience concerning the role','$2.000 - $3.000 USD based on the Skillsets.','2024-06-18',0),(19,'Citrix','L1 - Service Desk Engineer','This is a full-time remote role for a L1 Engineer - Managed Services. As a L1 Engineer - Managed Services, you will be responsible for maintaining and supporting customer\'s environment by providing in-depth troubleshooting and resolution of issues, system monitoring, and response to alerts in accordance with the customer\'s Service Level Agreement.','Remote','Full-time','https://www.linkedin.com/jobs/view/3953274821','This is a full-time remote role for a L1 Engineer - Managed Services. As a L1 Engineer - Managed Services, you will be responsible for maintaining and supporting customer\'s environment by providing in-depth troubleshooting and resolution of issues, system monitoring, and response to alerts in accordance with the customer\'s Service Level Agreement.','This is a full-time remote role for a L1 Engineer - Managed Services. As a L1 Engineer - Managed Services, you will be responsible for maintaining and supporting customer\'s environment by providing in-depth troubleshooting and resolution of issues, system monitoring, and response to alerts in accordance with the customer\'s Service Level Agreement.','This is a full-time remote role for a L1 Engineer - Managed Services. As a L1 Engineer - Managed Services, you will be responsible for maintaining and supporting customer\'s environment by providing in-depth troubleshooting and resolution of issues, system monitoring, and response to alerts in accordance with the customer\'s Service Level Agreement.','This is a full-time remote role for a L1 Engineer - Managed Services. As a L1 Engineer - Managed Services, you will be responsible for maintaining and supporting customer\'s environment by providing in-depth troubleshooting and resolution of issues, system monitoring, and response to alerts in accordance with the customer\'s Service Level Agreement.','$1.000 - $2.000  USD based on the Skillsets.','2024-06-20',0);
/*!40000 ALTER TABLE `job_postings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `job_skillsets`
--

DROP TABLE IF EXISTS `job_skillsets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `job_skillsets` (
  `id` int NOT NULL AUTO_INCREMENT,
  `category_id` int NOT NULL,
  `skillset_name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `category_id` (`category_id`),
  CONSTRAINT `job_skillsets_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `job_categories` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=171 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `job_skillsets`
--

LOCK TABLES `job_skillsets` WRITE;
/*!40000 ALTER TABLE `job_skillsets` DISABLE KEYS */;
INSERT INTO `job_skillsets` VALUES (1,1,'Installation and Configuration'),(2,1,'Managing Machine Catalogs and Delivery Groups'),(3,1,'Application Publishing'),(4,1,'Profile Management'),(5,1,'StoreFront Configuration'),(6,1,'Citrix Policies'),(7,1,'Monitoring and Troubleshooting'),(8,1,'Citrix Director'),(9,1,'Citrix Studio'),(10,1,'Load Balancing'),(11,2,'Cloud Connectors Installation'),(12,2,'Workspace Configuration'),(13,2,'Resource Locations'),(14,2,'Subscription Management'),(15,2,'Identity and Access Management'),(16,2,'Monitoring and Analytics'),(17,2,'Service Health and Performance'),(18,2,'Disaster Recovery'),(19,2,'Integration with On-Premises'),(20,2,'Security Management'),(21,3,'Load Balancing Configuration'),(22,3,'SSL Offloading'),(23,3,'Content Switching'),(24,3,'Global Server Load Balancing (GSLB)'),(25,3,'Application Firewall Configuration'),(26,3,'NetScaler Gateway Setup'),(27,3,'High Availability'),(28,3,'Networking and TCP Optimization'),(29,3,'Monitoring and Logging'),(30,3,'Authentication, Authorization, and Auditing (AAA)'),(31,4,'Installation and Configuration'),(32,4,'Active Directory Management'),(33,4,'Group Policy Management'),(34,4,'DNS and DHCP Configuration'),(35,4,'File and Storage Services'),(36,4,'Windows Server Update Services (WSUS)'),(37,4,'Performance Monitoring and Tuning'),(38,4,'Backup and Restore'),(39,4,'Remote Desktop Services (RDS)'),(40,4,'PowerShell Scripting'),(98,34,'EC2 Management'),(99,34,'S3 Storage Solutions'),(100,34,'VPC Configuration'),(101,34,'IAM Policies and Roles'),(102,34,'RDS Management'),(103,34,'Lambda Functions'),(104,34,'CloudFormation Templates'),(105,34,'Route 53 DNS Management'),(106,34,'CloudWatch Monitoring'),(107,34,'Security Groups and Network ACLs'),(108,35,'Azure Virtual Machines'),(109,35,'Azure Storage Solutions'),(110,35,'Azure Virtual Network (VNet) Configuration'),(111,35,'Azure Active Directory (AD)'),(112,35,'Azure SQL Database Management'),(113,35,'Azure Functions'),(114,35,'Azure Resource Manager (ARM) Templates'),(115,35,'Azure DNS Management'),(116,35,'Azure Monitor and Alerts'),(117,35,'Azure Security Center'),(118,37,'Advanced Load Balancing Techniques with Content Switching Policies'),(119,37,'SSL Offloading, Certificate Management, and TLS 1.3 Configuration'),(120,37,'Advanced Content Switching with Regex and Expressions'),(121,37,'Global Server Load Balancing (GSLB) with Site Persistence'),(122,37,'In-depth Troubleshooting using Command-Line Interface (CLI) and NITRO API'),(123,37,'Advanced Application Firewall Configuration with Custom Rules'),(124,37,'Optimizing Traffic Management with Rate Limiting and QoS Policies'),(125,37,'Integrating Authentication and Authorization with SAML and OAuth'),(126,37,'Advanced Secure Web Gateway Configuration with URL Filtering'),(127,37,'Configuring and Managing NetScaler MAS (Management and Analytics System) for Large Scale Deployments'),(128,41,'Verbal Communication'),(129,41,'Nonverbal Communication'),(130,41,'Listening Skills'),(131,41,'Public Speaking'),(132,41,'Written Communication'),(133,41,'Emotional Intelligence'),(134,41,'Presentation Skills'),(135,41,'Persuasion and Influence'),(136,41,'Conflict Resolution'),(138,42,'Basic Understanding'),(139,42,'Conversational Fluency'),(140,42,'Professional Proficiency'),(141,42,'Advanced Vocabulary'),(142,42,'Grammar Accuracy'),(143,42,'Pronunciation Clarity'),(144,42,'Reading Comprehension'),(145,42,'Writing Skills'),(146,42,'Listening Comprehension'),(147,42,'Public Speaking Proficiency'),(148,43,'Analytical Thinking'),(149,43,'Creative Problem Solving'),(150,43,'Decision Making'),(151,43,'Strategic Thinking'),(152,43,'Root Cause Analysis'),(153,43,'Troubleshooting'),(154,43,'Resourcefulness'),(155,43,'Risk Management'),(156,43,'Innovative Solutions'),(157,43,'Process Improvement'),(160,46,'Fundamentals'),(161,46,'OSI and TCP/IP Models'),(162,46,'Switching Concepts'),(163,46,'IPv4 and IPv6 Addressing'),(164,46,'VLANs'),(165,46,'Routing'),(166,46,'Network Security (ACL, NAT)'),(167,46,'WAN Technologies (MPLS, VPNs)'),(168,46,'Troubleshooting'),(169,46,'Cloud Networking'),(170,41,'Interpersonal Skills');
/*!40000 ALTER TABLE `job_skillsets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `site_feedback`
--

DROP TABLE IF EXISTS `site_feedback`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `site_feedback` (
  `id` int NOT NULL AUTO_INCREMENT,
  `type` varchar(255) NOT NULL,
  `description` text NOT NULL,
  `email` varchar(255) DEFAULT NULL,
  `screenshotUrl` varchar(255) DEFAULT NULL,
  `status` varchar(50) NOT NULL DEFAULT 'Open',
  `observations` text,
  `date_open` date NOT NULL,
  `date_closed` date DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `site_feedback`
--

LOCK TABLES `site_feedback` WRITE;
/*!40000 ALTER TABLE `site_feedback` DISABLE KEYS */;
INSERT INTO `site_feedback` VALUES (1,'Application Error, Application Error','test','juan.otalvaro@samanagroup.co','https://drive.google.com/file/d/1r0sF26OKD_YT5RCbFxpT2YYqXTu0K36a/view','Open',NULL,'2024-08-05',NULL),(2,'Application Error, Application Error','test','juan.otalvaro@samanagroup.co','https://drive.google.com/file/d/1rMxVXRE4mdxBikC-QhDFVZpubldy2pdO/view','Open',NULL,'2024-08-05',NULL),(3,'Functionality, Functionality','test2','juan.otalvaro@samanagroup.co','https://drive.google.com/file/d/18PxdUotGBG_XiOUA7s8fHqXAtjuguHPK/view','Open',NULL,'2024-08-05',NULL),(4,'Application Error, Application Error','dadsdsa','juan.otalvaro@samanagroup.co','https://drive.google.com/file/d/1xGq9gqbGVy39SggTclctL4hUsycCgwYb/view','Open',NULL,'2024-08-05',NULL),(5,'Application Error, Application Error','dadsdsa','juan.otalvaro@samanagroup.co','https://drive.google.com/file/d/1zYogaGwWBRDheQ2aSnlFqLT9oCkyVVO0/view','Open',NULL,'2024-08-05',NULL);
/*!40000 ALTER TABLE `site_feedback` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `google_id` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `profile_image` varchar(255) DEFAULT NULL,
  `admin` int DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=55 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'107718006345817804829','Juan Pablo Otalvaro','juan.otalvaro@samanagroup.co','2024-05-29 21:02:56','https://lh3.googleusercontent.com/a/ACg8ocJ63PiVOvjMOWzDg1Dq5DO0uxODftn7tmwUD5mj4DoJH4m3B2U=s96-c',5),(20,'106627567844771269358','Julian Gomez','julian.gomez@samanagroup.co','2024-05-29 21:47:08',NULL,4),(21,'112593017355682812744','Alonso Maury Santana Torres','alonso.santana@samanagroup.co','2024-05-29 21:51:42',NULL,3),(22,'108974602786113534024','Danny Ruiz','danny.ruiz@samanagroup.co','2024-05-29 21:52:28',NULL,4),(23,'109428893794057877653','Felipe Bernal','felipe.bernal@samanagroup.co','2024-05-29 21:53:32',NULL,5),(28,'115501872698198075239','Fabian Baena','fabian.baena@samanagroup.co','2024-05-30 19:22:24',NULL,4),(29,'108003748111961961576','Jorge Gomez','Jorge.Gomez@samanagroup.co','2024-05-30 21:20:00',NULL,3);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-08-13 13:53:16
