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
) ENGINE=InnoDB AUTO_INCREMENT=573 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ambito`
--

LOCK TABLES `ambito` WRITE;
/*!40000 ALTER TABLE `ambito` DISABLE KEYS */;
INSERT INTO `ambito` VALUES (1,'Commerciale','Riguarda tutte le attività di vendita e marketing.','COMM','2025-07-08 10:08:37','root@localhost'),(2,'Operativo','Gestisce le operazioni quotidiane e la logistica.','OPR','2025-07-08 10:08:37','root@localhost'),(3,'Finanziario','Si occupa della contabilità, bilancio e investimenti.','FIN','2025-07-08 10:08:37','root@localhost'),(4,'Risorse Umane','Gestisce il personale e le politiche HR.','HR','2025-07-08 10:08:37','root@localhost'),(5,'IT','Riguarda lo sviluppo software e la gestione infrastrutture','IT','2025-07-22 13:27:31','root@localhost'),(7,'Ambito new1','Ambito1 test1','NEW1','2025-07-22 13:30:23','root@localhost'),(10,'Ambito2','aaaaaaaaaa','NEW2','2025-07-22 15:01:21','root@localhost'),(11,'Ambito Default per Categorie','Creato per test','DEFAULT_AMB','2025-07-23 09:26:40','root@localhost'),(572,'IT & RISK assessment','','SPER','2025-11-11 11:13:43','root@localhost');
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
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categoria`
--

