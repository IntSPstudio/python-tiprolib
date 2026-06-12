#|==============================================================|#
# Made by IntSPstudio
# Thank you for using this plugin!
# ID: 980001023
#|==============================================================|#

#SETTINGS
import re
from core.categories import get_or_create_cat, link_product_to_category
from core.identifiers import generate_internal_code, get_or_create_type, guess_identifier_type
from core.organizations import get_or_create_org
from core.settings import ALLOWED_FIELDS_PRD, FIELD_ALIAS, PRODUCT_UPDATE_FIELDS
from database.adapter import PLACEHOLDER
from utils.parsers import parse_qty_input
from utils.textutils import boring_text

#GET OR CREATE COMPLETE PRODUCT WITH DICTIONARY
def get_or_create_complete_product(conn, input_dict: dict, cre_ide: int = 0):
    cursor = conn.cursor()
    events = []
    data = normal_product_data(input_dict, events)
    identifier_data = normal_identifier_data(input_dict, events)
    #FIRST RULES
    if not input_dict:
        return {"error": "invalid input"}
    if not data.get("name") and not identifier_data.get("value"):
        return {"error": "name_or_identifier_required", "events": events}   
    #IDEN CHECK
    existing_identifier = None
    if identifier_data.get("value"):
        existing_identifier = get_identifier(cursor, identifier_data["value"])
        if existing_identifier and existing_identifier["product_id"]:
            return {
                "status": "exists",
                "product_id": existing_identifier["product_id"],
                "identifier_id": existing_identifier["id"],
                "events": events,
            }        
    #GET BRAND
    if data.get("brand_id"):
        data["brand_id"] = resolve_organization(conn, data["brand_id"], events)
    #GET CATEGORY
    #if data.get("category_id"):
    #    data["category_id"] = resolve_category(conn, data["category_id"], events)
    #QTY RULES
    if isinstance(data.get("qty_default"), str):
        qty = parse_qty_input(data["qty_default"])
        data["qty_default"] = qty["value"]
        data["qty_unit"] = data.get("qty_unit") or qty["unit"]
    if data.get("qty_default") is None:
        data["qty_default"] = 1
    if not data.get("qty_unit"):
        data["qty_unit"] = "pcs"
    #BASIC WEIGHT SETTINGS
    if data.get("weight_default") and isinstance(data.get("weight_default"), str):
        weight = parse_qty_input(data["weight_default"])
        data["weight_default"] = weight["value"]
        data["weight_unit"] = data.get("weight_unit") or weight["unit"] or "g"
    #NAME CHECK
    #if not data.get("name"):
    #    data["name"] = f"Product {identifier_data['value']}"
    if not data.get("name"):
        suffix = identifier_data.get("value") or "Unnamed"
        data["name"] = f"Product {suffix}"
    #KEY GENERATION
    data["key"] = boring_text(data["name"], 3)
    #INTERNAL IDENTIFIER CHECK 1
    if not identifier_data.get("value"):
        if cre_ide != 0:
            identifier_data["value"] = generate_internal_code(conn)
            identifier_data["type_id"] = resolve_identifier_type(conn, "internal", events)
            events.append(f"Generated internal identifier: {identifier_data['value']}")
        else:
            events.append("No identifier provided, skipping identifier creation")
    elif not identifier_data.get("type_id"):
        identifier_data["type_id"] = guess_identifier_type(conn, identifier_data["value"], events)
    else:
        identifier_data["type_id"] = resolve_identifier_type(conn, identifier_data["type_id"], events)
    #CHECK IF PRODUCT EXISTS
    product_id = get_existing_product(cursor, data)
    if not product_id:
        product_id = insert_product(cursor, data)
        events.append("Product created")
    else:
        events.append("Product exists")
    #CATEGORIES
    if input_dict.get("c1"):
        c1 = resolve_category(conn, input_dict.get("c1"), events)
        link_product_to_category(conn, product_id, c1)
        if input_dict.get("c2"):
            c2 = resolve_category(conn, input_dict.get("c2"), events)
            link_product_to_category(conn, product_id, c2)       
    #INTERNAL IDENTIFIER CHECK 2
    identifier_id = None
    if identifier_data.get("value"):
        if existing_identifier:
            identifier_id = existing_identifier["id"]
            cursor.execute(
                f"UPDATE identifiers SET product_id = {PLACEHOLDER}, updated = CURRENT_TIMESTAMP WHERE id = {PLACEHOLDER}",
                (product_id, identifier_id),
            )
            events.append("Existing identifier linked to product")
        else:
            identifier_id = insert_identifier(cursor, product_id, identifier_data)
            events.append("Identifier created")
    else:
        events.append("Product created without identifier")
    #SEND IT
    conn.commit()
    return {
        "status": "ok",
        "product_id": product_id,
        "identifier_id": identifier_id,
        "identifier": identifier_data.get("value"),
        "events": events,
    }

