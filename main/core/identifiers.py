#|==============================================================|#
# Made by IntSPstudio
# Thank you for using this plugin!
# ID: 980001023
#|==============================================================|#

#SETTINGS
import sqlite3
from random import randint
from database.adapter import PLACEHOLDER
import re

#IF NOT CODE -> INTERNAL CODE
def generate_internal_code(conn):
    cursor = conn.cursor()
    while True:
        code = str(
            randint(1000000000, 9999999999)
        )
        cursor.execute(
            f"SELECT value FROM identifiers WHERE value={PLACEHOLDER}",
            (code,)
        )
        if not cursor.fetchone():
            return code

#GET OR CREATE
def get_or_create_iden(conn, input: dict, events=None):
    if events is None:
        events = []
    cursor = conn.cursor()
    value = str(input.get("value", "")).strip().replace(" ", "")
    product_id = input.get("product_id")
    type_id = input.get("type_id")
    info = input.get("info")
    internal_id = get_or_create_type(conn, "internal").get("id")
    if not value:
        if type_id == internal_id:
            value = generate_internal_code(conn)
        else:
            return {"error": "Identifier value is required"}
    elif type_id is None:
        type_id = guess_identifier_type(conn, value, events)
    cursor.execute(f"SELECT id, product_id FROM identifiers WHERE value = {PLACEHOLDER}", (value,))
    row = cursor.fetchone()
    if row:
        return {"id": row[0], "product_id": row[1], "status": "exists"}
    cursor.execute(
        f"""
        INSERT INTO identifiers (product_id, value, type_id, info)
        VALUES ({PLACEHOLDER}, {PLACEHOLDER}, {PLACEHOLDER}, {PLACEHOLDER})
        """,
        (product_id, value, type_id, info),
    )
    conn.commit()
    return {"id": cursor.lastrowid, "value": value, "status": "created"}

#SCANNER
def get_by_identifier(conn, identifier: str):
    identifier = str(identifier).strip().replace(" ", "")
    cursor = conn.cursor()
    query = f"""
        SELECT p.*, o.name as brand_name, i.value as identifier_value
        FROM products p
        JOIN identifiers i ON p.id = i.product_id
        JOIN organizations o ON p.brand_id = o.id
        WHERE i.value = {PLACEHOLDER} AND p.status_id = 1
    """
    cursor.execute(query, (identifier,))
    row = cursor.fetchone()
    if row:
        columns = [column[0] for column in cursor.description]
        result = dict(zip(columns, row))
        return {"results": result}

#GET OR CREATE IDENTIFIER TYPE
def get_or_create_type(conn, type_input: str):
    cursor = conn.cursor()
    #RULES
    code = str(type_input).strip().lower()
    if not code:
        return {"error": "Identifier code is required"}
    #CHECK
    cursor.execute(f"SELECT id FROM identifier_types WHERE value = {PLACEHOLDER}", (code,))
    row = cursor.fetchone()
    #IF EXISTS
    if row:
        return {"id": row[0], "status": "exists"}
    #CREATE
    try:
        cursor.execute(f"INSERT INTO identifier_types (value) VALUES ({PLACEHOLDER})", (code,))
        conn.commit()
        return {"id": cursor.lastrowid, "status": "created"}
    #ERROR
    except sqlite3.Error as e:
        return {"error": str(e)}
    
#CHECK IF VALID
def is_valid_barcode(code: str) -> bool:
    code = str(code or "").strip()
    if not code.isdigit() or len(code) not in {8, 12, 13}:
        return False
    data_digits = code[:-1]       
    check_digit = int(code[-1])   
    reversed_digits = reversed(data_digits)
    total = sum(int(digit) * (3 if i % 2 == 0 else 1) for i, digit in enumerate(reversed_digits))
    calculated_check = (10 - (total % 10)) % 10
    return calculated_check == check_digit

#GUESS IDENTIFIER TYPE
def guess_identifier_type(conn, value, events):
    code = str(value).strip().replace(" ", "")
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, value, regex_pattern 
        FROM identifier_types 
        WHERE regex_pattern IS NOT NULL AND status_id = 1
        ORDER BY priority DESC, id ASC
        """
    )
    rules = cursor.fetchall()
    for type_id, type_value, pattern in rules:
        try:
            if re.match(pattern, code):
                if len(code) in {8, 12, 13} and not is_valid_barcode(code):
                    events.append(f"Code matched {type_value} pattern but failed checksum.")
                    continue
                events.append(f"Guessed identifier type: {type_value}")
                return type_id
        except re.error:
            continue
    events.append("Could not guess identifier type, leaving as NULL")
    return None