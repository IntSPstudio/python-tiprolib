-- |==============================================================|
--
-- HELLO!
--
-- Run this script with a privileged user (e.g. root or admin).
-- Script include basic settings and tips. Example: how to create database and users / privileges.
--
-- Replace the username with own. You can replace 'localhost' with an IP address or with '%' symbol. 
-- IP address can be like 192.168.0.%. Be careful with the % symbol though!
--
-- |==============================================================|

-- USER SETTINGS

-- CREATE USER
-- (Replace CHANGE_ME_SUPER_STRONG_PASSWORD with a secure password!)
CREATE USER 'username'@'localhost' IDENTIFIED BY 'CHANGE_ME_SUPER_STRONG_PASSWORD';

-- PRIVILEGES (Access to only product database tables with select, insert, update):
GRANT SELECT, INSERT, UPDATE ON tiprolib.* TO 'username'@'localhost';

-- OPTIONAL: (Recommended for remote access. Require SSL)
ALTER USER 'username'@'localhost' REQUIRE SSL;

-- |==============================================================|
-- SEED DEFAULTS

-- STATUSES
INSERT IGNORE INTO statuses (id, value, name) VALUES 
(2, 'active', 'Active'),
(3, 'passive', 'Passive'),
(4, 'deleted', 'Deleted');

-- ORGANIZATIONS
INSERT IGNORE INTO organizations (id, sys_name, name, info) VALUES 
(1, 'default', 'Default', 'Default organization'),
(2, 'undefined', 'Undefined', 'Undefined organization'),
(3, 'cash_customer', 'Cash customer', 'Default cash customer');

-- CATEGORIES
INSERT IGNORE INTO categories (id, name, info) VALUES 
(1, 'default', 'Default category');

-- WEBSITE USERS
INSERT IGNORE INTO web_users (id, username, display_name, password_hash, user_role, must_change_password) VALUES 
(1, 'korhonen', 'Korhonen', '', 'admin', 1),
(2, 'virtanen', 'Virtanen', '', 'admin', 1);

-- IDENTIFIER TYPES
INSERT IGNORE INTO identifier_types (id, value, name, regex_pattern, priority) VALUES 
(1, 'internal', 'Internal code', NULL, 0),
(2, 'upc', 'UPC', '^\\d{12}$', 0),
(5, 'isbn', 'ISBN', '^\\d{10}$|^97[89]\\d{10}$', 110),
(3, 'ean13', 'EAN-13', '^\\d{13}$', 100),
(4, 'ean8', 'EAN-8', '^\\d{8}$', 0),
(6, 'pn', 'Part number', NULL, 0),
(7, 'sn', 'Serial number', NULL, 0),
(8, 'alias', 'Alternative name', NULL, 0);

-- DEPOSIT TYPES
INSERT IGNORE INTO deposit_types (id, code, name, amount, currency) VALUES 
(1, 'none', 'No deposit', 0.0, 'eur');

-- START ID'S
ALTER TABLE statuses AUTO_INCREMENT = 10;
ALTER TABLE organizations AUTO_INCREMENT = 10;
ALTER TABLE categories AUTO_INCREMENT = 10;
ALTER TABLE web_users AUTO_INCREMENT = 10;
ALTER TABLE identifier_types AUTO_INCREMENT = 10;
ALTER TABLE deposit_types AUTO_INCREMENT = 10;