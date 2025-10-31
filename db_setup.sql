CREATE DATABASE OBS;

use OBS;

DROP TABLE IF EXISTS `account`;

CREATE TABLE `account` (
  `acc_no` int NOT NULL,
  `overdraft` float DEFAULT NULL,
  `balance` float DEFAULT NULL,
  PRIMARY KEY (`acc_no`)
);

DROP TABLE IF EXISTS `account_type`;
CREATE TABLE `account_type` (
  `account_no` int NOT NULL,
  `deposit_ammount` int DEFAULT NULL,
  `transaction_limit` int DEFAULT NULL,
  `withdraw_limit` int DEFAULT NULL,
  `interest_rate` int DEFAULT NULL,
  PRIMARY KEY (`account_no`),
  CONSTRAINT `account_type_ibfk_1` FOREIGN KEY (`account_no`) REFERENCES `account` (`acc_no`) ON DELETE CASCADE
);

DROP TABLE IF EXISTS `credit_card`;
CREATE TABLE `credit_card` (
  `cc_limit` int DEFAULT NULL,
  `cc_number` int NOT NULL,
  `cc_cvv` int DEFAULT NULL,
  `cc_expirydate` date DEFAULT NULL,
  `account_no` int NOT NULL,
  PRIMARY KEY (`cc_number`),
  KEY `account_no` (`account_no`),
  CONSTRAINT `credit_card_ibfk_1` FOREIGN KEY (`account_no`) REFERENCES `account` (`acc_no`) ON DELETE CASCADE
);

DROP TABLE IF EXISTS `debit_card`;
CREATE TABLE `debit_card` (
  `debit_number` int NOT NULL,
  `cc_cvv` int DEFAULT NULL,
  `debit_expirydate` date DEFAULT NULL,
  `account_no` int NOT NULL,
  PRIMARY KEY (`debit_number`),
  KEY `account_no` (`account_no`),
  CONSTRAINT `debit_card_ibfk_1` FOREIGN KEY (`account_no`) REFERENCES `account` (`acc_no`) ON DELETE CASCADE
);

DROP TABLE IF EXISTS `customer`;
CREATE TABLE `customer` (
  `cust_id` int NOT NULL,
  `dob` date DEFAULT NULL,
  `first_name` varchar(20) DEFAULT NULL,
  `last_name` varchar(20) DEFAULT NULL,
  `phone_no` bigint NOT NULL,
  `email` varchar(250) DEFAULT NULL,
  `pan_no` bigint NOT NULL,
  `account_no` int NOT NULL,
  PRIMARY KEY (`cust_id`),
  KEY `account_no` (`account_no`),
  CONSTRAINT `customer_ibfk_1` FOREIGN KEY (`account_no`) REFERENCES `account` (`acc_no`) ON DELETE CASCADE
);

DROP TABLE IF EXISTS `login`;
CREATE TABLE `login` (
  `email_id` varchar(250) NOT NULL,
  `username` varchar(50) DEFAULT NULL,
  `password` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`email_id`)
);

DROP TABLE IF EXISTS `transaction_history`;
CREATE TABLE `transaction_history` (
  `date` date NOT NULL,
  `time` time NOT NULL,
  `amount` float DEFAULT NULL,
  `description` varchar(150) DEFAULT NULL,
  `available_balance` float DEFAULT NULL,
  `account_no` int NOT NULL,
  KEY `account_no` (`account_no`),
  CONSTRAINT `transaction_ibfk_1` FOREIGN KEY (`account_no`) REFERENCES `account` (`acc_no`) ON DELETE CASCADE
);

DROP TABLE IF EXISTS `loans`;
CREATE TABLE `loans` (
  `loan_id` int NOT NULL,
  `term` int DEFAULT NULL,
  `rate_of_interest` float DEFAULT NULL,
  `amount` float DEFAULT NULL,
  `type_of_loan` varchar(20) DEFAULT NULL,
  `account_no` int DEFAULT NULL,
  PRIMARY KEY (`loan_id`),
  KEY `account_no` (`account_no`),
  CONSTRAINT `loans_ibfk_1` FOREIGN KEY (`account_no`) REFERENCES `account` (`acc_no`) ON DELETE SET NULL
);

