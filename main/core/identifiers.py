#|==============================================================|#
# Made by IntSPstudio
# Thank you for using this plugin!
# ID: 980001023
#|==============================================================|#

#SETTINGS
from random import randint

#IF NOT GTIN -> INTERNAL
def generate_internal_gtin(conn):
    cursor = conn.cursor()
    while True:
        code = str(
            randint(1000000000, 9999999999)
        )
        cursor.execute(
            "SELECT gtin FROM products WHERE gtin=?",
            (code,)
        )
        if not cursor.fetchone():
            return code