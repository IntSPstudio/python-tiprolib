#|==============================================================|#
# Made by IntSPstudio
# Thank you for using this plugin!
# ID: 980001023
#|==============================================================|#

#SETTINGS
import sqlite3
from database.adapter import PLACEHOLDER
from utils.parsers import parse_qty_input
from utils.textutils import boring_text

#ADD NEW PRICE TO PRODUCT PRICE HISTORY
def add_price(conn, product_identifier, value, place=None):
    cursor = conn.cursor()
    resolved_product_id = None
    #CHECK IDENTIFIERS
    cursor.execute(
        f"SELECT product_id FROM identifiers WHERE value = {PLACEHOLDER}",
        (str(product_identifier).strip(),)
    )
    row = cursor.fetchone()
    #IF IDENTIFIER FOUND:
    if row:
        resolved_product_id = row[0]
    #PRODUCT ID CHECK
    else:
        try:
            prod_id_int = int(product_identifier)
            cursor.execute(
                f"SELECT id FROM products WHERE id = {PLACEHOLDER}",
                (prod_id_int,)
            )
            p_row = cursor.fetchone()
            if p_row:
                resolved_product_id = p_row[0]
        except (ValueError, TypeError):
            pass       
    #PRODUCT ID IS MUST
    if not resolved_product_id:
        return {"error": "product_not_found"}
    #LOCATION
    resolved_location_id = None
    resolved_organization_id = None
    if place is not None:
        #DISPLAY NAME -> SYSTEM NAME
        loc_key = boring_text(place, 3)
        cursor.execute(
            f"SELECT id, organization_id FROM locations WHERE key = {PLACEHOLDER}",
            (loc_key,)
        )
        loc_row = cursor.fetchone()
        if loc_row:
            resolved_location_id = loc_row[0]
            resolved_organization_id = loc_row[1]
        else:
            try:
                loc_id_int = int(place)
                cursor.execute(
                    f"SELECT id, organization_id FROM locations WHERE id = {PLACEHOLDER}",
                    (loc_id_int,)
                )
                loc_row = cursor.fetchone()
                if loc_row:
                    resolved_location_id = loc_row[0]
                    resolved_organization_id = loc_row[1]
            except (ValueError, TypeError):
                pass
        if not resolved_location_id:
            return {"error": "location_not_found"}
    #ADD PRICE
    try:
        parsed_data = parse_qty_input(str(value))
        price_value = parsed_data["value"]
        currency_value = parsed_data["unit"] or "eur" 
    except ValueError as e:
        return {"error": f"invalid_price_format: {str(e)}"}
    #SAVE ALL TO DATABASE
    try:
        cursor.execute(
            f"""
            INSERT INTO price_history (
                product_id, price, currency, location_id, organization_id
            )
            VALUES ({PLACEHOLDER}, {PLACEHOLDER}, {PLACEHOLDER}, {PLACEHOLDER}, {PLACEHOLDER})
            """,
            (
                resolved_product_id, 
                price_value, 
                currency_value, 
                resolved_location_id, 
                resolved_organization_id
            )
        )
        conn.commit()
        return {"success": True, "id": cursor.lastrowid}
    except sqlite3.Error as e:
        return {"error": f"database_error: {str(e)}"}