LOCK TABLES `categoria` WRITE;
/*!40000 ALTER TABLE `categoria` DISABLE KEYS */;
INSERT INTO `categoria` VALUES (1,'Marketing Digitale','Marketing',2,'2025-07-23 12:55:48','root@localhost'),(2,'Vendite B2B','Vendite',1,'2025-07-23 12:57:22','root@localhost'),(3,'Logistica Inbound','Logistica',2,'2025-07-08 10:09:36','root@localhost'),(4,'Gestione Magazzino','Logistica',1,'2025-07-23 12:56:56','root@localhost'),(5,'Contabilità Clienti','Contabilità',3,'2025-07-08 10:09:36','root@localhost'),(6,'Budgeting','Finanza',3,'2025-07-08 10:09:36','root@localhost'),(7,'Recruiting','HR',4,'2025-07-08 10:09:36','root@localhost'),(8,'Formazione Dipendenti','HR',4,'2025-07-08 10:09:36','root@localhost'),(9,'Sviluppo Software','IT',5,'2025-07-08 10:09:36','root@localhost'),(10,'Supporto Tecnico','IT',5,'2025-07-08 10:09:36','root@localhost'),(11,'Categoria Default per Domande','Default',1,'2025-07-25 16:00:09','root@localhost'),(26,'Categoria Default per Driver','Default',11,'2025-07-28 10:57:25','root@localhost'),(27,'Rete Informatica','Questa categoria si concentra sulla struttura, la segmentazione e le difese perimetrali della rete.',572,'2025-11-11 11:14:28','root@localhost'),(28,'Dotazioni Hardware e Software','Protezione e la standardizzazione dei dispositivi (Postazioni, Server, Periferiche).',572,'2025-11-11 11:15:53','root@localhost'),(29,'Sistemi operativi','Gestione del ciclo di vita e manutenzione di sicurezza dei sistemi operativi e software.',572,'2025-11-11 11:17:07','root@localhost'),(30,'Modalità di gestione dei backup e del disaster recovery','Affidabilità dei dati, disponibilità e capacità di ripristino in caso di incidente grave.',572,'2025-11-11 11:18:05','root@localhost'),(31,'Policy di sicurezza informatica e sistemi di difesa implementati','Quadro normativo interno, prevenzione e capacità di testare le difese.',572,'2025-11-11 11:18:58','root@localhost'),(32,'Gestione utenti, ruoli e accessi ai sistemi','Identità, credenziali e autorizzazioni all\'interno dell\'infrastruttura.',572,'2025-11-11 11:19:55','root@localhost'),(33,'Livello di conformità GDPR e linee guida AgID','Aderenza ai requisiti legali e regolamentari pertinenti.',572,'2025-11-11 11:20:47','root@localhost'),(34,'Organizzazione risorse ICT, interne o esterne, e loro capacità operativa','Governance, competenze e gestione dei fornitori esterni.',572,'2025-11-11 11:21:47','root@localhost');
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
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cliente`
--

LOCK TABLES `cliente` WRITE;
/*!40000 ALTER TABLE `cliente` DISABLE KEYS */;
INSERT INTO `cliente` VALUES (1,'Cliente1','12345678901',NULL,NULL,NULL,NULL,NULL,NULL,'2025-10-02 14:02:19',NULL),(2,'Cliente2','11111111112',NULL,NULL,NULL,NULL,NULL,NULL,'2025-10-29 16:17:23',NULL),(3,'Cesano Maderno - Comune','01234567890','Via Roma, 45','Cesano Maderno','MB','20100','contatti@cmaderno.it','0212345678','2025-11-17 11:50:35',NULL);
/*!40000 ALTER TABLE `cliente` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `correttiva`
--

DROP TABLE IF EXISTS `correttiva`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `correttiva` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `ID_PROGETTO_QUESTIONARIO_DOMANDA` int NOT NULL,
  `DESCRIZIONE_CORRETTIVA` text NOT NULL,
  `RESPONSABILE` varchar(100) DEFAULT NULL,
  `DATA_INSERIMENTO` datetime DEFAULT CURRENT_TIMESTAMP,
  `DATA_SCADENZA` date NOT NULL,
  `DATA_EFFETTIVA_INTERVENTO` date DEFAULT NULL,
  `STATO` enum('Aperta','In Corso','Completata','Pending','Annullata') NOT NULL DEFAULT 'Aperta',
  `COSTO` tinyint(1) DEFAULT '0',
  `NOTE` text,
  `MODIFICATO_DA` varchar(100) DEFAULT NULL,
  `DATA_ULTIMA_MODIFICA` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`ID`),
  KEY `fk_corr_pqd` (`ID_PROGETTO_QUESTIONARIO_DOMANDA`),
  CONSTRAINT `fk_corr_pqd` FOREIGN KEY (`ID_PROGETTO_QUESTIONARIO_DOMANDA`) REFERENCES `progetto_questionario_domanda` (`ID`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `correttiva`
--

LOCK TABLES `correttiva` WRITE;
/*!40000 ALTER TABLE `correttiva` DISABLE KEYS */;
INSERT INTO `correttiva` VALUES (2,71,'corr1','Max','2025-11-18 12:12:44','2025-12-31',NULL,'Aperta',1,'nota1','configuratore@example.com','2025-11-18 12:12:44');
/*!40000 ALTER TABLE `correttiva` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=153 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `domande`
--

LOCK TABLES `domande` WRITE;
/*!40000 ALTER TABLE `domande` DISABLE KEYS */;
INSERT INTO `domande` VALUES (1,'Quali sono le parole chiave più rilevanti per il nostro settore?',1,'2025-09-30 15:01:43','root@localhost',NULL),(2,'Come possiamo migliorare il posizionamento sui motori di ricerca?',1,'2025-10-01 14:04:44','root@localhost',NULL),(3,'Qual è il ROI delle nostre campagne SEM attuali?',2,'2025-07-08 10:12:03','root@localhost',NULL),(4,'Come possiamo ottimizzare le offerte CPC per massimizzare le conversioni?',2,'2025-07-08 10:12:03','root@localhost',NULL),(5,'Quale piattaforma di email marketing consigliate?',3,'2025-07-08 10:12:03','root@localhost',NULL),(6,'Come possiamo segmentare meglio la nostra lista email?',3,'2025-07-08 10:12:03','root@localhost',NULL),(7,'Quali sono le strategie più efficaci per la lead generation?',4,'2025-07-08 10:12:03','root@localhost',NULL),(8,'Come possiamo qualificati i lead in ingresso?',4,'2025-07-08 10:12:03','root@localhost',NULL),(9,'Quali sono i termini standard per i nostri contratti B2B?',5,'2025-07-08 10:12:03','root@localhost',NULL),(10,'Qual è il nostro tasso di successo nella chiusura dei contratti?',5,'2025-07-08 10:12:03','root@localhost',NULL),(11,'Come monitoriamo l\'efficienza della flotta?',6,'2025-07-08 10:12:03','root@localhost',NULL),(12,'Quali sono i costi di manutenzione della nostra flotta?',6,'2025-07-08 10:12:03','root@localhost',NULL),(13,'Come ottimizziamo i percorsi di consegna?',7,'2025-07-08 10:12:03','root@localhost',NULL),(14,'Quali software usiamo per la pianificazione dei percorsi?',7,'2025-07-08 10:12:03','root@localhost',NULL),(15,'Come gestiamo l\'inventario per evitare esaurimento scorte?',8,'2025-07-08 10:12:03','root@localhost',NULL),(16,'Qual è la nostra rotazione di magazzino media?',8,'2025-07-08 10:12:03','root@localhost',NULL),(17,'Quali standard di qualità adottiamo per i prodotti in ingresso?',9,'2025-07-08 10:12:03','root@localhost',NULL),(18,'Come gestiamo i resi per difetti di qualità?',9,'2025-07-08 10:12:03','root@localhost',NULL),(19,'Qual è il processo di fatturazione per i nuovi clienti?',10,'2025-07-08 10:12:03','root@localhost',NULL),(20,'Come gestiamo i crediti inesigibili?',10,'2025-07-08 10:12:03','root@localhost',NULL),(21,'Quali sono le procedure per la riconciliazione bancaria?',11,'2025-07-08 10:12:03','root@localhost',NULL),(22,'Come identifichiamo le discrepanze nei conti?',11,'2025-07-08 10:12:03','root@localhost',NULL),(23,'Quali sono le scadenze fiscali principali per quest\'anno?',12,'2025-07-08 10:12:03','root@localhost',NULL),(24,'Come possiamo ridurre l\'onere fiscale legalmente?',12,'2025-07-08 10:12:03','root@localhost',NULL),(25,'Come calcoliamo il costo di produzione per unità?',13,'2025-07-08 10:12:03','root@localhost',NULL),(26,'Quali sono i maggiori fattori di costo operativi?',13,'2025-07-08 10:12:03','root@localhost',NULL),(27,'Quali sono le migliori pratiche per condurre un colloquio?',14,'2025-07-08 10:12:03','root@localhost',NULL),(28,'Come valutiamo le competenze tecniche dei candidati?',14,'2025-07-08 10:12:03','root@localhost',NULL),(29,'Qual è il processo di onboarding per i nuovi assunti?',15,'2025-07-08 10:12:03','root@localhost',NULL),(30,'Come misuriamo l\'efficacia dell\'onboarding?',15,'2025-07-08 10:12:03','root@localhost',NULL),(31,'Quali corsi di aggiornamento sono obbligatori per il nostro personale?',16,'2025-07-08 10:12:03','root@localhost',NULL),(32,'Come valuti l\'impatto della formazione sulla produttività? ',16,'2025-07-28 10:35:56','root@localhost',NULL),(33,'Quali certificazioni IT sono richieste per il ruolo X?',17,'2025-07-08 10:12:03','root@localhost',NULL),(34,'Offriamo incentivi per l\'ottenimento di certificazioni?',17,'2025-07-08 10:12:03','root@localhost',NULL),(35,'Quali pattern di architettura software adottiamo?',18,'2025-07-08 10:12:03','root@localhost',NULL),(36,'Come garantiamo la scalabilità delle nostre applicazioni?',18,'2025-07-08 10:12:03','root@localhost',NULL),(37,'Quali strumenti usiamo per il debug del codice?',19,'2025-07-08 10:12:03','root@localhost',NULL),(38,'Come gestiamo i bug critici in produzione?',19,'2025-07-08 10:12:03','root@localhost',NULL),(39,'Qual è il SLA per le richieste di help desk?',20,'2025-07-08 10:12:03','root@localhost',NULL),(40,'Come misuriamo la soddisfazione degli utenti del supporto tecnico?',20,'2025-07-08 10:12:03','root@localhost',NULL),(41,'Qual è il processo di escalation per gli incidenti di livello 1?',21,'2025-07-08 10:12:03','root@localhost',NULL),(42,'Come documentiamo e analizziamo gli incidenti passati?',21,'2025-07-08 10:12:03','root@localhost',NULL),(49,'Domanda 1 Driver 1',1,'2025-08-28 13:44:39','root@localhost',NULL),(50,'Domanda 1 Driver 2',14,'2025-11-07 16:06:45','root@localhost',NULL),(51,'Domanda 2 Driver 1',1,'2025-08-28 13:44:39','root@localhost',NULL),(52,'Domanda 1 Driver 3',3,'2025-08-28 13:44:39','root@localhost',NULL),(53,'Domanda 2 Driver 2',2,'2025-08-28 13:44:39','root@localhost',NULL),(66,'La documentazione (diagrammi logici e fisici) dell\'infrastruttura di rete viene revisionata formalmente?',37,'2025-11-13 16:18:24','root@localhost',NULL),(67,'I servizi IT critici sono supportati da ridondanza (es. percorsi di rete alternativi o failover)?',37,'2025-11-13 16:18:48','root@localhost',NULL),(68,'La progettazione della rete include meccanismi integrati per la mitigazione di attacchi a livello infrastrutturale (es. DoS)?',37,'2025-11-13 16:19:00','root@localhost',NULL),(69,'La rete è segmentata (VLAN/Subnetting) per isolare i server critici e le aree ad alto rischio?',38,'2025-11-13 16:19:14','root@localhost',NULL),(70,'È in vigore una DMZ (Demilitarized Zone) per i server esposti su internet?',38,'2025-11-13 16:19:25','root@localhost',NULL),(71,'L\'accesso tra segmenti di rete diversi è controllato rigorosamente tramite ACL (Access Control Lists) basate sul minimo privilegio?',38,'2025-11-13 16:19:36','root@localhost',NULL),(72,'È implementato un sistema di IDS/IPS per il rilevamento e la prevenzione delle intrusioni al perimetro?',39,'2025-11-13 16:19:47','root@localhost',NULL),(73,'Con quale frequenza vengono aggiornate le firme e le policy dei sistemi di sicurezza perimetrale (Firewall, IDS/IPS)?',39,'2025-11-13 16:20:02','root@localhost',NULL),(74,'Il perimetro di sicurezza utilizza tecnologie avanzate (es. Sandboxing, Threat Intelligence) per la difesa?',39,'2025-11-13 16:20:13','root@localhost',NULL),(75,'L\'accesso remoto (VPN) richiede sempre l\'autenticazione Multi-Fattore (MFA)?',40,'2025-11-13 16:20:40','root@localhost',NULL),(76,'Con quale frequenza i protocolli e le configurazioni crittografiche della VPN vengono revisionati per la loro robustezza?',40,'2025-11-13 16:20:55','root@localhost',NULL),(77,'Le regole di accesso tramite VPN garantiscono il minimo accesso alle risorse strettamente necessarie (Zero Trust)?',40,'2025-11-13 16:21:11','root@localhost',NULL),(78,'La configurazione dei server prevede l\'Hardening (rimozione di servizi e funzionalità non necessari) ?',42,'2025-11-17 08:55:55','root@localhost',NULL),(79,'È implementata una soluzione EDR (Endpoint Detection and Response) sui server per la sicurezza avanzata?',42,'2025-11-17 08:56:23','root@localhost',NULL),(80,'La crittografia del disco (FDE) è implementata su tutti i server?',42,'2025-11-17 08:56:59','root@localhost',NULL),(81,'Tutte le postazioni di lavoro utilizzano l\'Autenticazione Multi-Fattore (MFA) per l\'accesso?',41,'2025-11-17 08:57:32','root@localhost',NULL),(82,'Tutti gli utenti di postazioni di lavoro operano senza privilegi amministrativi?',41,'2025-11-17 08:58:03','root@localhost',NULL),(83,'La crittografia del disco (BitLocker/FileVault) è implementata su tutte le postazioni di lavoro (inclusi i laptop)?',41,'2025-11-17 08:58:24','root@localhost',NULL),(84,'Esiste un sistema di controllo centralizzato per l\'utilizzo di periferiche (es. USB, dischi esterni)?',43,'2025-11-17 09:14:40','root@localhost',NULL),(85,'Il tuo ambiente utilizza supporti rimovibili crittografati (es. chiavette USB) per la conservazione dei dati?',43,'2025-11-17 09:14:53','root@localhost',NULL),(86,'Esiste una politica per la cancellazione sicura (wiping) dei dati sui supporti rimovibili prima della loro dismissione?',43,'2025-11-17 09:15:05','root@localhost',NULL),(87,'Le patch di sicurezza critiche per i sistemi operativi vengono applicate entro 48 ore dalla loro disponibilità?',45,'2025-11-17 09:15:54','root@localhost',NULL),(88,'Il processo di patching include una fase formale di test su un ambiente di staging o un gruppo pilota?',45,'2025-11-17 09:16:08','root@localhost',NULL),(89,'La distribuzione delle patch di sicurezza è un processo automatizzato (dall\'identificazione alla distribuzione)?',45,'2025-11-17 09:16:23','root@localhost',NULL),(90,'Quanti sistemi operativi o software chiave sono ancora in produzione pur essendo End-of-Life (EOL)?',44,'2025-11-17 09:16:54','root@localhost',NULL),(91,'Esiste un piano di migrazione proattivo e documentato per i sistemi che si avvicinano alla data EOL?',44,'2025-11-17 09:17:08','root@localhost',NULL),(92,'La politica aziendale richiede l\'utilizzo esclusivo di software con supporto attivo del produttore?',44,'2025-11-17 09:17:20','root@localhost',NULL),(93,'Le configurazioni predefinite (default) dei sistemi operativi e dei servizi sono state modificate per ragioni di sicurezza?',46,'2025-11-17 09:18:06','root@localhost',NULL),(94,'Le porte e i servizi di rete sono limitati a livello di Host Firewall per i sistemi in produzione?',46,'2025-11-17 09:18:21','root@localhost',NULL),(95,'I permessi di accesso ai file e alle directory critiche sono stati ridotti (hardening) rispetto alle impostazioni di default?',46,'2025-11-17 09:18:47','root@localhost',NULL),(96,'La tua strategia di backup rispetta la regola 3-2-1 (3 copie, 2 supporti, 1 off-site)?',47,'2025-11-17 09:19:20','root@localhost',NULL),(97,'Il backup off-site (o cloud) è configurato con immutabilità o \"air-gapped\" (disconnesso logicamente) per prevenire la manomissione?',47,'2025-11-17 09:19:30','root@localhost',NULL),(98,'Con quale frequenza viene creata la copia di backup off-site o offline dei dati critici?',47,'2025-11-17 09:19:41','root@localhost',NULL),(99,'Con quale frequenza i processi di ripristino (verifica che i dati siano leggibili) vengono testati formalmente?',48,'2025-11-17 09:20:06','root@localhost',NULL),(100,'Il test di ripristino include la misurazione effettiva del tempo necessario per recuperare il servizio?',48,'2025-11-17 09:20:15','root@localhost',NULL),(101,'Il personale è addestrato a eseguire le procedure di ripristino in caso di emergenza?',48,'2025-11-17 09:20:25','root@localhost',NULL),(102,'Sono stati formalmente definiti gli obiettivi RTO (tempo di ripristino) e RPO (punto di ripristino) per i servizi critici?',49,'2025-11-17 09:20:56','root@localhost',NULL),(103,'Qual è l\'RTO obiettivo per il servizio aziendale più critico (ad es. ERP/E-commerce)?',49,'2025-11-17 09:21:07','root@localhost',NULL),(104,'L\'RTO/RPO effettivo misurato nei test rispetta gli obiettivi definiti (deviazione < 25%)?',49,'2025-11-17 09:21:24','root@localhost',NULL),(105,'Sono state eseguite simulazioni di DR (Disaster Recovery) specificamente per scenari di Ransomware/Wiper?',50,'2025-11-17 09:21:49','root@localhost',NULL),(106,'Il Piano di Disaster Recovery (DRP) include procedure dedicate alla gestione di un ciberattacco mirato?',50,'2025-11-17 09:22:02','root@localhost',NULL),(107,'L\'infrastruttura di backup è progettata per essere isolata e immune da un attacco proveniente dalla rete di produzione?',50,'2025-11-17 09:22:16','root@localhost',NULL),(108,'Esiste un Documento Programmatico sulla Sicurezza (DPS) o equivalente (es. ISMS) formalmente approvato dal Management?',51,'2025-11-17 09:22:46','root@localhost',NULL),(109,'Le policy di sicurezza (es. uso accettabile) sono state diffuse e l\'accettazione da parte dei dipendenti è tracciata?',51,'2025-11-17 09:23:05','root@localhost',NULL),(110,'Le policy di sicurezza (es. blocco schermo) sono applicate forzatamente dal sistema (e non solo richieste)?',51,'2025-11-17 09:23:22','root@localhost',NULL),(111,'Qual è la frequenza dell\'esecuzione di una scansione di Vulnerability Assessment interna sull\'infrastruttura IT?',52,'2025-11-17 09:23:50','root@localhost',NULL),(112,'Viene eseguito un Penetration Testing di servizi o applicazioni critiche da parte di terze parti indipendenti?',52,'2025-11-17 09:24:04','root@localhost',NULL),(113,'È implementato un processo formale per la gestione e la correzione delle vulnerabilità (remediation)?',52,'2025-11-17 09:24:16','root@localhost',NULL),(114,'È implementata una soluzione di sicurezza avanzata come il Sandboxing per l\'analisi dei file (es. allegati email)?',53,'2025-11-17 09:24:41','root@localhost',NULL),(115,'I meccanismi di protezione del dominio (DMARC, DKIM, SPF) sono implementati e forzati per prevenire lo spoofing?',53,'2025-11-17 09:24:57','root@localhost',NULL),(116,'Quali strumenti di difesa avanzata (es. WAF, CASB, DLP) sono implementati oltre al Firewall?',53,'2025-11-17 09:25:09','root@localhost',NULL),(117,'Con quale frequenza vengono eseguite simulazioni di Phishing sui dipendenti?',54,'2025-11-17 09:25:31','root@localhost',NULL),(118,'Le simulazioni di sicurezza (es. Phishing) sono utilizzate per definire un training di sicurezza personalizzato?',54,'2025-11-17 09:25:44','root@localhost',NULL),(119,'Viene condotta un\'esercitazione di simulazione di incidente (es. Tabletop Exercise) che coinvolge il Management?',54,'2025-11-17 09:26:01','root@localhost',NULL),(120,'L\'Autenticazione Multi-Fattore (MFA) è implementata per tutti gli utenti e i servizi aziendali?',55,'2025-11-17 09:26:26','root@localhost',NULL),(121,'Quali metodi di MFA sono prioritari per l\'accesso?',55,'2025-11-17 09:26:38','root@localhost',NULL),(122,'Esiste un processo di revoca automatica e immediata (entro 1 ora) dell\'MFA in caso di cessazione del rapporto di lavoro?',55,'2025-11-17 09:26:57','root@localhost',NULL),(123,'Gli utenti hanno accesso solo ed esclusivamente alle risorse strettamente necessarie (minimo privilegio)?',56,'2025-11-17 09:27:24','root@localhost',NULL),(124,'È implementato un sistema di Privileged Access Management (PAM) per il monitoraggio degli account amministrativi?',56,'2025-11-17 09:27:35','root@localhost',NULL),(125,'Con quale frequenza vengono eseguiti audit per rimuovere i permessi in eccesso o obsoleti dagli utenti?',56,'2025-11-17 09:27:48','root@localhost',NULL),(126,'Le password richiedono una lunghezza minima di almeno 12 caratteri (o passphrase)?',57,'2025-11-17 09:28:26','root@localhost',NULL),(127,'La policy delle password impedisce il riutilizzo delle password precedenti (password history)?',57,'2025-11-17 09:28:42','root@localhost',NULL),(128,'Viene utilizzato un gestore di password (Password Manager) aziendale per la gestione delle credenziali?',57,'2025-11-17 09:29:01','root@localhost',NULL),(129,'Con quale frequenza viene condotta una revisione formale degli accessi da parte del Management/Responsabili?',58,'2025-11-17 09:29:27','root@localhost',NULL),(130,'Il processo di De-provisioning (revoca degli accessi) è automatizzato e scatta immediatamente alla cessazione del rapporto di lavoro?',58,'2025-11-17 09:29:40','root@localhost',NULL),(131,'La tracciabilità e la rendicontazione delle modifiche ai permessi sono garantite dal sistema di gestione degli accessi?',58,'2025-11-17 09:29:55','root@localhost',NULL),(132,'È stata definita una procedura per stabilire quando è obbligatorio condurre una DPIA (Data Protection Impact Assessment)?',60,'2025-11-17 09:35:39','root@localhost',NULL),(133,'Viene eseguita e documentata una DPIA per ogni nuovo progetto che introduce un alto rischio per i dati personali?',60,'2025-11-17 09:35:54','root@localhost',NULL),(134,'Le misure di mitigazione dei rischi identificate nella DPIA vengono implementate e monitorate formalmente?',60,'2025-11-17 09:36:07','root@localhost',NULL),(135,'La tua organizzazione ha adottato la Linea Guida AgID per la classificazione dei dati?',61,'2025-11-17 09:36:33','root@localhost',NULL),(136,'I servizi cloud utilizzati sono qualificati AgID (ove richiesto)?',61,'2025-11-17 09:36:46','root@localhost',NULL),(137,'L\'identità digitale (es. SPID/CIE) è utilizzata per l\'autenticazione ai servizi?',61,'2025-11-17 09:36:56','root@localhost',NULL),(138,'Esiste una procedura formale per la notifica delle violazioni di dati (Data Breach) entro le 72 ore?',62,'2025-11-17 09:37:30','root@localhost',NULL),(139,'Il piano di gestione incidenti (IRP) assegna chiaramente le responsabilità per la notifica all\'Autorità Garante?',62,'2025-11-17 09:37:46','root@localhost',NULL),(140,'Vengono conservati i registri di tutte le violazioni di dati personali (incluse quelle non notificate)?',62,'2025-11-17 09:38:02','root@localhost',NULL),(141,'Le responsabilità e l\'accountability (chi è responsabile per cosa) per ICT/Security sono chiaramente documentate (es. matrice RACI)?',63,'2025-11-17 09:38:31','root@localhost',NULL),(142,'Esiste una figura o un team dedicato (es. CISO) che ha la responsabilità unica e formale della sicurezza?',63,'2025-11-17 09:38:45','root@localhost',NULL),(143,'I conflitti di interesse (es. gestione e audit) sono prevenuti da una rigorosa Separazione dei Compiti (SoD)?',63,'2025-11-17 09:38:56','root@localhost',NULL),(144,'Con quale frequenza viene condotta un\'analisi del gap di competenze (skill gap) del personale ICT/Security?',64,'2025-11-17 09:39:16','root@localhost',NULL),(145,'Le competenze interne sono adeguate per gestire gli incidenti cyber più complessi (es. analisi forense)?',64,'2025-11-17 09:39:34','root@localhost',NULL),(146,'È in vigore un piano di formazione continua e obbligatorio per il personale IT/Security sulle nuove minacce?',64,'2025-11-17 09:39:46','root@localhost',NULL),(147,'Viene condotta una valutazione di rischio di sicurezza sui fornitori di servizi critici prima della stipula del contratto?',65,'2025-11-17 09:40:25','root@localhost',NULL),(148,'Con quale frequenza viene effettuato il monitoraggio della sicurezza dei fornitori di terze parti critici (es. audit/dashboard)?',65,'2025-11-17 09:40:37','root@localhost',NULL),(149,'I contratti con i fornitori includono clausole specifiche (es. SLA) in merito alla notifica immediata di un Data Breach?',65,'2025-11-17 09:40:48','root@localhost',NULL),(150,'Sono state formalizzate e documentate le procedure operative standard per la gestione degli incidenti cyber?',66,'2025-11-17 09:41:17','root@localhost',NULL),(151,'Con quale frequenza vengono condotte esercitazioni simulate di incidente (Tabletop) per testare la prontezza operativa?',66,'2025-11-17 09:41:28','root@localhost',NULL),(152,'Le risorse dedicate alla gestione degli incidenti (Incident Handlers) sono disponibili 24/7 per i servizi critici?',66,'2025-11-17 09:41:39','root@localhost',NULL);
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
INSERT INTO `domande_questionario` VALUES (1,1),(4,1),(5,1),(6,1),(7,1),(2,2),(3,2),(1,3),(2,3),(3,3),(2,4),(7,4),(3,5),(6,5),(7,6),(6,7),(6,9),(6,11),(6,12),(6,13),(6,14),(3,15),(3,16),(4,16),(6,16),(5,17),(6,21),(4,36),(3,50),(2,51),(3,52),(8,66),(8,67),(8,68),(8,69),(8,70),(8,71),(8,72),(8,73),(8,74),(8,75),(8,76),(8,77),(8,78),(8,79),(8,80),(8,81),(8,82),(8,83),(8,84),(8,85),(8,86),(8,87),(8,88),(8,89),(8,90),(8,91),(8,92),(8,93),(8,94),(8,95),(8,96),(8,97),(8,98),(8,99),(8,100),(8,101),(8,102),(8,103),(8,104),(8,105),(8,106),(8,107),(8,108),(8,109),(8,110),(8,111),(8,112),(8,113),(8,114),(8,115),(8,116),(8,117),(8,118),(8,119),(8,120),(8,121),(8,122),(8,123),(8,124),(8,125),(8,126),(8,127),(8,128),(8,129),(8,130),(8,131),(8,132),(8,133),(8,134),(8,135),(8,136),(8,137),(8,138),(8,139),(8,140),(8,141),(8,142),(8,143),(8,144),(8,145),(8,146),(8,147),(8,148),(8,149),(8,150),(8,151),(8,152);
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
) ENGINE=InnoDB AUTO_INCREMENT=67 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `driver`
--

LOCK TABLES `driver` WRITE;
/*!40000 ALTER TABLE `driver` DISABLE KEYS */;
INSERT INTO `driver` VALUES (1,'SEO',1,'2025-07-08 10:10:46','root@localhost'),(2,'SEM',1,'2025-07-08 10:10:46','root@localhost'),(3,'Email Marketing',1,'2025-07-08 10:10:46','root@localhost'),(4,'Lead Generation',2,'2025-07-08 10:10:46','root@localhost'),(5,'Negoziazione Contratti',2,'2025-07-08 10:10:46','root@localhost'),(6,'Gestione Flotta',3,'2025-07-08 10:10:46','root@localhost'),(7,'Ottimizzazione Percorsi',3,'2025-07-08 10:10:46','root@localhost'),(8,'Inventario',4,'2025-07-08 10:10:46','root@localhost'),(9,'Controllo Qualità Prodotti',4,'2025-07-08 10:10:46','root@localhost'),(10,'Fatturazione',5,'2025-07-08 10:10:46','root@localhost'),(11,'Riconciliazione Conti',5,'2025-07-08 10:10:46','root@localhost'),(12,'Pianificazione Fiscale',6,'2025-07-08 10:10:46','root@localhost'),(13,'Analisi di Costo',6,'2025-07-08 10:10:46','root@localhost'),(14,'Colloqui',7,'2025-07-08 10:10:46','root@localhost'),(15,'Onboarding',7,'2025-07-08 10:10:46','root@localhost'),(16,'Corsi di Aggiornamento',8,'2025-07-08 10:10:46','root@localhost'),(17,'Certificazioni IT',8,'2025-07-08 10:10:46','root@localhost'),(18,'Architettura Software',9,'2025-07-08 10:10:46','root@localhost'),(19,'Debug Codice',9,'2025-07-08 10:10:46','root@localhost'),(20,'Help Desk',10,'2025-07-08 10:10:46','root@localhost'),(21,'Gestione Incidenti',10,'2025-07-08 10:10:46','root@localhost'),(22,'Driver Default per Domande',11,'2025-07-25 16:00:09','root@localhost'),(37,'Topologia - Disponibilità e accuratezza dei diagrammi di rete (logici e fisici). Livello di ridondanza (assenza di SPOF) e implementazione del Quality of Service (QoS).',27,'2025-11-11 11:25:01','root@localhost'),(38,'Segmentazione - Efficacia della separazione logica (VLAN/Subnetting) per isolare le aree critiche (server, ospiti, DMZ) e controllo dell\'accesso tra segmenti (ACL).',27,'2025-11-11 11:24:32','root@localhost'),(39,'Sicurezza Perimetrale - Efficacia e aggiornamento delle configurazioni di Firewall e dei sistemi IDS/IPS.',27,'2025-11-11 11:25:41','root@localhost'),(40,'Sicurezza VPN - Robustezza protocolli crittografici e integrazione MFA per accessi remoti.',27,'2025-11-11 11:28:34','root@localhost'),(41,'Postazioni di Lavoro (Endpoint) - Livello di standardizzazione delle configurazioni, aggiornamento EDR/Antivirus, Crittografia del Disco (FDE).',28,'2025-11-11 11:30:31','root@localhost'),(42,'Server - Hardening e gestione sicura delle piattaforme di Virtualizzazione (Hypervisor).',28,'2025-11-11 11:30:40','root@localhost'),(43,'Periferiche - Controllo e tracciabilità degli accessi fisici alle periferiche critiche.',28,'2025-11-11 11:30:52','root@localhost'),(44,'Ciclo di Vita e Supporto - Percentuale di sistemi operativi in uso che sono ancora supportati dal produttore (non End-of-Life).',29,'2025-11-11 11:32:04','root@localhost'),(45,'Patch Management - Frequenza, automazione e tasso di successo nell\'applicazione tempestiva delle patch di sicurezza a SO e applicazioni.',29,'2025-11-11 11:32:15','root@localhost'),(46,'Configurazioni di Default - Grado di rimozione o modifica delle configurazioni di sicurezza predefinite (hardening).',29,'2025-11-11 11:32:28','root@localhost'),(47,'Regola 3-2-1 - Conformità alla regola di conservazione (3 copie, 2 supporti diversi, 1 copia off-site/offline o immutabile).',30,'2025-11-11 11:33:36','root@localhost'),(48,'Test di Ripristino - Frequenza e successo dei test di ripristino per verificarne l\'integrità.',30,'2025-11-11 11:33:48','root@localhost'),(49,'RTO e RPO - Chiarezza e misurabilità degli obiettivi di Recovery Time Objective (RTO) e Recovery Point Objective (RPO) per le applicazioni critiche.',30,'2025-11-11 11:34:00','root@localhost'),(50,'Scenario Ciberattacco - Inclusione e test di scenari specifici di ciberattacco (es. ransomware) nel Piano di DR.',30,'2025-11-11 11:34:12','root@localhost'),(51,'Policy Formale - Documento Programmatico sulla Sicurezza (DPS) o di un Policy Framework aziendale.',31,'2025-11-11 11:42:37','root@localhost'),(52,'Vulnerability Management - Frequenza e metodologia di esecuzione di Vulnerability Assessment e Penetration Testing (Pentest).',31,'2025-11-11 11:42:48','root@localhost'),(53,'Difese Proattive - Implementazione di sistemi di Sandboxing e analisi avanzate per la rilevazione di minacce sconosciute o zero-day.',31,'2025-11-11 11:43:00','root@localhost'),(54,'Simulazioni - Esecuzione periodica di simulazioni di phishing e di esercitazioni tabletop per la risposta agli incidenti.',31,'2025-11-11 11:43:11','root@localhost'),(55,'Autenticazione MultiFattore (MFA) - Percentuale di account (critici, remoti) che utilizzano l\'MFA e robustezza dei metodi utilizzati.',32,'2025-11-11 11:44:58','root@localhost'),(56,'Principio del Minimo Privilegio - Granularità delle autorizzazioni (accesso strettamente necessario) e gestione account privilegiati (PAM).',32,'2025-11-11 11:45:07','root@localhost'),(57,'Policy Password - Rigore (lunghezza minima, complessità, blocco riutilizzo) e sicurezza nell\'archiviazione delle password (hashing robusto).',32,'2025-11-11 11:45:18','root@localhost'),(58,'Revisione Accessi - Frequenza e formalità della revisione degli account e delle autorizzazioni ',32,'2025-11-11 11:45:27','root@localhost'),(59,'Data Inventory e Mappatura - Mappatura e classificazione di tutti i dati personali e sensibili gestiti (GDPR).',33,'2025-11-11 11:47:04','root@localhost'),(60,'DPIA - Documentazione del Data Protection Impact Assessment (DPIA) per i trattamenti ad alto rischio.',33,'2025-11-11 11:47:13','root@localhost'),(61,'Requisiti AgID - Linee Guida AgID per i servizi cloud, dematerializzazione e identità digitale (ove applicabile).',33,'2025-11-11 11:47:30','root@localhost'),(62,'Gestione delle Violazioni - Esistenza di una procedura formalizzata per notifica violazione dati(Data Breach) alle autorità competenti entro 72 ore (GDPR).',33,'2025-11-11 11:47:41','root@localhost'),(63,'Organigramma e Ruoli - Definizione chiara e documentata delle responsabilità ICT e del processo decisionale.',34,'2025-11-11 11:48:39','root@localhost'),(64,'Skillset - Livello di competenza del personale ICT in materia di sicurezza (certificazioni, formazione continua).',34,'2025-11-11 11:48:47','root@localhost'),(65,'Gestione dei Fornitori (Third-Party Risk) - Procedure di valutazione del rischio di sicurezza per i fornitori e partner esterni che accedono all\'infrastruttura.',34,'2025-11-11 11:48:58','root@localhost'),(66,'Capacità Operativa - Disponibilità di risorse (interne o esterne) per la gestione degli incidenti 24/7 e il mantenimento dei sistemi critici.',34,'2025-11-11 11:49:09','root@localhost');
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
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Tabella per la gestione dei gruppi di risposte.';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gruppo_risposta`
--