INSERT INTO `account` VALUES (329668,0,997757),(486558,0,998189),(620886,0,1000550),(647360,0,999773),(674275,0,999730),(765420,0,999637),(767522,0,997776),(777259,0,999052),(873373,0,999786),(883489,0,999027);
INSERT INTO `account_type` VALUES (329668,500,200000,200000,5),(486558,5000,200000,100000,5),(620886,1500,300000,100000,6),(647360,1500,123000,200000,8),(674275,990,500000,200000,6),(765420,2000,100000,100000,5),(767522,2500,200000,200000,7),(777259,1600,100000,300000,8),(873373,1000,200000,100000,5),(883489,800,500000,300000,7);
INSERT INTO `credit_card` VALUES (54563,11655571,248,'2023-10-25',777259),(23670,12247594,901,'2023-12-06',873373),(62066,12546778,410,'2023-06-17',674275),(14134,12890436,213,'2023-10-13',883489),(34119,13221224,570,'2024-02-12',486558),(96119,13246683,308,'2023-10-23',329668),(10611,14286801,744,'2023-12-31',647360),(81671,14336466,127,'2023-04-16',767522),(82284,18548205,848,'2023-05-04',765420),(60265,18781485,829,'2023-08-28',620886);
INSERT INTO `debit_card` VALUES (10836544,563,'2023-03-03',329668),(11841303,281,'2023-12-19',620886),(13222655,372,'2023-12-20',674275),(13519196,699,'2023-12-15',486558),(13927455,856,'2023-07-18',765420),(15596584,830,'2023-06-07',647360),(17400335,158,'2023-11-27',873373),(18634753,857,'2023-12-19',777259),(19537734,681,'2023-05-11',883489),(19848698,980,'2023-09-18',767522);
INSERT INTO `loans` VALUES (1,9,9,74920,'Home Loan',873373),(2,9,9,39497,'Business Loan',329668),(3,5,6,35193,'Personal Loan',647360),(4,5,10,84855,'Gold Loan',620886),(5,10,9,25024,'Business Loan',883489),(6,10,6,71005,'Gold Loan',674275),(7,8,7,73476,'Gold Loan',873373),(8,5,9,10855,'Home Loan',777259),(9,5,6,12932,'Home Loan',765420),(10,6,8,54723,'Gold Loan',647360);
INSERT INTO `login` VALUES ('ac.mattis@protonmail.net','XEVO888','uwo46w0Su'),('ante.dictum@outlook.edu','SRKK317','ojy28p3Lh'),('consectetuer@google.com','YKOP908','lmg69k6Bp'),('est.mollis@hotmail.com','FLNI527','czc48x7Dv'),('fermentum.risus@icloud.com','NFIS952','guf05v8Vv'),('inceptos.hymenaeos@outlook.ca','XNPS443','ggx74x1Ag'),('maecenas.mi@google.edu','HDTO052','gkf62n8Nq'),('nec.ante.blandit@yahoo.net','DSRM876','uds90l8Ep'),('phasellus@google.ca','ESCK764','zhw03h3Kt'),('scelerisque@aol.edu','GGVT865','rhh73b5Ev');
INSERT INTO `customer` VALUES (1,'2020-07-05','Benedict','Harper',934652121,'ac.mattis@protonmail.net',161582657,873373),(2,'2008-02-09','Joshua','Boone',933750467,'vitae.sodales@yahoo.com',667818422,486558),(3,'2009-08-31','Jesse','Harvey',921984594,'mauris.ut@protonmail.edu',504181748,329668),(4,'2014-01-06','Quail','Morris',936233275,'lectus.quis@outlook.org',353491334,674275),(5,'1998-12-29','Bryar','Schultz',973216943,'phasellus@google.ca',660912167,883489),(6,'2006-11-19','Chase','Hart',973655286,'neque@outlook.org',484372827,777259),(7,'2008-03-02','Keegan','Goff',979617912,'turpis.nulla@google.net',338942066,765420),(8,'2007-12-29','Illiana','Hanson',977818456,'fermentum.risus@icloud.com',467327842,620886),(9,'2004-02-27','Baxter','Lawrence',987457745,'imperdiet@aol.org',933044774,767522),(10,'2004-06-10','Bert','Chang',968270946,'consectetuer@google.com',569736306,647360);

alter table `loans`
	add column `amount_due` float DEFAULT NULL;

update `loans` set `amount_due` = `amount` + (`amount`*`rate_of_interest`*`term`)/100 where `loan_id`>0;

select * from `transaction_history`;

select * from account;

select * from account_type;

select * from credit_card;

select * from debit_card;

select * from loans;

select * from login;