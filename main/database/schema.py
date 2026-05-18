#|==============================================================|#
# Made by IntSPstudio
# Thank you for using this plugin!
# ID: 980001023
#|==============================================================|#

#SETTINGS
from config import DATABASE_TYPE
from config import TABLES
from database.adapter import AUTOINCREMENT

#DATABASE
def create_database(conn):
    cursor = conn.cursor()

    #SQLITE
    if DATABASE_TYPE == "sqlite":
        cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY {AUTOINCREMENT},
            gtin TEXT UNIQUE,
            gtin_type TEXT,
            code TEXT,
            brand TEXT,
            manufacturer TEXT,
            name TEXT,
            qty_value REAL,
            qty_default REAL,
            qty_unit TEXT,
            category TEXT,
            info TEXT,
            note TEXT,
            madein TEXT,
            status TEXT,
            created DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated TEXT,
            additionalinfo TEXT
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS price_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            price REAL,
            currency TEXT,
            place TEXT,
            date DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)
    #COMMON
    conn.commit()
