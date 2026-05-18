#|==============================================================|#
# Made by IntSPstudio
# Thank you for using this plugin!
# ID: 980001023
#|==============================================================|#

#SETTINGS
import json
from utils.timeutils import currentdatetime
from utils.textutils import boring_text
from utils.parsers import parse_qty_input
from core.settings import (ALLOWED_TABLES, FIELD_ALIAS, ALLOWED_FIELDS_PRODUCTS)
from core.identifiers import generate_internal_gtin
from database.adapter import PLACEHOLDER

#BASIC GET ALL FROM TABLE
def get_table(conn, name: str, mode: int = 0):
    cursor = conn.cursor()
    if name not in ALLOWED_TABLES:
        return {"error": "Invalid table"}
    cursor.execute(f"SELECT * FROM {name}")
    rows = cursor.fetchall()
    if not rows:
        return {"error": "No data"}
    output_rows = []
    base_headers = [col[0] for col in cursor.description]
    extra_headers = []
    for row in rows:
        item = dict(row)
        if mode >= 1:
            if "additionalinfo" in item and item["additionalinfo"]:
                try:
                    extra = json.loads(item["additionalinfo"])
                    for key, value in extra.items():
                        item[key] = value
                        if key not in extra_headers:
                            extra_headers.append(key)
                    item.pop("additionalinfo", None)
                except json.JSONDecodeError:
                    item["json_error"] = "Invalid JSON"
        output_rows.append(item)
    headers = base_headers + extra_headers
    if mode == 0:
        return rows
    elif mode == 1:
        return {
            "title": headers,
            "content": output_rows
        }
    elif mode == 2:
        return output_rows
    return {"error": "Invalid mode"}

#CREATE PRODUCT
def create_product(conn, input: dict):
    #TA
    now = currentdatetime()
    events = []
    data = {}
    #RULES
    for field in ALLOWED_FIELDS_PRODUCTS:
        data.setdefault(field, None)
    #MORE RULES
    for field, value in input.items():
        field = FIELD_ALIAS.get(field, field)
        if field not in ALLOWED_FIELDS_PRODUCTS:
            events.append(f"Field not allowed -> {field}")
            continue
        if isinstance(value, str):
            value = value.strip()
        data[field] = value
    #NAME IS REQUIRED
    if not data.get("name"):
        return {"error": "name_required"}
    #
    if not data.get("gtin"):
        data["gtin"] = generate_internal_gtin(conn)
        data["gtin_type"] = "internal"
    raw_qty = data.get("qty_value")
    if isinstance(raw_qty, str):
        if not data.get("qty_unit"):
            if not raw_qty.isnumeric():
                qty_value, unit_symbol = parse_qty_input(raw_qty)
                data["qty_value"] = qty_value
                data["qty_unit"] = unit_symbol
    #MAKE IT
    sql = f"""
        INSERT INTO products (
            gtin,
            gtin_type,
            code,
            brand,
            manufacturer,
            name,
            qty_value,
            qty_default,
            qty_unit,
            category,
            info,
            note,
            madein,
            status,
            created,
            updated
        )
        VALUES ({PLACEHOLDER}, 
                {PLACEHOLDER}, 
                {PLACEHOLDER}, 
                {PLACEHOLDER}, 
                {PLACEHOLDER}, 
                {PLACEHOLDER}, 
                {PLACEHOLDER}, 
                {PLACEHOLDER}, 
                {PLACEHOLDER}, 
                {PLACEHOLDER}, 
                {PLACEHOLDER}, 
                {PLACEHOLDER}, 
                {PLACEHOLDER}, 
                {PLACEHOLDER}, 
                {PLACEHOLDER}, 
                {PLACEHOLDER})
    """
    #SEND IT
    with conn:
        conn.execute(
            sql, 
            (
                str(data["gtin"]),
                data["gtin_type"],
                data["code"],
                data["brand"],
                data["manufacturer"],
                data["name"],
                data["qty_value"],
                data["qty_default"],
                data["qty_unit"],
                data["category"],
                data["info"],
                data["note"],
                data["madein"],
                "active",
                now,
                now
            )
        )
    return {
        "info": "Product created",
        "gtin": data["gtin"],
        "events": events
    }

#GET PRODUCT DATA
def get_product(conn, gtin: str):
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM products WHERE gtin=?",
        (gtin,)
    )
    row = cursor.fetchone()
    if not row:
        return {"error": "Product not found"}
    product = dict(row)
    if product.get("additionalinfo"):
        additional = json.loads(product["additionalinfo"] or "{}")
        product.pop("additionalinfo")
        product.update(additional)
    return product
