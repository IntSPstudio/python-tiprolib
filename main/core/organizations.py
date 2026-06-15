#|==============================================================|#
# Made by IntSPstudio
# Thank you for using this plugin!
# ID: 980001023
#|==============================================================|#

#SETTINGS
import sqlite3
from database.adapter import PLACEHOLDER
from utils.textutils import boring_text

#GET OR CREATE
def get_or_create_org(conn, raw_name, description=None, mode: int = 1):
    #RULES
    raw_name = boring_text(raw_name,0)
    key = boring_text(raw_name,3)
    if not raw_name:
        return {"error": "Invalid name"}
    #COMMAND
    cursor = conn.cursor()
    command = f"SELECT id FROM organizations WHERE sys_name = {PLACEHOLDER}"
    cursor.execute(command, (key,))
    row = cursor.fetchone()
    #IF EXISTS
    if row:
        return {"id": row[0]}
    #CREATE
    if mode == 1:
        try:
            command = f"""
                INSERT INTO organizations (sys_name, name, info)
                VALUES ({PLACEHOLDER}, {PLACEHOLDER}, {PLACEHOLDER})
            """
            cursor.execute(command, (key, raw_name, boring_text(description,2)))
            conn.commit()
            return {"id": cursor.lastrowid}
        #ERROR
        except sqlite3.IntegrityError:
            cursor.execute(
                f"SELECT id FROM organizations WHERE sys_name = {PLACEHOLDER}",
                (key,)
            )
            row = cursor.fetchone()
            if row:
                return {"id": row[0]}
            raise
    return {"error": "Not found and mode=0"}

#GET ORGANIZATION BY KEY
def get_organization_by_key(conn, org_key: str):
    #RULES
    clean_key = boring_text(org_key, 3)
    if not clean_key:
        return {"error": "invalid_key"}
    #GET
    cursor = conn.cursor()
    cursor.execute(
        f"""
        SELECT id, sys_name, name, info, status_id, created, updated 
        FROM organizations 
        WHERE sys_name = {PLACEHOLDER}
        """,
        (clean_key,)
    )
    row = cursor.fetchone()
    #NOT
    if not row:
        return {"error": "organization_not_found"}
    columns = [column[0] for column in cursor.description]
    return {"results": dict(zip(columns, row))}