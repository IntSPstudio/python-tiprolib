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

-- CREATE DATABASE
CREATE DATABASE IF NOT EXISTS tiprolib;
USE tiprolib;

-- STATUSES
CREATE TABLE IF NOT EXISTS statuses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    value VARCHAR(100) UNIQUE NOT NULL,
    name VARCHAR(255),
    created DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ORGANIZATIONS
CREATE TABLE IF NOT EXISTS organizations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sys_name VARCHAR(100) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    info TEXT,
    status_id INT DEFAULT 1,
    created DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- CATEGORIES
CREATE TABLE IF NOT EXISTS categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) UNIQUE NOT NULL,
    info TEXT,
    status_id INT DEFAULT 1,
    created DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- LOCATIONS
CREATE TABLE IF NOT EXISTS locations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sys_name VARCHAR(100) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    organization_id INT DEFAULT 1,
    street_address VARCHAR(255),
    postal_code VARCHAR(20),
    city VARCHAR(100),
    info TEXT,
    status_id INT DEFAULT 1,
    created DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY(organization_id) REFERENCES organizations(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- DEPOSIT_TYPES
CREATE TABLE IF NOT EXISTS deposit_types (
    id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(100) UNIQUE NOT NULL,
    name VARCHAR(255),
    amount DOUBLE DEFAULT 0,
    currency VARCHAR(10) DEFAULT 'eur',
    status_id INT DEFAULT 1,
    created DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- PRODUCTS
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    brand_id INT DEFAULT 1,
    sys_name VARCHAR(100) NOT NULL,
    name VARCHAR(255) NOT NULL,
    qty_default DOUBLE DEFAULT 1,
    qty_unit VARCHAR(50) DEFAULT 'pcs',
    weight_default DOUBLE,
    weight_unit VARCHAR(50) DEFAULT 'g',
    deposit_type_id INT DEFAULT 1,
    info TEXT,
    note TEXT,
    status_id INT DEFAULT 1,
    created DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    extra TEXT,
    FOREIGN KEY(brand_id) REFERENCES organizations(id),
    FOREIGN KEY(deposit_type_id) REFERENCES deposit_types(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ROUTE_CATEGORIES
CREATE TABLE IF NOT EXISTS route_categories (
    product_id INT,
    category_id INT,
    status_id INT DEFAULT 1,
    created DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (product_id, category_id),
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- IDENTIFIER_TYPES
CREATE TABLE IF NOT EXISTS identifier_types (
    id INT AUTO_INCREMENT PRIMARY KEY,
    value VARCHAR(100) UNIQUE NOT NULL,
    name VARCHAR(255),
    regex_pattern VARCHAR(255),
    priority INT DEFAULT 0,
    info TEXT,
    status_id INT DEFAULT 1,
    created DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- IDENTIFIERS
CREATE TABLE IF NOT EXISTS identifiers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT,
    value VARCHAR(150) UNIQUE NOT NULL,
    type_id INT,
    info TEXT,
    status_id INT DEFAULT 1,
    created DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY(product_id) REFERENCES products(id),
    FOREIGN KEY(type_id) REFERENCES identifier_types(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- EXTRA_FIELD_DEFINITIONS
CREATE TABLE IF NOT EXISTS extra_field_definitions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    key_name VARCHAR(100) UNIQUE NOT NULL,
    display_name VARCHAR(255) NOT NULL,
    data_type VARCHAR(50) DEFAULT 'text',
    status_id INT DEFAULT 1,
    created DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- STOCK_SLOTS
CREATE TABLE IF NOT EXISTS stock_slots (
    id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(100) NOT NULL,
    path VARCHAR(255) UNIQUE,
    parent_id INT,
    organization_id INT,
    info TEXT,
    location_id INT,
    status_id INT DEFAULT 1,
    created DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY(parent_id) REFERENCES stock_slots(id),
    FOREIGN KEY(organization_id) REFERENCES organizations(id),
    FOREIGN KEY(location_id) REFERENCES locations(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- STOCK
CREATE TABLE IF NOT EXISTS stock (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    identifier_id INT,
    qty_value DOUBLE DEFAULT 0,
    qty_unit VARCHAR(50),
    weight DOUBLE,
    weight_unit VARCHAR(50) DEFAULT 'kg',
    manufacturer_id INT DEFAULT 1,
    extra TEXT,
    slot_id INT DEFAULT 1,
    status_id INT DEFAULT 1,
    created DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY(product_id) REFERENCES products(id),
    FOREIGN KEY(identifier_id) REFERENCES identifiers(id),
    FOREIGN KEY(manufacturer_id) REFERENCES organizations(id),
    FOREIGN KEY(slot_id) REFERENCES stock_slots(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- STOCK_LOGS
CREATE TABLE IF NOT EXISTS stock_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    stock_id INT,
    product_id INT,
    identifier_id INT,
    action VARCHAR(100) NOT NULL,
    qty_delta DOUBLE DEFAULT 0,
    qty_unit VARCHAR(50),
    reason TEXT,
    ref_table VARCHAR(100),
    ref_id INT,
    status_id INT DEFAULT 1,
    created DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY(stock_id) REFERENCES stock(id),
    FOREIGN KEY(product_id) REFERENCES products(id),
    FOREIGN KEY(identifier_id) REFERENCES identifiers(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- PRICE_HISTORY
CREATE TABLE IF NOT EXISTS price_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    price DOUBLE NOT NULL,
    currency VARCHAR(10) DEFAULT 'eur',
    location_id INT,
    organization_id INT,
    created DATETIME DEFAULT CURRENT_TIMESTAMP,
    status_id INT DEFAULT 1,
    FOREIGN KEY(product_id) REFERENCES products(id),
    FOREIGN KEY(location_id) REFERENCES locations(id),
    FOREIGN KEY(organization_id) REFERENCES organizations(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- PURCHASES
CREATE TABLE IF NOT EXISTS purchases (
    id INT AUTO_INCREMENT PRIMARY KEY,
    organization_id INT DEFAULT 1,
    vendor_id INT DEFAULT 2,
    total_price DOUBLE,
    currency VARCHAR(10) DEFAULT 'eur',
    status_id INT DEFAULT 1,
    created DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY(organization_id) REFERENCES organizations(id),
    FOREIGN KEY(vendor_id) REFERENCES organizations(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- PURCHASE_LINES
CREATE TABLE IF NOT EXISTS purchase_lines (
    id INT AUTO_INCREMENT PRIMARY KEY,
    purchase_id INT NOT NULL,
    product_id INT NOT NULL,
    identifier_id INT,
    qty_value DOUBLE DEFAULT 1,
    qty_unit VARCHAR(50),
    unit_price DOUBLE,
    status_id INT DEFAULT 1,
    created DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY(purchase_id) REFERENCES purchases(id),
    FOREIGN KEY(product_id) REFERENCES products(id),
    FOREIGN KEY(identifier_id) REFERENCES identifiers(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- SALES
CREATE TABLE IF NOT EXISTS sales (
    id INT AUTO_INCREMENT PRIMARY KEY,
    organization_id INT DEFAULT 1,
    customer_id INT DEFAULT 3,
    total_price DOUBLE,
    currency VARCHAR(10) DEFAULT 'eur',
    payment_status INT DEFAULT 0,
    status_id INT DEFAULT 1,
    created DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY(organization_id) REFERENCES organizations(id),
    FOREIGN KEY(customer_id) REFERENCES organizations(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- SALE_LINES
CREATE TABLE IF NOT EXISTS sale_lines (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sale_id INT NOT NULL,
    product_id INT NOT NULL,
    identifier_id INT,
    qty_value DOUBLE DEFAULT 1,
    qty_unit VARCHAR(50),
    unit_price DOUBLE,
    status_id INT DEFAULT 1,
    created DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY(sale_id) REFERENCES sales(id),
    FOREIGN KEY(product_id) REFERENCES products(id),
    FOREIGN KEY(identifier_id) REFERENCES identifiers(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- JOURNAL
CREATE TABLE IF NOT EXISTS journal (
    id INT AUTO_INCREMENT PRIMARY KEY,
    dated DATETIME DEFAULT CURRENT_TIMESTAMP,
    title VARCHAR(255),
    body TEXT NOT NULL,
    extra TEXT,
    status_id INT DEFAULT 1,
    created DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- WEBSITE USERS
CREATE TABLE IF NOT EXISTS web_users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(150) UNIQUE NOT NULL,
    display_name VARCHAR(255),
    password_hash VARCHAR(255),
    user_role VARCHAR(50) DEFAULT 'seller',
    must_change_password TINYINT DEFAULT 1,
    token_secret VARCHAR(255),
    status_id INT DEFAULT 1,
    created DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;