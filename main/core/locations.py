#|==============================================================|#
# Made by IntSPstudio
# Thank you for using this plugin!
# ID: 980001023
#|==============================================================|#

#SETTINGS
import sqlite3
import json
from database.adapter import PLACEHOLDER
from core.settings import FIELD_ALIAS
from core.settings import ALLOWED_FIELDS_LOC
from core.organizations import get_or_create_org

#GET OR CREATE
def get_or_create_loc(conn, input: dict):
    cursor = conn.cursor()
    events =[]
    data ={}
    if not input:
        return {"error": "invalid input"}
    #VALIDATE + MAP INPUT
    for field in ALLOWED_FIELDS_LOC:
        data.setdefault(field, None)
    for field, value in input.items():
        try:
            field = FIELD_ALIAS["add_locations"].get(field, field)
            if field not in ALLOWED_FIELDS_LOC:
                events.append(f"Error: field not allowed -> {field}")
                continue
            if isinstance(value, str):
                value = value.strip()
            data[field] = value
        except ValueError as e:
            events.append(str(e))
    #NAME IS REQUIRED
    if not data.get("name"):
        return {"error": "Location name is required", "events": events}
    #ORG
    key = "organization_id"
    org_raw = data.get(key); org = org_raw.lower() if org_raw else None
    if org:
        if not org.isnumeric():
            output = get_or_create_org(conn,org)
            test = output.get("id")
            if test:
                test = output["id"]
                data[key] = test
    #CONNECT
    try:
        cursor.execute(f"SELECT id FROM locations WHERE name = {PLACEHOLDER}", (data["name"],))
        row = cursor.fetchone()
        #IF EXISTS
        if row:
            return {"status": "exists", "id": row[0], "events": events}
        #CREATING NEW
        clean_data = {k: v for k, v in data.items() if v is not None}
        columns = ", ".join(clean_data.keys())
        placeholders = ", ".join([PLACEHOLDER] * len(clean_data))
        query = f"INSERT INTO locations ({columns}) VALUES ({placeholders})"
        cursor.execute(query, tuple(clean_data.values()))
        conn.commit()
        return {"status": "created", "id": cursor.lastrowid, "events": events}
    #ERROR
    except sqlite3.Error as e:
        return {"error": str(e), "events": events}