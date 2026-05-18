#|==============================================================|#
# Made by IntSPstudio
# Thank you for using this plugin!
# ID: 980001023
#|==============================================================|#

#|SYSTEM|=======================================================|#
APP_NAME = "TIPROLIB"

#|DATABASE|=====================================================|#
DATABASE_TYPE = "sqlite"
SQLITE_PATH = "products.db"

DATABASES = {
    "sqlite": {
        "path": "products.db"
    },

    "mariadb": {
        "host": "localhost",
        "user": "",
        "password": "",
        "database": ""
    }
}

TABLES = {
    "products": "products",
    "price_history": "price_history"
}

#|FEATURES|=====================================================|#
DEBUG = True