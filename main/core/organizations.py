#|==============================================================|#
# Made by IntSPstudio
# Thank you for using this plugin!
# ID: 980001023
#|==============================================================|#

#SETTINGS
import sqlite3
import database.adapter as adpt

#GET OR CREATE
def get_or_create_org(conn, name, description=None):
    cursor = conn.cursor()
    #TRY
    command = f"SELECT id FROM organizations WHERE name = {adpt.PLACEHOLDER}"
    cursor.execute(command, (name,))
    row = cursor.fetchone()
    #IF EXISTS
    if row:
        return {"id": row[0]} 
    #CREATE
    try:
        command = f"INSERT INTO organizations (name, info) VALUES ({adpt.PLACEHOLDER}, {adpt.PLACEHOLDER})"
        cursor.execute(command,(name, description))
        conn.commit()
        return {"id": cursor.lastrowid}
    #ERROR
    except sqlite3.IntegrityError:
        command = f"SELECT id FROM organizations WHERE name = {adpt.PLACEHOLDER}"
        cursor.execute(command, (name,))
        row = cursor.fetchone()
        if row:
            return {"id": row[0]}
        raise