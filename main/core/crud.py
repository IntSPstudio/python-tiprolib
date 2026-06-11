#|==============================================================|#
# Made by IntSPstudio
# Thank you for using this plugin!
# ID: 980001023
#|==============================================================|#

#SETTINGS
import sqlite3
from enums.status import Status
from database.adapter import PLACEHOLDER
from core.settings import ALLOWED_TABLES, ALLOWED_FIELDS

#GET ALL
def get_all(conn, table_name: str, mode: int=0, limit: int =100, offset: int =0):
    #TABLE RULES
    if table_name not in ALLOWED_TABLES:
        raise ValueError(f"Invalid table '{table_name}'")
    #CONNECTION
    cursor = conn.cursor()
    #SEARCH RESTRICTIONS (API THINGS)
    if mode == 0:
        query = f"""
                SELECT * FROM {table_name} 
                WHERE status_id = {PLACEHOLDER} 
                LIMIT {PLACEHOLDER} OFFSET {PLACEHOLDER}
            """
        params = (Status.ACTIVE.value, limit, offset)
    else:
        query = f"SELECT * FROM {table_name} LIMIT {PLACEHOLDER} OFFSET {PLACEHOLDER}"
        params = (limit, offset)
    #GET DATA
    try:
        cursor.execute(query, params)
        columns = [column[0] for column in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    except sqlite3.Error as e:
        print(f"Error with {table_name}): {e}")
        return {}

#GET BY ID
def get_by_id(conn, table_name, row_id):
    #TABLE RULES
    if table_name not in ALLOWED_TABLES:
        raise ValueError(f"Invalid table '{table_name}'")
    #CONNECTION
    cursor = conn.cursor()
    #QUERY
    query = f"SELECT * FROM {table_name} WHERE id = {PLACEHOLDER}"
    #GET DATA
    try:
        cursor.execute(query, (row_id,))
        row = cursor.fetchone()
        if row:
            columns = [column[0] for column in cursor.description]
            return dict(zip(columns, row))
        return None
    except sqlite3.Error as e:
        print(f"Error with {table_name}): {e}")
        return None
    
#GENERAL UPDATE
def update_record(conn, table: str, row_id: int, update_data: dict) -> dict:
    #TABLE RULES
    if table not in ALLOWED_TABLES:
        return {"error": f"Table '{table}' is not allowed or does not exist."}
    cursor = conn.cursor()
    #FIELD RULES
    allowed_fields = ALLOWED_FIELDS.get(table)
    if not allowed_fields:
        return {"error": f"No allowed fields configured for table '{table}'."}  
    #PREP
    clean_updates = {}
    for field, value in update_data.items():
        #SKIP
        if field == "id" or field == "name" or field.endswith("_id"):
            continue
        #VALIDATE + MAP INPUT
        if field in allowed_fields:
            if isinstance(value, str):
                value = value.strip()
            clean_updates[field] = value
        else:
            return {"error": f"Field '{field}' is not allowed for table '{table}'."}
    #CHECK
    if not clean_updates:
        return {"error": "No valid fields provided for update."}
    #CREATING COMMAND
    set_clauses = [f"{field} = {PLACEHOLDER}" for field in clean_updates.keys()]
    set_string = ", ".join(set_clauses)
    query = f"UPDATE {table} SET {set_string} WHERE id = {PLACEHOLDER}"
    query_params = tuple(clean_updates.values()) + (row_id,)
    #SEND IT
    try:
        cursor.execute(query, query_params)
        conn.commit()
        if cursor.rowcount == 0:
            return {"error": f"Record with ID {row_id} not found in table '{table}'."}
        return {
            "success": True, 
            "status": "updated", 
            "id": row_id, 
            "events": [f"Updated fields: {', '.join(clean_updates.keys())} in '{table}'"]
        }
    #ERROR
    except sqlite3.Error as e:
        return {"error": f"Database error: {str(e)}"}

#STATUS UPDATE
def update_status(conn, table_name: str, row_id: int, new_status: int):
    #TABLE RULES
    if table_name not in ALLOWED_TABLES:
        raise ValueError(f"Invalid table '{table_name}'")
    cursor = conn.cursor()
    #QUERY
    query = f"""
        UPDATE {table_name} 
        SET status_id = {PLACEHOLDER}, updated = CURRENT_TIMESTAMP 
        WHERE id = {PLACEHOLDER}
    """
    #SEND IT
    try:
        cursor.execute(query, (new_status, row_id))
        conn.commit()
        #CHECK
        if cursor.rowcount == 0:
            return {"status": "error", "events": f"ID {row_id} not found in the {table_name}"}
        return {"status": "success", "events": f"Status update (ID: {row_id})"}
    #ERROR
    except sqlite3.Error as e:
        conn.rollback()
        return {"status": "error", "events": str(e)}