LOCK TABLES `gruppo_risposta` WRITE;
/*!40000 ALTER TABLE `gruppo_risposta` DISABLE KEYS */;
INSERT INTO `gruppo_risposta` VALUES (13,'Frequenza - Continuità','configuratore@example.com','2025-11-17 14:31:02'),(14,'Implementazione - Qualità','configuratore@example.com','2025-11-17 15:45:06'),(15,'Stato EOL e Rischio','configuratore@example.com','2025-11-17 15:48:48'),(16,'Metodologia e Standard','configuratore@example.com','2025-11-17 15:50:33'),(17,'Si - Positivo','configuratore@example.com','2025-11-17 16:06:49');
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
INSERT INTO `gruppo_risposta_risposta` VALUES (13,39),(13,40),(13,41),(13,42),(13,43),(14,44),(14,45),(14,46),(14,47),(14,48),(15,49),(15,50),(15,51),(15,52),(16,53),(16,54),(16,55),(16,56),(16,57),(17,59),(17,60),(17,61);
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
  `ID_CLIENTE` int NOT NULL,
  `REF_CLIENTE` varchar(200) DEFAULT NULL,
  `MODIFICATO_DA` varchar(100) DEFAULT NULL,
  `DATA_ULTIMA_MODIFICA` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`ID`),
  KEY `ID_AMBITO` (`ID_AMBITO`),
  KEY `fk_progetto_cliente` (`ID_CLIENTE`),
  KEY `fk_progetto_stato` (`ID_STATO`),
  CONSTRAINT `fk_progetto_cliente` FOREIGN KEY (`ID_CLIENTE`) REFERENCES `cliente` (`ID`),
  CONSTRAINT `fk_progetto_stato` FOREIGN KEY (`ID_STATO`) REFERENCES `stati_progetto` (`ID`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `progetto_ibfk_1` FOREIGN KEY (`ID_AMBITO`) REFERENCES `ambito` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `progetto`
--

LOCK TABLES `progetto` WRITE;
/*!40000 ALTER TABLE `progetto` DISABLE KEYS */;
INSERT INTO `progetto` VALUES (12,'proj2','2025-01-11','2025-12-31',1,5,1,NULL,'configuratore@example.com','2025-10-14 10:56:58'),(14,'proj3','2025-10-10','2025-12-31',2,10,1,'ugo','configuratore@example.com','2025-10-14 13:32:13'),(15,'Assessment Cesano Maderno','2025-11-17','2025-12-31',1,1,3,'Apollieni','configuratore@example.com','2025-11-17 11:51:47');
/*!40000 ALTER TABLE `progetto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `progetto_questionario`
--

DROP TABLE IF EXISTS `progetto_questionario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `progetto_questionario` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `ID_PROGETTO` int NOT NULL,
  `ID_QUESTIONARIO` int NOT NULL,
  `DATA_ASSOCIAZIONE` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`ID`),
  KEY `fk_pq_progetto` (`ID_PROGETTO`),
  KEY `fk_pq_questionario` (`ID_QUESTIONARIO`),
  CONSTRAINT `fk_pq_progetto` FOREIGN KEY (`ID_PROGETTO`) REFERENCES `progetto` (`ID`) ON DELETE CASCADE,
  CONSTRAINT `fk_pq_questionario` FOREIGN KEY (`ID_QUESTIONARIO`) REFERENCES `questionario` (`ID`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `progetto_questionario`
--

LOCK TABLES `progetto_questionario` WRITE;
/*!40000 ALTER TABLE `progetto_questionario` DISABLE KEYS */;
INSERT INTO `progetto_questionario` VALUES (6,12,3,'2025-10-17 16:30:14'),(8,14,2,'2025-10-21 17:54:08'),(9,15,8,'2025-11-17 12:53:26');
/*!40000 ALTER TABLE `progetto_questionario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `progetto_questionario_domanda`
--

DROP TABLE IF EXISTS `progetto_questionario_domanda`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `progetto_questionario_domanda` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `ID_PROGETTO_QUESTIONARIO` int NOT NULL,
  `ID_DOMANDA` int NOT NULL,
  `ID_GRUPPO_RISPOSTA` int DEFAULT NULL,
  PRIMARY KEY (`ID`),
  KEY `fk_pqd_pq` (`ID_PROGETTO_QUESTIONARIO`),
  KEY `fk_pqd_domanda` (`ID_DOMANDA`),
  KEY `fk_pqd_gruppo_risposta` (`ID_GRUPPO_RISPOSTA`),
  CONSTRAINT `fk_pqd_domanda` FOREIGN KEY (`ID_DOMANDA`) REFERENCES `domande` (`ID`) ON DELETE CASCADE,
  CONSTRAINT `fk_pqd_gruppo_risposta` FOREIGN KEY (`ID_GRUPPO_RISPOSTA`) REFERENCES `gruppo_risposta` (`ID_GRUPPO_RISPOSTA`) ON DELETE CASCADE,
  CONSTRAINT `fk_pqd_pq` FOREIGN KEY (`ID_PROGETTO_QUESTIONARIO`) REFERENCES `progetto_questionario` (`ID`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=103 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `progetto_questionario_domanda`
--

LOCK TABLES `progetto_questionario_domanda` WRITE;
/*!40000 ALTER TABLE `progetto_questionario_domanda` DISABLE KEYS */;
INSERT INTO `progetto_questionario_domanda` VALUES (16,9,66,16),(17,9,67,16),(18,9,68,16),(19,9,69,16),(20,9,70,17),(21,9,71,17),(22,9,72,16),(23,9,73,13),(24,9,74,17),(25,9,75,17),(26,9,76,13),(27,9,77,16),(28,9,78,17),(29,9,79,17),(30,9,80,17),(31,9,81,17),(32,9,82,17),(33,9,83,17),(34,9,84,17),(35,9,85,17),(36,9,86,17),(37,9,87,17),(38,9,88,17),(39,9,89,17),(40,9,90,15),(41,9,91,17),(42,9,92,17),(43,9,93,17),(44,9,94,17),(45,9,95,17),(46,9,96,17),(47,9,97,17),(48,9,98,13),(49,9,99,13),(50,9,100,17),(51,9,101,17),(52,9,102,16),(53,9,103,16),(54,9,104,17),(55,9,105,17),(56,9,106,17),(57,9,107,17),(58,9,108,17),(59,9,109,17),(60,9,110,17),(61,9,111,13),(62,9,112,16),(63,9,113,17),(64,9,114,17),(65,9,115,15),(66,9,116,17),(67,9,117,13),(68,9,118,17),(69,9,119,17),(70,9,120,17),(71,9,121,17),(72,9,122,17),(73,9,123,17),(74,9,124,17),(75,9,125,13),(76,9,126,17),(77,9,127,17),(78,9,128,17),(79,9,129,13),(80,9,130,17),(81,9,131,17),(82,9,132,17),(83,9,133,17),(84,9,134,17),(85,9,135,17),(86,9,136,17),(87,9,137,17),(88,9,138,17),(89,9,139,17),(90,9,140,17),(91,9,141,17),(92,9,142,17),(93,9,143,17),(94,9,144,13),(95,9,145,17),(96,9,146,17),(97,9,147,17),(98,9,148,13),(99,9,149,17),(100,9,150,17),(101,9,151,13),(102,9,152,17);
/*!40000 ALTER TABLE `progetto_questionario_domanda` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `progetto_questionario_punteggio`
--

DROP TABLE IF EXISTS `progetto_questionario_punteggio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `progetto_questionario_punteggio` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `ID_PROGETTO` int NOT NULL COMMENT 'Chiave esterna per la tabella progetto',
  `ID_QUESTIONARIO` int NOT NULL COMMENT 'Chiave esterna per la tabella questionario',
  `ID_CLIENTE` int NOT NULL COMMENT 'Chiave esterna per la tabella cliente',
  `ID_PROGETTO_QUESTIONARIO` int NOT NULL COMMENT 'ID della riga di associazione (Progetto, Questionario) che ha generato il calcolo',
  `ID_CATEGORIA` int NOT NULL COMMENT 'Chiave esterna per la tabella categoria',
  `PESO_TOTALE` decimal(10,2) NOT NULL COMMENT 'Somma dei pesi delle risposte per categoria',
  `DATA_CHIUSURA` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`ID`),
  KEY `fk_pqp_progetto` (`ID_PROGETTO`),
  KEY `fk_pqp_questionario` (`ID_QUESTIONARIO`),
  KEY `fk_pqp_cliente` (`ID_CLIENTE`),
  KEY `fk_pqp_pq` (`ID_PROGETTO_QUESTIONARIO`),
  KEY `fk_pqp_categoria` (`ID_CATEGORIA`),
  CONSTRAINT `fk_pqp_categoria` FOREIGN KEY (`ID_CATEGORIA`) REFERENCES `categoria` (`ID`) ON DELETE CASCADE,
  CONSTRAINT `fk_pqp_cliente` FOREIGN KEY (`ID_CLIENTE`) REFERENCES `cliente` (`ID`) ON DELETE CASCADE,
  CONSTRAINT `fk_pqp_pq` FOREIGN KEY (`ID_PROGETTO_QUESTIONARIO`) REFERENCES `progetto_questionario` (`ID`) ON DELETE CASCADE,
  CONSTRAINT `fk_pqp_progetto` FOREIGN KEY (`ID_PROGETTO`) REFERENCES `progetto` (`ID`) ON DELETE CASCADE,
  CONSTRAINT `fk_pqp_questionario` FOREIGN KEY (`ID_QUESTIONARIO`) REFERENCES `questionario` (`ID`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=48 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `progetto_questionario_punteggio`
--

LOCK TABLES `progetto_questionario_punteggio` WRITE;
/*!40000 ALTER TABLE `progetto_questionario_punteggio` DISABLE KEYS */;
INSERT INTO `progetto_questionario_punteggio` VALUES (21,14,2,1,8,1,3.00,'2025-11-07 17:18:48'),(37,12,3,1,6,1,5.00,'2025-11-10 12:07:07'),(38,12,3,1,6,7,1.00,'2025-11-10 12:07:07'),(39,12,3,1,6,4,2.00,'2025-11-10 12:07:07'),(40,15,8,3,9,34,21.00,'2025-11-17 16:19:51'),(41,15,8,3,9,27,27.00,'2025-11-17 16:19:51'),(42,15,8,3,9,30,21.00,'2025-11-17 16:19:51'),(43,15,8,3,9,31,19.00,'2025-11-17 16:19:51'),(44,15,8,3,9,32,18.00,'2025-11-17 16:19:51'),(45,15,8,3,9,29,7.00,'2025-11-17 16:19:51'),(46,15,8,3,9,28,13.00,'2025-11-17 16:19:51'),(47,15,8,3,9,33,11.00,'2025-11-17 16:19:51');
/*!40000 ALTER TABLE `progetto_questionario_punteggio` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `questionario`
--

LOCK TABLES `questionario` WRITE;
/*!40000 ALTER TABLE `questionario` DISABLE KEYS */;
INSERT INTO `questionario` VALUES (1,'q1','2025-09-02 15:48:50','Utente di test','2025-10-15 10:38:08','configuratore@example.com'),(2,'q2','2025-09-02 15:53:26','Utente di test','2025-11-10 09:46:47',NULL),(3,'q3','2025-09-08 09:25:26','Utente di test','2025-11-10 09:47:04',NULL),(4,'q4','2025-09-08 13:30:38','Utente di test','2025-11-10 09:47:27',NULL),(5,'q5','2025-09-08 13:46:09','Utente di test',NULL,NULL),(6,'q6','2025-09-09 10:09:49','Utente di test','2025-10-20 13:44:55','configuratore@example.com'),(7,'q7','2025-10-15 09:16:26','Utente di test','2025-11-10 09:48:19','configuratore@example.com'),(8,'IT & Risk Assessment','2025-11-17 09:42:55','Utente di test','2025-11-17 11:27:02','configuratore@example.com');
/*!40000 ALTER TABLE `questionario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `questionario_cliente_old`
--

DROP TABLE IF EXISTS `questionario_cliente_old`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `questionario_cliente_old` (
  `ID_QUESTIONARIO` int NOT NULL,
  `ID_CLIENTE` int NOT NULL,
  PRIMARY KEY (`ID_QUESTIONARIO`,`ID_CLIENTE`),
  KEY `fk_qc_cliente` (`ID_CLIENTE`),
  CONSTRAINT `fk_qc_cliente` FOREIGN KEY (`ID_CLIENTE`) REFERENCES `cliente` (`ID`) ON DELETE CASCADE,
  CONSTRAINT `fk_qc_questionario` FOREIGN KEY (`ID_QUESTIONARIO`) REFERENCES `questionario` (`ID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `questionario_cliente_old`
--

LOCK TABLES `questionario_cliente_old` WRITE;
/*!40000 ALTER TABLE `questionario_cliente_old` DISABLE KEYS */;
/*!40000 ALTER TABLE `questionario_cliente_old` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `questionario_domande_old`
--

DROP TABLE IF EXISTS `questionario_domande_old`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `questionario_domande_old` (
  `id_questionario` int DEFAULT NULL,
  `id_domanda` int DEFAULT NULL,
  KEY `id_questionario` (`id_questionario`),
  KEY `id_domanda` (`id_domanda`),
  CONSTRAINT `questionario_domande_old_ibfk_1` FOREIGN KEY (`id_questionario`) REFERENCES `questionario` (`ID`),
  CONSTRAINT `questionario_domande_old_ibfk_2` FOREIGN KEY (`id_domanda`) REFERENCES `domande` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `questionario_domande_old`
--

LOCK TABLES `questionario_domande_old` WRITE;
/*!40000 ALTER TABLE `questionario_domande_old` DISABLE KEYS */;
INSERT INTO `questionario_domande_old` VALUES (1,53),(1,4),(1,3),(1,49);
/*!40000 ALTER TABLE `questionario_domande_old` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=62 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Tabella per la gestione delle risposte associate ai gruppi di risposte.';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `risposta`
--

LOCK TABLES `risposta` WRITE;
/*!40000 ALTER TABLE `risposta` DISABLE KEYS */;
INSERT INTO `risposta` VALUES (39,'Mai / No / Non tracciato',NULL,'2025-11-17 14:37:27',1.00),(40,'Annualmente / Solo su richiesta / Mesi (>6)',NULL,'2025-11-17 14:32:13',2.00),(41,'Semestralmente / Pochi (<3) / Mesi (3-6)',NULL,'2025-11-17 14:35:40',3.00),(42,'Trimestralmente / Settimanale / Qualcuno (3-10)',NULL,'2025-11-17 14:37:46',4.00),(43,'Mensile / Quotidiana / Continua / Immediata / Molti (>10)',NULL,'2025-11-17 14:36:06',5.00),(44,'No / Nessuno / Nessuna / Solo manuale',NULL,'2025-11-17 15:45:27',1.00),(45,'Parzialmente / Sì, ma generiche / Incompleto / Base',NULL,'2025-11-17 15:45:40',2.00),(46,'Sì, per la maggior parte / Abbastanza completo / Avanzato',NULL,'2025-11-17 15:45:50',3.00),(47,'Sì, rigorosamente / Completo / Totalmente automatizzato',NULL,'2025-11-17 15:46:01',4.00),(48,'Sì, formale e testato / Completo e continuo',NULL,'2025-11-17 15:46:14',5.00),(49,'Molti (>10) / Obiettivo mancato / No',NULL,'2025-11-17 15:49:09',1.00),(50,'Qualcuno (3-10) / No, solo teoriche',NULL,'2025-11-17 15:49:27',2.00),(51,'Pochi (<3) / Parzialmente / Non tracciato',NULL,'2025-11-17 15:49:45',3.00),(52,'Nessuno / Sì, con ripristino effettivo / Sì',NULL,'2025-11-17 15:50:07',4.00),(53,'No (installazione diretta/solo teorica) / Niente',NULL,'2025-11-17 15:50:50',1.00),(54,'Sì, su un gruppo pilota / Sì, solo informale',NULL,'2025-11-17 15:51:05',2.00),(55,'Sì, su ambiente di staging / Formale e documentata',NULL,'2025-11-17 15:51:17',3.00),(56,'Sì, con misurazione RTO / Con procedure dettagliate',NULL,'2025-11-17 15:51:36',4.00),(57,'Test live/completo / Formale e tracciata / Rigorosa',NULL,'2025-11-17 15:51:55',5.00),(59,'Sì',NULL,'2025-11-17 16:07:06',1.00),(60,'No',NULL,'2025-11-17 16:07:17',2.00),(61,'N/A',NULL,'2025-11-17 16:07:32',0.00);
/*!40000 ALTER TABLE `risposta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `risposta_cliente`
--

DROP TABLE IF EXISTS `risposta_cliente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `risposta_cliente` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `ID_PROGETTO_QUESTIONARIO_DOMANDA` int NOT NULL,
  `ID_RISPOSTA` int NOT NULL,
  `DATA_COMPILAZIONE` datetime DEFAULT CURRENT_TIMESTAMP,
  `MODIFICATO_DA` varchar(100) DEFAULT NULL,
  `DATA_ULTIMA_MODIFICA` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`ID`),
  KEY `fk_rc_pqd` (`ID_PROGETTO_QUESTIONARIO_DOMANDA`),
  KEY `fk_rc_risposta` (`ID_RISPOSTA`),
  CONSTRAINT `fk_rc_pqd` FOREIGN KEY (`ID_PROGETTO_QUESTIONARIO_DOMANDA`) REFERENCES `progetto_questionario_domanda` (`ID`) ON DELETE CASCADE,
  CONSTRAINT `fk_rc_risposta` FOREIGN KEY (`ID_RISPOSTA`) REFERENCES `risposta` (`ID_RISPOSTA`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=100 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `risposta_cliente`
--

LOCK TABLES `risposta_cliente` WRITE;
/*!40000 ALTER TABLE `risposta_cliente` DISABLE KEYS */;
INSERT INTO `risposta_cliente` VALUES (13,16,56,'2025-11-17 16:16:47','configuratore@example.com','2025-11-17 16:16:47'),(14,17,54,'2025-11-17 16:16:47','configuratore@example.com','2025-11-17 16:16:47'),(15,18,53,'2025-11-17 16:16:47','configuratore@example.com','2025-11-17 16:16:47'),(16,19,55,'2025-11-17 16:16:47','configuratore@example.com','2025-11-17 16:16:47'),(17,20,60,'2025-11-17 16:16:47','configuratore@example.com','2025-11-17 16:16:47'),(18,21,60,'2025-11-17 16:18:08','configuratore@example.com','2025-11-17 16:18:08'),(19,22,54,'2025-11-17 16:18:08','configuratore@example.com','2025-11-17 16:18:08'),(20,23,40,'2025-11-17 16:18:08','configuratore@example.com','2025-11-17 16:18:08'),(21,24,61,'2025-11-17 16:18:08','configuratore@example.com','2025-11-17 16:18:08'),(22,25,60,'2025-11-17 16:18:08','configuratore@example.com','2025-11-17 16:18:08'),(23,26,41,'2025-11-17 16:18:08','configuratore@example.com','2025-11-17 16:18:08'),(24,27,56,'2025-11-17 16:18:08','configuratore@example.com','2025-11-17 16:18:08'),(25,28,59,'2025-11-17 16:18:08','configuratore@example.com','2025-11-17 16:18:08'),(26,29,59,'2025-11-17 16:18:08','configuratore@example.com','2025-11-17 16:18:08'),(27,30,59,'2025-11-17 16:18:08','configuratore@example.com','2025-11-17 16:18:08'),(28,31,60,'2025-11-17 16:18:08','configuratore@example.com','2025-11-17 16:18:08'),(29,32,60,'2025-11-17 16:18:08','configuratore@example.com','2025-11-17 16:18:08'),(30,33,60,'2025-11-17 16:18:08','configuratore@example.com','2025-11-17 16:18:08'),(31,34,60,'2025-11-17 16:18:08','configuratore@example.com','2025-11-17 16:18:08'),(32,35,60,'2025-11-17 16:18:08','configuratore@example.com','2025-11-17 16:18:08'),(33,36,61,'2025-11-17 16:18:08','configuratore@example.com','2025-11-17 16:18:08'),(34,37,61,'2025-11-17 16:18:08','configuratore@example.com','2025-11-17 16:18:08'),(35,38,60,'2025-11-17 16:18:08','configuratore@example.com','2025-11-17 16:18:08'),(36,39,61,'2025-11-17 16:18:08','configuratore@example.com','2025-11-17 16:18:08'),(37,40,50,'2025-11-17 16:18:08','configuratore@example.com','2025-11-17 16:18:08'),(38,41,61,'2025-11-17 16:18:08','configuratore@example.com','2025-11-17 16:18:08'),(39,42,60,'2025-11-17 16:18:08','configuratore@example.com','2025-11-17 16:18:08'),(40,43,61,'2025-11-17 16:18:08','configuratore@example.com','2025-11-17 16:18:08'),(41,44,61,'2025-11-17 16:18:08','configuratore@example.com','2025-11-17 16:18:08'),(42,45,59,'2025-11-17 16:18:08','configuratore@example.com','2025-11-17 16:18:08'),(43,46,59,'2025-11-17 16:18:08','configuratore@example.com','2025-11-17 16:18:08'),(44,47,60,'2025-11-17 16:18:08','configuratore@example.com','2025-11-17 16:18:08'),(45,48,40,'2025-11-17 16:18:08','configuratore@example.com','2025-11-17 16:18:08'),(46,49,42,'2025-11-17 16:18:08','configuratore@example.com','2025-11-17 16:18:08'),(47,50,61,'2025-11-17 16:18:08','configuratore@example.com','2025-11-17 16:18:08'),(48,51,60,'2025-11-17 16:18:08','configuratore@example.com','2025-11-17 16:18:08'),(49,52,54,'2025-11-17 16:18:08','configuratore@example.com','2025-11-17 16:18:08'),(50,53,56,'2025-11-17 16:18:08','configuratore@example.com','2025-11-17 16:18:08'),(51,54,61,'2025-11-17 16:18:08','configuratore@example.com','2025-11-17 16:18:08'),(52,55,61,'2025-11-17 16:18:08','configuratore@example.com','2025-11-17 16:18:08'),(53,56,60,'2025-11-17 16:19:48','configuratore@example.com','2025-11-17 16:19:48'),(54,57,60,'2025-11-17 16:19:48','configuratore@example.com','2025-11-17 16:19:48'),(55,58,60,'2025-11-17 16:19:48','configuratore@example.com','2025-11-17 16:19:48'),(56,59,59,'2025-11-17 16:19:48','configuratore@example.com','2025-11-17 16:19:48'),(57,60,61,'2025-11-17 16:19:48','configuratore@example.com','2025-11-17 16:19:48'),(58,61,41,'2025-11-17 16:19:48','configuratore@example.com','2025-11-17 16:19:48'),(59,62,56,'2025-11-17 16:19:48','configuratore@example.com','2025-11-17 16:19:48'),(60,63,61,'2025-11-17 16:19:48','configuratore@example.com','2025-11-17 16:19:48'),(61,64,59,'2025-11-17 16:19:48','configuratore@example.com','2025-11-17 16:19:48'),(62,65,49,'2025-11-17 16:19:48','configuratore@example.com','2025-11-17 16:19:48'),(63,66,61,'2025-11-17 16:19:48','configuratore@example.com','2025-11-17 16:19:48'),(64,67,41,'2025-11-17 16:19:48','configuratore@example.com','2025-11-17 16:19:48'),(65,68,60,'2025-11-17 16:19:48','configuratore@example.com','2025-11-17 16:19:48'),(66,69,60,'2025-11-17 16:19:48','configuratore@example.com','2025-11-17 16:19:48'),(67,70,60,'2025-11-17 16:19:48','configuratore@example.com','2025-11-17 16:19:48'),(68,71,60,'2025-11-17 16:19:48','configuratore@example.com','2025-11-17 16:19:48'),(69,72,60,'2025-11-17 16:19:48','configuratore@example.com','2025-11-17 16:19:48'),(70,73,61,'2025-11-17 16:19:48','configuratore@example.com','2025-11-17 16:19:48'),(71,74,60,'2025-11-17 16:19:48','configuratore@example.com','2025-11-17 16:19:48'),(72,75,41,'2025-11-17 16:19:48','configuratore@example.com','2025-11-17 16:19:48'),(73,76,61,'2025-11-17 16:19:48','configuratore@example.com','2025-11-17 16:19:48'),(74,77,60,'2025-11-17 16:19:48','configuratore@example.com','2025-11-17 16:19:48'),(75,78,61,'2025-11-17 16:19:48','configuratore@example.com','2025-11-17 16:19:48'),(76,79,41,'2025-11-17 16:19:48','configuratore@example.com','2025-11-17 16:19:48'),(77,80,61,'2025-11-17 16:19:48','configuratore@example.com','2025-11-17 16:19:48'),(78,81,60,'2025-11-17 16:19:48','configuratore@example.com','2025-11-17 16:19:48'),(79,82,61,'2025-11-17 16:19:48','configuratore@example.com','2025-11-17 16:19:48'),(80,83,60,'2025-11-17 16:19:48','configuratore@example.com','2025-11-17 16:19:48'),(81,84,61,'2025-11-17 16:19:48','configuratore@example.com','2025-11-17 16:19:48'),(82,85,60,'2025-11-17 16:19:48','configuratore@example.com','2025-11-17 16:19:48'),(83,86,61,'2025-11-17 16:19:48','configuratore@example.com','2025-11-17 16:19:48'),(84,87,60,'2025-11-17 16:19:48','configuratore@example.com','2025-11-17 16:19:48'),(85,88,60,'2025-11-17 16:19:48','configuratore@example.com','2025-11-17 16:19:48'),(86,89,59,'2025-11-17 16:19:48','configuratore@example.com','2025-11-17 16:19:48'),(87,90,60,'2025-11-17 16:19:48','configuratore@example.com','2025-11-17 16:19:48'),(88,91,60,'2025-11-17 16:19:48','configuratore@example.com','2025-11-17 16:19:48'),(89,92,59,'2025-11-17 16:19:48','configuratore@example.com','2025-11-17 16:19:48'),(90,93,59,'2025-11-17 16:19:48','configuratore@example.com','2025-11-17 16:19:48'),(91,94,43,'2025-11-17 16:19:48','configuratore@example.com','2025-11-17 16:19:48'),(92,95,59,'2025-11-17 16:19:48','configuratore@example.com','2025-11-17 16:19:48'),(93,96,60,'2025-11-17 16:19:48','configuratore@example.com','2025-11-17 16:19:48'),(94,97,60,'2025-11-17 16:19:48','configuratore@example.com','2025-11-17 16:19:48'),(95,98,41,'2025-11-17 16:19:48','configuratore@example.com','2025-11-17 16:19:48'),(96,99,61,'2025-11-17 16:19:48','configuratore@example.com','2025-11-17 16:19:48'),(97,100,60,'2025-11-17 16:19:48','configuratore@example.com','2025-11-17 16:19:48'),(98,101,39,'2025-11-17 16:19:48','configuratore@example.com','2025-11-17 16:19:48'),(99,102,59,'2025-11-17 16:19:48','configuratore@example.com','2025-11-17 16:19:48');
/*!40000 ALTER TABLE `risposta_cliente` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_funzionalita`
--

LOCK TABLES `t_funzionalita` WRITE;
/*!40000 ALTER TABLE `t_funzionalita` DISABLE KEYS */;
INSERT INTO `t_funzionalita` VALUES (1,1,NULL,'Gestione Anagrafiche','Gestione Anagrafiche','fa-solid fa-cog','#',1,'_self',NULL,1),(2,0,1,'Ambito','Ambito','fa-solid fa-boxes','/ambito',2,'_self',NULL,1),(3,0,1,'Categoria','Categoria','fa-solid fa-tags','/categoria',3,'_self',NULL,1),(4,0,1,'Driver','Driver','fa-solid fa-road','/driver',4,'_self',NULL,1),(5,0,1,'Domanda','Domanda','fa-solid fa-question','/domanda',5,'_self',NULL,1),(9,0,NULL,'Menu Analista1','Menu Analista1','fa-solid fa-chart-line','#',10,'_self',NULL,1),(10,0,9,'Menu 10','Menu 10','fa-solid fa-circle-1','/menu10',11,'_self',NULL,1),(11,0,9,'Menu 11','Menu 11','fa-solid fa-circle-2','/menu11',12,'_self',NULL,1),(12,0,9,'Menu 12','Menu 12','fa-solid fa-circle-3','/menu12',13,'_self',NULL,1),(19,0,1,'Gruppi Risposte','Gruppi Risposte','fas fa-reply-all','/gruppo_risposta',6,'_self',NULL,1),(41,0,1,'Caricamento Domande','Caricamento Domande','fas fa-upload','/caricamento_domande',8,'_self',NULL,1),(44,0,NULL,'Menu Analista2','Menu Analista2','fas fa-table','/menu12',22,'_self',NULL,1),(45,0,1,'Log upload','Log upload','fa-solid fa-clipboard-check','/caricamenti_log',9,'_self',NULL,1),(46,0,NULL,'Gestione Progetti','Gestione Progetti','fa-solid fa-rocket','#',2,'_self',NULL,1),(47,0,46,'Nuovo Progetto','Nuovo Progetto','fa-solid fa-clone','/progetti',1,'_self',NULL,1),(48,0,46,'Assegna Analisti','Assegna Analisti','fa-solid fa-user-group','/assegna_analisti',2,'_self',NULL,1),(49,0,46,'Crea Questionario','Crea Questionario','fa-solid fa-user-group','/crea_questionario',3,'_self',NULL,1),(50,0,1,'Risposte','Risposte','fa-solid fa-square-poll-vertical','/gestione_risposte',7,'_self',NULL,1),(51,0,46,'Associa Quest-Progetto','Associa Quest-Progetto','fa-solid fa-clipboard-list','/associa_questionario_progetto',4,'_self',NULL,1),(52,0,46,'Intervista cliente(analista)','Intervista cliente(analista)','fa-file-powerpoint','/report_progetti_questionari',5,'_self',NULL,1);
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
) ENGINE=InnoDB AUTO_INCREMENT=102 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_funzionalita_utente`
--

LOCK TABLES `t_funzionalita_utente` WRITE;
/*!40000 ALTER TABLE `t_funzionalita_utente` DISABLE KEYS */;
INSERT INTO `t_funzionalita_utente` VALUES (1,1,1,1),(2,1,2,1),(3,1,3,1),(4,1,4,1),(5,1,5,1),(6,1,9,1),(7,1,10,1),(8,1,11,1),(9,1,12,1),(10,2,1,1),(11,2,2,1),(12,2,3,1),(13,2,4,1),(14,2,5,1),(15,3,9,1),(16,3,10,1),(17,3,11,1),(18,3,12,1),(73,1,19,1),(74,3,19,1),(76,1,41,1),(79,1,44,1),(81,2,19,1),(82,2,41,1),(86,3,44,1),(87,2,45,1),(88,1,46,1),(89,2,46,1),(90,1,47,1),(91,2,47,1),(92,1,48,1),(93,2,48,1),(94,1,49,1),(95,2,49,1),(96,1,50,1),(97,2,50,1),(98,1,51,1),(99,2,51,1),(100,1,52,1),(101,2,52,1);
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
INSERT INTO `t_utenti` VALUES (4,'8e785b07-7728-493f-a3b5-25f61f10e98c','admin@example.com','Admin','User',1,1,'2025-07-16 17:29:21','2025-10-28 15:01:15','admin@example.com','pbkdf2:sha256:1000000$QIqLHlxWjg19Nk9q$ea55ec49ff236c06f7d0265a8f6109dcd34f33786eeb22446c990f0ae56df964',NULL,NULL),(5,'a015083c-6632-11f0-8ad7-00090ffe0001','configuratore@example.com','Luca','Verdi',2,1,'2025-07-21 15:00:06','2025-11-24 09:37:06','configuratore@example.com','pbkdf2:sha256:1000000$QIqLHlxWjg19Nk9q$ea55ec49ff236c06f7d0265a8f6109dcd34f33786eeb22446c990f0ae56df964',NULL,NULL),(6,'a2cdd2f8-6632-11f0-8ad7-00090ffe0001','analista@example.com','Anna','Neri',3,1,'2025-07-21 15:00:11','2025-11-17 16:15:35','analista@example.com','pbkdf2:sha256:1000000$QIqLHlxWjg19Nk9q$ea55ec49ff236c06f7d0265a8f6109dcd34f33786eeb22446c990f0ae56df964',NULL,NULL),(7,'0dda8f30-2cab-497c-8c14-9d1e8428f0d8','config@example.com','Config','User',2,1,'2025-07-22 10:29:21','2025-07-22 10:29:21','config@example.com','pbkdf2:sha256:1000000$uAwK1DqMJUCKr4Gv$dab580f79ce7dec3fb83d786f7ae462be507fa81e3cbad246e139aaf3e752d46',NULL,NULL);
/*!40000 ALTER TABLE `t_utenti` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-24 12:25:36
