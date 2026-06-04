#|==============================================================|#
# Made by IntSPstudio
# Thank you for using this plugin!
# ID: 980001023
#|==============================================================|#

#SETTINGS
import sqlite3
import database.adapter as adpt
from utils.textutils import boring_text

#GET OR CREATE
def get_or_create_org(conn, raw_name, description=None, mode: int = 1):
    #RULES
    raw_name = boring_text(raw_name,0)
    key = raw_name.strip().lower()
    if not raw_name:
        return {"error": "Invalid name"}
    #COMMAND
    cursor = conn.cursor()
    command = f"SELECT id FROM organizations WHERE key = {adpt.PLACEHOLDER}"
    cursor.execute(command, (key,))
    row = cursor.fetchone()
    #IF EXISTS
    if row:
        return {"id": row[0]}
    #CREATE
    if mode == 1:
        try:
            command = f"""
                INSERT INTO organizations (key, name, info)
                VALUES ({adpt.PLACEHOLDER}, {adpt.PLACEHOLDER}, {adpt.PLACEHOLDER})
            """
            cursor.execute(command, (key, raw_name, description))
            conn.commit()
            return {"id": cursor.lastrowid}
        #ERROR
        except sqlite3.IntegrityError:
            cursor.execute(
                f"SELECT id FROM organizations WHERE key = {adpt.PLACEHOLDER}",
                (key,)
            )
            row = cursor.fetchone()
            if row:
                return {"id": row[0]}
            raise
    return {"error": "Not found and mode=0"}