#GET PRODUCT
def get_product(conn, product_id: int):
    cursor = conn.cursor()
    cursor.execute(
        f"""
        SELECT 
            p.*, 
            o.name AS brand_name, 
            dt.code AS deposit_code
        FROM products p
        LEFT JOIN organizations o ON p.brand_id = o.id
        LEFT JOIN deposit_types dt ON p.deposit_type_id = dt.id
        WHERE p.id = {PLACEHOLDER}
        """,
        (product_id,),
    )
    row = cursor.fetchone()
    if not row:
        return {"error": "product_not_found"}
    columns = [column[0] for column in cursor.description]
    product = dict(zip(columns, row))
    #GET IDENTIFIERS
    product["identifiers"] = get_product_identifiers(conn, product_id)
    #GET CATEGORIES
    product["categories"] = get_product_categories(conn, product_id)
    return {"results": product}

#GET PRODUCT IDENTIFIERS
def get_product_identifiers(conn, product_id: int):
    cursor = conn.cursor()
    cursor.execute(
        f"""
        SELECT i.id, i.value, i.type_id, it.value AS type
        FROM identifiers i
        LEFT JOIN identifier_types it ON i.type_id = it.id
        WHERE i.product_id = {PLACEHOLDER}
        ORDER BY i.id
        """,
        (product_id,),
    )
    columns = [column[0] for column in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

#GET PRODUCT CATEGORIES
def get_product_categories(conn, product_id: int):
    cursor = conn.cursor()
    cursor.execute(
        f"""
        SELECT c.id, c.name, c.info
        FROM categories c
        JOIN route_categories rc ON c.id = rc.category_id
        WHERE rc.product_id = {PLACEHOLDER}
        """,
        (product_id,),
    )
    columns = [column[0] for column in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

#SEARCH PRODUCTS
def search_products(conn, query: str, slimit: int = 50):
    query = str(query or "").strip()
    if not query:
        return {"results": []}
    cursor = conn.cursor()
    like_value = f"%{query}%"
    flat_query = f"%{query.lower().replace(' ', '').replace('_', '')}%"
    
    cursor.execute(
        f"""
        SELECT DISTINCT
            p.id,
            p.key,
            p.name,
            p.qty_default,
            p.qty_unit,
            p.weight_default,
            p.weight_unit,
            p.status_id,
            o.name AS brand_name
        FROM products p
        LEFT JOIN organizations o ON p.brand_id = o.id
        LEFT JOIN route_categories rc ON p.id = rc.product_id
        LEFT JOIN categories c ON rc.category_id = c.id
        LEFT JOIN identifiers i ON p.id = i.product_id
        WHERE
            p.name LIKE {PLACEHOLDER}
            OR p.key LIKE {PLACEHOLDER}
            OR REPLACE(p.key, '_', '') LIKE {PLACEHOLDER}  -- Haku siivotulla avaimella
            OR o.name LIKE {PLACEHOLDER}
            OR c.name LIKE {PLACEHOLDER}
            OR i.value = {PLACEHOLDER}
        ORDER BY p.id DESC
        LIMIT {slimit}
        """,
        (like_value, like_value, flat_query, like_value, like_value, query),
    )
    columns = [column[0] for column in cursor.description]
    rows = cursor.fetchall()
    results = []
    for row in rows:
        product = dict(zip(columns, row))
        product_id = product["id"]
        #GET IDENTIFIERS
        product["identifiers"] = get_product_identifiers(conn, product_id)
        #GET CATEGORIES
        product["categories"] = get_product_categories(conn, product_id)
        results.append(product)
    return {"results": results}

#UPDATE PRODUCT
def update_product(conn, product_id: int, input_dict: dict):
    events = []
    if not product_id:
        return {"error": "product_id_required"}
    data = normal_product_data(input_dict or {}, events)
    data = {key: value for key, value in data.items() if key in PRODUCT_UPDATE_FIELDS and value is not None}
    if not data:
        return {"error": "no_valid_fields", "events": events}
    #CHOICES
    if data.get("brand_id"):
        data["brand_id"] = resolve_organization(conn, data["brand_id"], events)
    if isinstance(data.get("qty_default"), str):
        qty = parse_qty_input(data["qty_default"])
        data["qty_default"] = qty["value"]
        data["qty_unit"] = data.get("qty_unit") or qty["unit"]
    if isinstance(data.get("weight_default"), str):
        weight = parse_qty_input(data["weight_default"])
        data["weight_default"] = weight["value"]
        data["weight_unit"] = data.get("weight_unit") or weight["unit"] or "g"
    #UPDATE
    cursor = conn.cursor()
    assignments = [f"{field} = {PLACEHOLDER}" for field in data]
    assignments.append("updated = CURRENT_TIMESTAMP")
    cursor.execute(
        f"UPDATE products SET {', '.join(assignments)} WHERE id = {PLACEHOLDER}",
        (*data.values(), product_id),
    )
    if cursor.rowcount == 0:
        return {"error": "product_not_found", "events": events}
    conn.commit()
    return {"status": "ok", "product_id": product_id, "events": events}

#ADDITIONAL INFO KEYS
def resolve_extra_field(conn, key_name: str, display_name: str = None):
    cursor = conn.cursor()
    key_name = key_name.strip().lower().replace(" ", "_")
    cursor.execute(
        f"SELECT key_name FROM extra_field_definitions WHERE key_name = {PLACEHOLDER}", 
        (key_name,)
    )
    row = cursor.fetchone()
    if not row:
        d_name = display_name or key_name.capitalize()
        cursor.execute(
            f"INSERT INTO extra_field_definitions (key_name, display_name) VALUES ({PLACEHOLDER}, {PLACEHOLDER})",
            (key_name, d_name)
        )
        conn.commit()
        return key_name
    return row[0]

#
# FOR SYSTEM
#

def normal_product_data(input_dict, events):
    fields = set(ALLOWED_FIELDS_PRD) | {"key"}
    data = {field: None for field in fields}
    for raw_field, value in (input_dict or {}).items():
        field = map_field(raw_field)
        if field not in fields:
            if field not in {"value", "type_id", "identifier_info"}:
                events.append(f"Field ignored: {raw_field}")
            continue
        data[field] = value.strip() if isinstance(value, str) else value
    data.pop("id", None)
    data.pop("status_id", None)
    return data

def normal_identifier_data(input_dict, events):
    data = {"value": None, "type_id": None, "info": None}
    for raw_field, value in (input_dict or {}).items():
        field = map_field(raw_field)
        if field in {"value", "identifier"}:
            data["value"] = str(value).strip().replace(" ", "")
        elif field in {"type_id", "identifier_type", "gtin_type"}:
            data["type_id"] = str(value).strip().lower()
        elif field == "identifier_info":
            data["info"] = value
    if data["value"] == "":
        data["value"] = None
    return data

def map_field(field):
    if field in FIELD_ALIAS["add_complete_product"]:
        return FIELD_ALIAS["add_complete_product"][field]["name"]
    return FIELD_ALIAS["basic"].get(field, field)

def resolve_organization(conn, value, events):
    if isinstance(value, int) or str(value).isnumeric():
        return int(value)
    result = get_or_create_org(conn, str(value))
    if result.get("id"):
        events.append(f"Organization resolved: {value}")
        return result["id"]
    return 1

def resolve_category(conn, value, events):
    if isinstance(value, int) or str(value).isnumeric():
        return int(value)
    result = get_or_create_cat(conn, str(value))
    if result.get("id"):
        events.append(f"Category resolved: {value}")
        return result["id"]
    return None

def resolve_identifier_type(conn, value, events):
    if isinstance(value, int) or str(value).isnumeric():
        return int(value)
    result = get_or_create_type(conn, str(value))
    if result.get("id"):
        events.append(f"Identifier type resolved: {value}")
        return result["id"]
    return None

def get_identifier(cursor, value):
    cursor.execute(f"SELECT id, product_id FROM identifiers WHERE value = {PLACEHOLDER}", (value,))
    row = cursor.fetchone()
    return {"id": row[0], "product_id": row[1]} if row else None

def get_existing_product(cursor, data):
    key = data.get("key")
    brand_id = data.get("brand_id") or 1
    if not key:
        return None
    flat_key = key.replace("_", "")
    cursor.execute(
        f"""
        SELECT id FROM products
        WHERE REPLACE(key, '_', '') = {PLACEHOLDER}
        AND COALESCE(brand_id, 1) = {PLACEHOLDER}
        AND status_id = 1
        """,
        (flat_key, brand_id),
    )
    row = cursor.fetchone()
    return row[0] if row else None

def insert_product(cursor, data):
    clean_data = {}
    for key, value in data.items():
        if value is None:
            continue
        #if key == "extra" and isinstance(value, dict):
        #    value = json.dumps(value, ensure_ascii=False)
        clean_data[key] = value
    columns = ", ".join(clean_data.keys())
    placeholders = ", ".join([PLACEHOLDER] * len(clean_data))
    cursor.execute(
        f"INSERT INTO products ({columns}) VALUES ({placeholders})",
        tuple(clean_data.values()),
    )
    return cursor.lastrowid

def insert_identifier(cursor, product_id, data):
    cursor.execute(
        f"""
        INSERT INTO identifiers (product_id, value, type_id, info)
        VALUES ({PLACEHOLDER}, {PLACEHOLDER}, {PLACEHOLDER}, {PLACEHOLDER})
        """,
        (product_id, data["value"], data["type_id"], data.get("info")),
    )
    return cursor.lastrowid