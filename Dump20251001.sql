CREATE DATABASE  IF NOT EXISTS `resilienza` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `resilienza`;
-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: resilienza
-- ------------------------------------------------------
-- Server version	9.2.0

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
-- Table structure for table `ambito`
--

DROP TABLE IF EXISTS `ambito`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ambito` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `DESCR` varchar(255) NOT NULL,
  `NOTE` text,
  `ACRONIMO` varchar(50) DEFAULT NULL,
  `DATA_ULTIMA_MODIFICA` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `MODIFICATO_DA` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `ACRONIMO` (`ACRONIMO`)
) ENGINE=InnoDB AUTO_INCREMENT=572 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ambito`
--

LOCK TABLES `ambito` WRITE;
/*!40000 ALTER TABLE `ambito` DISABLE KEYS */;
INSERT INTO `ambito` VALUES (1,'Commerciale','Riguarda tutte le attività di vendita e marketing.','COMM','2025-07-08 10:08:37','root@localhost'),(2,'Operativo','Gestisce le operazioni quotidiane e la logistica.','OPR','2025-07-08 10:08:37','root@localhost'),(3,'Finanziario','Si occupa della contabilità, bilancio e investimenti.','FIN','2025-07-08 10:08:37','root@localhost'),(4,'Risorse Umane','Gestisce il personale e le politiche HR.','HR','2025-07-08 10:08:37','root@localhost'),(5,'IT','Riguarda lo sviluppo software e la gestione infrastrutture','IT','2025-07-22 13:27:31','root@localhost'),(7,'Ambito new1','Ambito1 test1','NEW1','2025-07-22 13:30:23','root@localhost'),(10,'Ambito2','aaaaaaaaaa','NEW2','2025-07-22 15:01:21','root@localhost'),(11,'Ambito Default per Categorie','Creato per test','DEFAULT_AMB','2025-07-23 09:26:40','root@localhost');
/*!40000 ALTER TABLE `ambito` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `categoria`
--

DROP TABLE IF EXISTS `categoria`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categoria` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `DESCR` varchar(255) NOT NULL,
  `TIPO_CATEGORIA` varchar(100) DEFAULT NULL,
  `ID_AMBITO` int NOT NULL,
  `DATA_ULTIMA_MODIFICA` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `MODIFICATO_DA` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  KEY `ID_AMBITO` (`ID_AMBITO`),
  CONSTRAINT `categoria_ibfk_1` FOREIGN KEY (`ID_AMBITO`) REFERENCES `ambito` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categoria`
--

LOCK TABLES `categoria` WRITE;
/*!40000 ALTER TABLE `categoria` DISABLE KEYS */;
INSERT INTO `categoria` VALUES (1,'Marketing Digitale','Marketing',2,'2025-07-23 12:55:48','root@localhost'),(2,'Vendite B2B','Vendite',1,'2025-07-23 12:57:22','root@localhost'),(3,'Logistica Inbound','Logistica',2,'2025-07-08 10:09:36','root@localhost'),(4,'Gestione Magazzino','Logistica',1,'2025-07-23 12:56:56','root@localhost'),(5,'Contabilità Clienti','Contabilità',3,'2025-07-08 10:09:36','root@localhost'),(6,'Budgeting','Finanza',3,'2025-07-08 10:09:36','root@localhost'),(7,'Recruiting','HR',4,'2025-07-08 10:09:36','root@localhost'),(8,'Formazione Dipendenti','HR',4,'2025-07-08 10:09:36','root@localhost'),(9,'Sviluppo Software','IT',5,'2025-07-08 10:09:36','root@localhost'),(10,'Supporto Tecnico','IT',5,'2025-07-08 10:09:36','root@localhost'),(11,'Categoria Default per Domande','Default',1,'2025-07-25 16:00:09','root@localhost'),(26,'Categoria Default per Driver','Default',11,'2025-07-28 10:57:25','root@localhost');
/*!40000 ALTER TABLE `categoria` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cliente`
--

DROP TABLE IF EXISTS `cliente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cliente` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `RAGIONE_SOCIALE` varchar(255) NOT NULL,
  `PARTITA_IVA` varchar(11) DEFAULT NULL,
  `INDIRIZZO` varchar(255) DEFAULT NULL,
  `CITTA` varchar(100) DEFAULT NULL,
  `PROVINCIA` varchar(2) DEFAULT NULL,
  `CAP` varchar(5) DEFAULT NULL,
  `EMAIL` varchar(255) DEFAULT NULL,
  `TELEFONO` varchar(50) DEFAULT NULL,
  `DATA_ULTIMA_MODIFICA` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `MODIFICATO_DA` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `idx_piva` (`PARTITA_IVA`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cliente`
--

LOCK TABLES `cliente` WRITE;
/*!40000 ALTER TABLE `cliente` DISABLE KEYS */;
/*!40000 ALTER TABLE `cliente` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `domande`
--

DROP TABLE IF EXISTS `domande`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `domande` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `DESCR` text NOT NULL,
  `ID_DRIVER` int NOT NULL,
  `DATA_ULTIMA_MODIFICA` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `MODIFICATO_DA` varchar(100) DEFAULT NULL,
  `ID_GRUPPO_RISPOSTA` int DEFAULT NULL,
  PRIMARY KEY (`ID`),
  KEY `ID_DRIVER` (`ID_DRIVER`),
  KEY `fk_domande_gruppo_risposta` (`ID_GRUPPO_RISPOSTA`),
  CONSTRAINT `domande_ibfk_1` FOREIGN KEY (`ID_DRIVER`) REFERENCES `driver` (`ID`),
  CONSTRAINT `fk_domande_gruppo_risposta` FOREIGN KEY (`ID_GRUPPO_RISPOSTA`) REFERENCES `gruppo_risposta` (`ID_GRUPPO_RISPOSTA`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=54 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `domande`
--

LOCK TABLES `domande` WRITE;
/*!40000 ALTER TABLE `domande` DISABLE KEYS */;
INSERT INTO `domande` VALUES (1,'Quali sono le parole chiave più rilevanti per il nostro settore?',1,'2025-09-30 15:01:43','root@localhost',3),(2,'Come possiamo migliorare il posizionamento sui motori di ricerca?',1,'2025-10-01 14:04:44','root@localhost',2),(3,'Qual è il ROI delle nostre campagne SEM attuali?',2,'2025-07-08 10:12:03','root@localhost',NULL),(4,'Come possiamo ottimizzare le offerte CPC per massimizzare le conversioni?',2,'2025-07-08 10:12:03','root@localhost',NULL),(5,'Quale piattaforma di email marketing consigliate?',3,'2025-07-08 10:12:03','root@localhost',NULL),(6,'Come possiamo segmentare meglio la nostra lista email?',3,'2025-07-08 10:12:03','root@localhost',NULL),(7,'Quali sono le strategie più efficaci per la lead generation?',4,'2025-07-08 10:12:03','root@localhost',NULL),(8,'Come possiamo qualificati i lead in ingresso?',4,'2025-07-08 10:12:03','root@localhost',NULL),(9,'Quali sono i termini standard per i nostri contratti B2B?',5,'2025-07-08 10:12:03','root@localhost',NULL),(10,'Qual è il nostro tasso di successo nella chiusura dei contratti?',5,'2025-07-08 10:12:03','root@localhost',NULL),(11,'Come monitoriamo l\'efficienza della flotta?',6,'2025-07-08 10:12:03','root@localhost',NULL),(12,'Quali sono i costi di manutenzione della nostra flotta?',6,'2025-07-08 10:12:03','root@localhost',NULL),(13,'Come ottimizziamo i percorsi di consegna?',7,'2025-07-08 10:12:03','root@localhost',NULL),(14,'Quali software usiamo per la pianificazione dei percorsi?',7,'2025-07-08 10:12:03','root@localhost',NULL),(15,'Come gestiamo l\'inventario per evitare esaurimento scorte?',8,'2025-07-08 10:12:03','root@localhost',NULL),(16,'Qual è la nostra rotazione di magazzino media?',8,'2025-07-08 10:12:03','root@localhost',NULL),(17,'Quali standard di qualità adottiamo per i prodotti in ingresso?',9,'2025-07-08 10:12:03','root@localhost',NULL),(18,'Come gestiamo i resi per difetti di qualità?',9,'2025-07-08 10:12:03','root@localhost',NULL),(19,'Qual è il processo di fatturazione per i nuovi clienti?',10,'2025-07-08 10:12:03','root@localhost',NULL),(20,'Come gestiamo i crediti inesigibili?',10,'2025-07-08 10:12:03','root@localhost',NULL),(21,'Quali sono le procedure per la riconciliazione bancaria?',11,'2025-07-08 10:12:03','root@localhost',NULL),(22,'Come identifichiamo le discrepanze nei conti?',11,'2025-07-08 10:12:03','root@localhost',NULL),(23,'Quali sono le scadenze fiscali principali per quest\'anno?',12,'2025-07-08 10:12:03','root@localhost',NULL),(24,'Come possiamo ridurre l\'onere fiscale legalmente?',12,'2025-07-08 10:12:03','root@localhost',NULL),(25,'Come calcoliamo il costo di produzione per unità?',13,'2025-07-08 10:12:03','root@localhost',NULL),(26,'Quali sono i maggiori fattori di costo operativi?',13,'2025-07-08 10:12:03','root@localhost',NULL),(27,'Quali sono le migliori pratiche per condurre un colloquio?',14,'2025-07-08 10:12:03','root@localhost',NULL),(28,'Come valutiamo le competenze tecniche dei candidati?',14,'2025-07-08 10:12:03','root@localhost',NULL),(29,'Qual è il processo di onboarding per i nuovi assunti?',15,'2025-07-08 10:12:03','root@localhost',NULL),(30,'Come misuriamo l\'efficacia dell\'onboarding?',15,'2025-07-08 10:12:03','root@localhost',NULL),(31,'Quali corsi di aggiornamento sono obbligatori per il nostro personale?',16,'2025-07-08 10:12:03','root@localhost',NULL),(32,'Come valuti l\'impatto della formazione sulla produttività? ',16,'2025-07-28 10:35:56','root@localhost',NULL),(33,'Quali certificazioni IT sono richieste per il ruolo X?',17,'2025-07-08 10:12:03','root@localhost',NULL),(34,'Offriamo incentivi per l\'ottenimento di certificazioni?',17,'2025-07-08 10:12:03','root@localhost',NULL),(35,'Quali pattern di architettura software adottiamo?',18,'2025-07-08 10:12:03','root@localhost',NULL),(36,'Come garantiamo la scalabilità delle nostre applicazioni?',18,'2025-07-08 10:12:03','root@localhost',NULL),(37,'Quali strumenti usiamo per il debug del codice?',19,'2025-07-08 10:12:03','root@localhost',NULL),(38,'Come gestiamo i bug critici in produzione?',19,'2025-07-08 10:12:03','root@localhost',NULL),(39,'Qual è il SLA per le richieste di help desk?',20,'2025-07-08 10:12:03','root@localhost',NULL),(40,'Come misuriamo la soddisfazione degli utenti del supporto tecnico?',20,'2025-07-08 10:12:03','root@localhost',NULL),(41,'Qual è il processo di escalation per gli incidenti di livello 1?',21,'2025-07-08 10:12:03','root@localhost',NULL),(42,'Come documentiamo e analizziamo gli incidenti passati?',21,'2025-07-08 10:12:03','root@localhost',NULL),(49,'Domanda 1 Driver 1',1,'2025-08-28 13:44:39','root@localhost',NULL),(50,'Domanda 1 Driver 2',2,'2025-08-28 13:44:39','root@localhost',NULL),(51,'Domanda 2 Driver 1',1,'2025-08-28 13:44:39','root@localhost',NULL),(52,'Domanda 1 Driver 3',3,'2025-08-28 13:44:39','root@localhost',NULL),(53,'Domanda 2 Driver 2',2,'2025-08-28 13:44:39','root@localhost',NULL);
/*!40000 ALTER TABLE `domande` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `domande_questionario`
--

DROP TABLE IF EXISTS `domande_questionario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `domande_questionario` (
  `ID_QUESTIONARIO` int NOT NULL,
  `ID_DOMANDA` int NOT NULL,
  PRIMARY KEY (`ID_QUESTIONARIO`,`ID_DOMANDA`),
  KEY `fk_dq_domanda` (`ID_DOMANDA`),
  CONSTRAINT `fk_dq_domanda` FOREIGN KEY (`ID_DOMANDA`) REFERENCES `domande` (`ID`) ON DELETE CASCADE,
  CONSTRAINT `fk_dq_questionario` FOREIGN KEY (`ID_QUESTIONARIO`) REFERENCES `questionario` (`ID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `domande_questionario`
--

LOCK TABLES `domande_questionario` WRITE;
/*!40000 ALTER TABLE `domande_questionario` DISABLE KEYS */;
INSERT INTO `domande_questionario` VALUES (4,1),(5,1),(6,1),(2,2),(3,2),(2,3),(3,3),(2,4),(3,5),(6,5),(6,7),(6,9),(6,11),(6,12),(6,13),(6,14),(4,16),(6,16),(5,17),(4,36),(3,50),(2,51),(3,52);
/*!40000 ALTER TABLE `domande_questionario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `driver`
--

DROP TABLE IF EXISTS `driver`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `driver` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `DESCR` varchar(255) NOT NULL,
  `ID_CATEGORIA` int NOT NULL,
  `DATA_ULTIMA_MODIFICA` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `MODIFICATO_DA` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  KEY `ID_CATEGORIA` (`ID_CATEGORIA`),
  CONSTRAINT `driver_ibfk_1` FOREIGN KEY (`ID_CATEGORIA`) REFERENCES `categoria` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `driver`
--

LOCK TABLES `driver` WRITE;
/*!40000 ALTER TABLE `driver` DISABLE KEYS */;
INSERT INTO `driver` VALUES (1,'SEO',1,'2025-07-08 10:10:46','root@localhost'),(2,'SEM',1,'2025-07-08 10:10:46','root@localhost'),(3,'Email Marketing',1,'2025-07-08 10:10:46','root@localhost'),(4,'Lead Generation',2,'2025-07-08 10:10:46','root@localhost'),(5,'Negoziazione Contratti',2,'2025-07-08 10:10:46','root@localhost'),(6,'Gestione Flotta',3,'2025-07-08 10:10:46','root@localhost'),(7,'Ottimizzazione Percorsi',3,'2025-07-08 10:10:46','root@localhost'),(8,'Inventario',4,'2025-07-08 10:10:46','root@localhost'),(9,'Controllo Qualità Prodotti',4,'2025-07-08 10:10:46','root@localhost'),(10,'Fatturazione',5,'2025-07-08 10:10:46','root@localhost'),(11,'Riconciliazione Conti',5,'2025-07-08 10:10:46','root@localhost'),(12,'Pianificazione Fiscale',6,'2025-07-08 10:10:46','root@localhost'),(13,'Analisi di Costo',6,'2025-07-08 10:10:46','root@localhost'),(14,'Colloqui',7,'2025-07-08 10:10:46','root@localhost'),(15,'Onboarding',7,'2025-07-08 10:10:46','root@localhost'),(16,'Corsi di Aggiornamento',8,'2025-07-08 10:10:46','root@localhost'),(17,'Certificazioni IT',8,'2025-07-08 10:10:46','root@localhost'),(18,'Architettura Software',9,'2025-07-08 10:10:46','root@localhost'),(19,'Debug Codice',9,'2025-07-08 10:10:46','root@localhost'),(20,'Help Desk',10,'2025-07-08 10:10:46','root@localhost'),(21,'Gestione Incidenti',10,'2025-07-08 10:10:46','root@localhost'),(22,'Driver Default per Domande',11,'2025-07-25 16:00:09','root@localhost');
/*!40000 ALTER TABLE `driver` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gruppo_risposta`
--

DROP TABLE IF EXISTS `gruppo_risposta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `gruppo_risposta` (
  `ID_GRUPPO_RISPOSTA` int NOT NULL AUTO_INCREMENT,
  `DESCR_GRUPPO_RISPOSTA` varchar(100) NOT NULL,
  `MODIFICATO_DA` varchar(100) DEFAULT NULL,
  `DATA_ULTIMA_MODIFICA` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`ID_GRUPPO_RISPOSTA`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Tabella per la gestione dei gruppi di risposte.';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gruppo_risposta`
--

LOCK TABLES `gruppo_risposta` WRITE;
/*!40000 ALTER TABLE `gruppo_risposta` DISABLE KEYS */;
INSERT INTO `gruppo_risposta` VALUES (1,'Si Positivo','system','2025-07-28 16:18:12'),(2,'Tutti Parzialmente','system','2025-07-28 16:18:12'),(3,'Si Negativo','configuratore@example.com','2025-09-18 16:05:15'),(4,'Si Parzialmente','system','2025-07-28 16:18:12');
/*!40000 ALTER TABLE `gruppo_risposta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gruppo_risposta_risposta`
--

DROP TABLE IF EXISTS `gruppo_risposta_risposta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `gruppo_risposta_risposta` (
  `ID_GRUPPO_RISPOSTA` int NOT NULL,
  `ID_RISPOSTA` int NOT NULL,
  PRIMARY KEY (`ID_GRUPPO_RISPOSTA`,`ID_RISPOSTA`),
  KEY `fk_grr_risposta` (`ID_RISPOSTA`),
  CONSTRAINT `fk_grr_gruppo_risposta` FOREIGN KEY (`ID_GRUPPO_RISPOSTA`) REFERENCES `gruppo_risposta` (`ID_GRUPPO_RISPOSTA`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_grr_risposta` FOREIGN KEY (`ID_RISPOSTA`) REFERENCES `risposta` (`ID_RISPOSTA`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Tabella di associazione per la relazione molti-a-molti.';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gruppo_risposta_risposta`
--

LOCK TABLES `gruppo_risposta_risposta` WRITE;
/*!40000 ALTER TABLE `gruppo_risposta_risposta` DISABLE KEYS */;
INSERT INTO `gruppo_risposta_risposta` VALUES (1,14),(4,15),(2,16),(1,17),(1,18),(2,18),(2,19),(2,20),(3,20),(4,35);
/*!40000 ALTER TABLE `gruppo_risposta_risposta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `progetto`
--

DROP TABLE IF EXISTS `progetto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `progetto` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `DESCR` varchar(200) NOT NULL,
  `DT_INIZIO` date DEFAULT NULL,
  `DT_FINE` date DEFAULT NULL,
  `ID_STATO` int DEFAULT NULL,
  `ID_AMBITO` int DEFAULT NULL,
  `REF_CLIENTE` varchar(200) DEFAULT NULL,
  `MODIFICATO_DA` varchar(100) DEFAULT NULL,
  `DATA_ULTIMA_MODIFICA` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`ID`),
  KEY `ID_AMBITO` (`ID_AMBITO`),
  CONSTRAINT `progetto_ibfk_1` FOREIGN KEY (`ID_AMBITO`) REFERENCES `ambito` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `progetto`
--

LOCK TABLES `progetto` WRITE;
/*!40000 ALTER TABLE `progetto` DISABLE KEYS */;
INSERT INTO `progetto` VALUES (11,'prj5','2025-09-10','2025-12-31',3,5,'ref_rocco','','2025-09-02 07:42:55');
/*!40000 ALTER TABLE `progetto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `questionario`
--

DROP TABLE IF EXISTS `questionario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `questionario` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `DESCR` varchar(255) NOT NULL,
  `DATA_CREAZIONE` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `CREATO_DA` varchar(100) DEFAULT NULL,
  `DATA_ULTIMA_MODIFICA` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `MODIFICATO_DA` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `questionario`
--

LOCK TABLES `questionario` WRITE;
/*!40000 ALTER TABLE `questionario` DISABLE KEYS */;
INSERT INTO `questionario` VALUES (1,'q1','2025-09-02 15:48:50','Utente di test',NULL,NULL),(2,'q4','2025-09-02 15:53:26','Utente di test',NULL,NULL),(3,'q2','2025-09-08 09:25:26','Utente di test',NULL,NULL),(4,'q3','2025-09-08 13:30:38','Utente di test',NULL,NULL),(5,'q5','2025-09-08 13:46:09','Utente di test',NULL,NULL),(6,'q6','2025-09-09 10:09:49','Utente di test',NULL,NULL);
/*!40000 ALTER TABLE `questionario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `questionario_cliente`
--

DROP TABLE IF EXISTS `questionario_cliente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `questionario_cliente` (
  `ID_QUESTIONARIO` int NOT NULL,
  `ID_CLIENTE` int NOT NULL,
  PRIMARY KEY (`ID_QUESTIONARIO`,`ID_CLIENTE`),
  KEY `fk_qc_cliente` (`ID_CLIENTE`),
  CONSTRAINT `fk_qc_cliente` FOREIGN KEY (`ID_CLIENTE`) REFERENCES `cliente` (`ID`) ON DELETE CASCADE,
  CONSTRAINT `fk_qc_questionario` FOREIGN KEY (`ID_QUESTIONARIO`) REFERENCES `questionario` (`ID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `questionario_cliente`
--

LOCK TABLES `questionario_cliente` WRITE;
/*!40000 ALTER TABLE `questionario_cliente` DISABLE KEYS */;
/*!40000 ALTER TABLE `questionario_cliente` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `questionario_domande`
--

DROP TABLE IF EXISTS `questionario_domande`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `questionario_domande` (
  `id_questionario` int DEFAULT NULL,
  `id_domanda` int DEFAULT NULL,
  KEY `id_questionario` (`id_questionario`),
  KEY `id_domanda` (`id_domanda`),
  CONSTRAINT `questionario_domande_ibfk_1` FOREIGN KEY (`id_questionario`) REFERENCES `questionario` (`ID`),
  CONSTRAINT `questionario_domande_ibfk_2` FOREIGN KEY (`id_domanda`) REFERENCES `domande` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `questionario_domande`
--

LOCK TABLES `questionario_domande` WRITE;
/*!40000 ALTER TABLE `questionario_domande` DISABLE KEYS */;
INSERT INTO `questionario_domande` VALUES (1,53),(1,4),(1,3),(1,49);
/*!40000 ALTER TABLE `questionario_domande` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `risposta`
--

DROP TABLE IF EXISTS `risposta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `risposta` (
  `ID_RISPOSTA` int NOT NULL AUTO_INCREMENT,
  `DESCR_RISPOSTA` varchar(100) NOT NULL,
  `MODIFICATO_DA` varchar(100) DEFAULT NULL,
  `DATA_ULTIMA_MODIFICA` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `PESO` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`ID_RISPOSTA`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Tabella per la gestione delle risposte associate ai gruppi di risposte.';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `risposta`
--

LOCK TABLES `risposta` WRITE;
/*!40000 ALTER TABLE `risposta` DISABLE KEYS */;
INSERT INTO `risposta` VALUES (14,'Si','configuratore@example.com','2025-09-18 16:24:49',1.00),(15,'No','configuratore@example.com','2025-09-18 16:24:56',0.00),(16,'Non noto','configuratore@example.com','2025-09-18 16:25:12',0.00),(17,'N/A','configuratore@example.com','2025-09-17 23:44:00',1.00),(18,'Tutti','configuratore@example.com','2025-09-16 18:03:25',2.00),(19,'Parzialmente','configuratore@example.com','2025-09-18 16:25:20',0.50),(20,'Nessuno','configuratore@example.com','2025-09-29 17:11:38',0.00),(35,'Si forse',NULL,'2025-09-18 16:24:11',1.00);
/*!40000 ALTER TABLE `risposta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `stati_progetto`
--

DROP TABLE IF EXISTS `stati_progetto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `stati_progetto` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `DESCR` varchar(255) NOT NULL,
  `NOTA` text,
  `DATA_ULTIMA_MODIFICA` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `MODIFICATO_DA` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `stati_progetto`
--

LOCK TABLES `stati_progetto` WRITE;
/*!40000 ALTER TABLE `stati_progetto` DISABLE KEYS */;
INSERT INTO `stati_progetto` VALUES (1,'In Lavorazione','Progetto in fase di sviluppo attivo.','2025-09-01 14:31:10',NULL),(2,'Completato','Progetto concluso con successo.','2025-09-01 14:31:10',NULL),(3,'Sospeso','Progetto temporaneamente fermo.','2025-09-01 14:31:10',NULL),(4,'Annullato','Progetto interrotto prima del completamento.','2025-09-01 14:31:10',NULL);
/*!40000 ALTER TABLE `stati_progetto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_ambito`
--

DROP TABLE IF EXISTS `t_ambito`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `t_ambito` (
  `id` int NOT NULL AUTO_INCREMENT,
  `codice` varchar(50) NOT NULL,
  `descrizione` varchar(255) NOT NULL,
  `dataCancellazione` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `codice` (`codice`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_ambito`
--

LOCK TABLES `t_ambito` WRITE;
/*!40000 ALTER TABLE `t_ambito` DISABLE KEYS */;
INSERT INTO `t_ambito` VALUES (1,'AMB001','Ambito di Test 1',NULL),(2,'AMB002','Ambito di Test 2',NULL),(3,'AMB003','Ambito di Test 3',NULL);
/*!40000 ALTER TABLE `t_ambito` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_dati_caricamento`
--

DROP TABLE IF EXISTS `t_dati_caricamento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `t_dati_caricamento` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `DESCRIZIONE` varchar(255) NOT NULL,
  `DATA_CARICAMENTO` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `UTENTE` varchar(100) NOT NULL,
  `NUMERO_RECORD` int NOT NULL,
  `STATO` varchar(50) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_dati_caricamento`
--

LOCK TABLES `t_dati_caricamento` WRITE;
/*!40000 ALTER TABLE `t_dati_caricamento` DISABLE KEYS */;
INSERT INTO `t_dati_caricamento` VALUES (1,'Caricamento massivo domande','2025-08-28 13:44:39','configuratore@example.com',5,'successo');
/*!40000 ALTER TABLE `t_dati_caricamento` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_funzionalita`
--

DROP TABLE IF EXISTS `t_funzionalita`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `t_funzionalita` (
  `id` int NOT NULL AUTO_INCREMENT,
  `menuPrincipale` tinyint(1) DEFAULT NULL,
  `fkPadre` int DEFAULT NULL,
  `titolo` varchar(100) DEFAULT NULL,
  `label` varchar(100) DEFAULT NULL,
  `icon` varchar(100) DEFAULT NULL,
  `link` varchar(100) DEFAULT NULL,
  `ordinatore` int NOT NULL,
  `target` varchar(15) NOT NULL,
  `dataCancellazione` datetime DEFAULT NULL,
  `fkMenuPrincipale` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_funzionalita_to_menu_principale` (`fkMenuPrincipale`),
  CONSTRAINT `fk_funzionalita_to_menu_principale` FOREIGN KEY (`fkMenuPrincipale`) REFERENCES `t_menu_principale` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_funzionalita`
--

LOCK TABLES `t_funzionalita` WRITE;
/*!40000 ALTER TABLE `t_funzionalita` DISABLE KEYS */;
INSERT INTO `t_funzionalita` VALUES (1,1,NULL,'Gestione Anagrafiche','Gestione Anagrafiche','fa-solid fa-cog','#',1,'_self',NULL,1),(2,0,1,'Ambito','Ambito','fa-solid fa-boxes','/ambito',2,'_self',NULL,1),(3,0,1,'Categoria','Categoria','fa-solid fa-tags','/categoria',3,'_self',NULL,1),(4,0,1,'Driver','Driver','fa-solid fa-road','/driver',4,'_self',NULL,1),(5,0,1,'Domanda','Domanda','fa-solid fa-question','/domanda',5,'_self',NULL,1),(9,0,NULL,'Menu Analista','Menu Analista','fa-solid fa-chart-line','#',10,'_self',NULL,1),(10,0,9,'Menu 10','Menu 10','fa-solid fa-circle-1','/menu10',11,'_self',NULL,1),(11,0,9,'Menu 11','Menu 11','fa-solid fa-circle-2','/menu11',12,'_self',NULL,1),(12,0,9,'Menu 12','Menu 12','fa-solid fa-circle-3','/menu12',13,'_self',NULL,1),(19,0,1,'Gruppi Risposte','Gruppi Risposte','fas fa-reply-all','/gruppo_risposta',6,'_self',NULL,1),(41,0,1,'Caricamento Domande','Caricamento Domande','fas fa-upload','/caricamento_domande',8,'_self',NULL,1),(42,0,NULL,'Menu 10','Menu Dieci','fas fa-list','/menu10',20,'_self',NULL,1),(43,0,NULL,'Menu 11','Menu Undici','fas fa-chart-line','/menu11',21,'_self',NULL,1),(44,0,NULL,'Menu 12','Menu Dodici','fas fa-table','/menu12',22,'_self',NULL,1),(45,0,1,'Log upload','Log upload','fa-solid fa-clipboard-check','/caricamenti_log',9,'_self',NULL,1),(46,0,NULL,'Gestione Progetti','Gestione Progetti','fa-solid fa-rocket','#',2,'_self',NULL,1),(47,0,46,'Nuovo Progetto','Nuovo Progetto','fa-solid fa-clone','/progetti',1,'_self',NULL,1),(48,0,46,'Assegna Analisti','Assegna Analisti','fa-solid fa-user-group','/assegna_analisti',2,'_self',NULL,1),(49,0,46,'Crea Questionario','Crea Questionario','fa-solid fa-user-group','/crea_questionario',3,'_self',NULL,1),(50,0,1,'Risposte','Risposte','fa-solid fa-square-poll-vertical','/gestione_risposte',7,'_self',NULL,1);
/*!40000 ALTER TABLE `t_funzionalita` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_funzionalita_utente`
--

DROP TABLE IF EXISTS `t_funzionalita_utente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `t_funzionalita_utente` (
  `id` int NOT NULL AUTO_INCREMENT,
  `fkIdRuolo` int DEFAULT NULL,
  `fkFunzionalita` int DEFAULT NULL,
  `permessi` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fkFunzionalita` (`fkFunzionalita`),
  KEY `fk_funzionalita_utente_ruolo` (`fkIdRuolo`),
  CONSTRAINT `fk_funzionalita_utente_ruolo` FOREIGN KEY (`fkIdRuolo`) REFERENCES `t_ruolo` (`ID`),
  CONSTRAINT `t_funzionalita_utente_ibfk_2` FOREIGN KEY (`fkFunzionalita`) REFERENCES `t_funzionalita` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=98 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_funzionalita_utente`
--

LOCK TABLES `t_funzionalita_utente` WRITE;
/*!40000 ALTER TABLE `t_funzionalita_utente` DISABLE KEYS */;
INSERT INTO `t_funzionalita_utente` VALUES (1,1,1,1),(2,1,2,1),(3,1,3,1),(4,1,4,1),(5,1,5,1),(6,1,9,1),(7,1,10,1),(8,1,11,1),(9,1,12,1),(10,2,1,1),(11,2,2,1),(12,2,3,1),(13,2,4,1),(14,2,5,1),(15,3,9,1),(16,3,10,1),(17,3,11,1),(18,3,12,1),(73,1,19,1),(74,3,19,1),(76,1,41,1),(77,1,42,1),(78,1,43,1),(79,1,44,1),(81,2,19,1),(82,2,41,1),(84,3,42,1),(85,3,43,1),(86,3,44,1),(87,2,45,1),(88,1,46,1),(89,2,46,1),(90,1,47,1),(91,2,47,1),(92,1,48,1),(93,2,48,1),(94,1,49,1),(95,2,49,1),(96,1,50,1),(97,2,50,1);
/*!40000 ALTER TABLE `t_funzionalita_utente` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_menu_principale`
--

DROP TABLE IF EXISTS `t_menu_principale`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `t_menu_principale` (
  `id` int NOT NULL AUTO_INCREMENT,
  `titolo` varchar(100) DEFAULT NULL,
  `label` varchar(100) DEFAULT NULL,
  `icon` varchar(100) DEFAULT NULL,
  `link` varchar(100) DEFAULT NULL,
  `ordinatore` int NOT NULL,
  `foto` varchar(255) DEFAULT NULL,
  `target` varchar(15) NOT NULL,
  `dataCancellazione` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_menu_principale`
--

LOCK TABLES `t_menu_principale` WRITE;
/*!40000 ALTER TABLE `t_menu_principale` DISABLE KEYS */;
INSERT INTO `t_menu_principale` VALUES (1,'RESILIENZA','Resilienza App','fas fa-shield-alt','/',1,NULL,'_self',NULL);
/*!40000 ALTER TABLE `t_menu_principale` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_ruolo`
--

DROP TABLE IF EXISTS `t_ruolo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `t_ruolo` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `public_id` varchar(255) DEFAULT NULL,
  `DESCR` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `public_id` (`public_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_ruolo`
--

LOCK TABLES `t_ruolo` WRITE;
/*!40000 ALTER TABLE `t_ruolo` DISABLE KEYS */;
INSERT INTO `t_ruolo` VALUES (1,'221099c7-1a42-455d-a205-b1a6201ff77b','Admin'),(2,'configuratore_public_id','Configuratore'),(3,'analista_public_id','Analista');
/*!40000 ALTER TABLE `t_ruolo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_tipi_utenti`
--

DROP TABLE IF EXISTS `t_tipi_utenti`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `t_tipi_utenti` (
  `id` int NOT NULL AUTO_INCREMENT,
  `public_id` varchar(255) DEFAULT NULL,
  `nomeTipoUtente` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `public_id` (`public_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_tipi_utenti`
--

LOCK TABLES `t_tipi_utenti` WRITE;
/*!40000 ALTER TABLE `t_tipi_utenti` DISABLE KEYS */;
/*!40000 ALTER TABLE `t_tipi_utenti` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_utenti`
--

DROP TABLE IF EXISTS `t_utenti`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `t_utenti` (
  `id` int NOT NULL AUTO_INCREMENT,
  `public_id` varchar(255) DEFAULT NULL,
  `username` varchar(50) NOT NULL,
  `nome` varchar(50) NOT NULL,
  `cognome` varchar(50) NOT NULL,
  `fkIdRuolo` int NOT NULL,
  `attivo` tinyint(1) DEFAULT NULL,
  `data_creazione` datetime DEFAULT NULL,
  `ultimo_accesso` datetime DEFAULT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `token` varchar(512) DEFAULT NULL,
  `expires` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_utenti_ruolo` (`fkIdRuolo`),
  CONSTRAINT `fk_utenti_ruolo` FOREIGN KEY (`fkIdRuolo`) REFERENCES `t_ruolo` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_utenti`
--

LOCK TABLES `t_utenti` WRITE;
/*!40000 ALTER TABLE `t_utenti` DISABLE KEYS */;
INSERT INTO `t_utenti` VALUES (4,'8e785b07-7728-493f-a3b5-25f61f10e98c','admin@example.com','Admin','User',1,1,'2025-07-16 17:29:21','2025-08-28 09:53:06','admin@example.com','pbkdf2:sha256:1000000$QIqLHlxWjg19Nk9q$ea55ec49ff236c06f7d0265a8f6109dcd34f33786eeb22446c990f0ae56df964',NULL,NULL),(5,'a015083c-6632-11f0-8ad7-00090ffe0001','configuratore@example.com','Luca','Verdi',2,1,'2025-07-21 15:00:06','2025-10-01 15:54:50','configuratore@example.com','pbkdf2:sha256:1000000$QIqLHlxWjg19Nk9q$ea55ec49ff236c06f7d0265a8f6109dcd34f33786eeb22446c990f0ae56df964',NULL,NULL),(6,'a2cdd2f8-6632-11f0-8ad7-00090ffe0001','analista@example.com','Anna','Neri',3,1,'2025-07-21 15:00:11','2025-08-26 15:10:32','analista@example.com','pbkdf2:sha256:1000000$QIqLHlxWjg19Nk9q$ea55ec49ff236c06f7d0265a8f6109dcd34f33786eeb22446c990f0ae56df964',NULL,NULL),(7,'0dda8f30-2cab-497c-8c14-9d1e8428f0d8','config@example.com','Config','User',2,1,'2025-07-22 10:29:21','2025-07-22 10:29:21','config@example.com','pbkdf2:sha256:1000000$uAwK1DqMJUCKr4Gv$dab580f79ce7dec3fb83d786f7ae462be507fa81e3cbad246e139aaf3e752d46',NULL,NULL);
/*!40000 ALTER TABLE `t_utenti` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'resilienza'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-10-01 16:36:35
