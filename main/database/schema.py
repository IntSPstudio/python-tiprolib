#|==============================================================|#
# Made by IntSPstudio
# Thank you for using this plugin!
# ID: 980001023
#|==============================================================|#

#SETTINGS
from config import DATABASE_TYPE

#DATABASE
def create_database(conn):
    cursor = conn.cursor()

    #SQLITE
    if DATABASE_TYPE == "sqlite":
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS products_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            brand_id INTEGER,
            name TEXT,
            qty_default REAL,
            qty_unit TEXT,
            category_id INTEGER,
            info TEXT,
            note TEXT,
            status_id INTEGER,
            created DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated TEXT,
            extra TEXT
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS product_identifiers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            identifier TEXT,
            type TEXT,
            info TEXT,
            status_id INTEGER,
            created DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated TEXT
        )
        """)
        cursor.execute("""                
        CREATE TABLE IF NOT EXISTS product_inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            identifier_id INTEGER,
            qty_value REAL,
            qty_unit TEXT,
            manufacturer_id INTEGER,
            extra TEXT,
            status_id INTEGER,
            created DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated TEXT
        )
        """)
        cursor.execute("""  
        CREATE TABLE IF NOT EXISTS quantity_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            identifier_id INTEGER,
            value INTEGER,
            status_id INTEGER,
            created DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated TEXT
        )
        """)
        cursor.execute("""                
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            info TEXT,
            status_id INTEGER,
            created DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated TEXT
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS categorys (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            info TEXT,
            status_id INTEGER,
            created DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated TEXT
        )
        """) 
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS price_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            price REAL,
            currency TEXT,
            place TEXT,
            created DATETIME DEFAULT CURRENT_TIMESTAMP,
            status_id INTEGER
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS locations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            organizations_id INTEGER,
            status_id,
            created DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated TEXT
        )
        """)
    #COMMON
    conn.commit()
