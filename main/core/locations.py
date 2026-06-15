#|==============================================================|#
# Made by IntSPstudio
# Thank you for using this plugin!
# ID: 980001023
#|==============================================================|#

#SETTINGS
import sqlite3
from database.adapter import PLACEHOLDER
from core.settings import FIELD_ALIAS
from core.settings import ALLOWED_FIELDS_LOC
from core.organizations import get_or_create_org
from utils.textutils import boring_text

#GET OR CREATE
def get_or_create_loc(conn, input: dict):
    cursor = conn.cursor()
    events = []
    data = {}
    #RULES
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
    raw_name = data.get("name")
    if not raw_name:
        return {"error": "Location name is required", "events": events}
    clean_name = boring_text(raw_name, 0)
    loc_key = boring_text(raw_name, 3)
    if not loc_key:
        return {"error": "Invalid location name for key generation", "events": events}
    #NAME SETTINGS
    data["name"] = clean_name
    data["sys_name"] = loc_key
    #ORG
    org_field = "organization_id"
    org_raw = data.get(org_field)
    if org_raw and isinstance(org_raw, str) and not org_raw.isnumeric():
        output = get_or_create_org(conn, org_raw)
        if "id" in output:
            data[org_field] = output["id"]
        else:
            events.append(f"Could not resolve organization: {org_raw}")
    #CONNECT
    try:
        #CHECK IF EXISTS
        cursor.execute(
            f"SELECT id FROM locations WHERE sys_name = {PLACEHOLDER}", 
            (loc_key,)
        )
        row = cursor.fetchone()
        if row:
            return {"status": "exists", "id": row[0], "events": events}
        #CREATE LOCATION
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