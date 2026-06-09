#|==============================================================|#
# Made by IntSPstudio
# Thank you for using this plugin!
# ID: 980001023
#|==============================================================|#

#SETTINGS
import sqlite3
import database.adapter as adpt
from utils.parsers import parse_qty_input 

#ADD NEW PRICE TO PRODUCT PRICE HISTORY
def add_price(conn, product_identifier, value, place=None):
    cursor = conn.cursor()
    resolved_product_id = None
    #CHECK IDENTIFIERS
    cursor.execute(
        f"SELECT product_id FROM identifiers WHERE value = {adpt.PLACEHOLDER}",
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
                f"SELECT id FROM products WHERE id = {adpt.PLACEHOLDER}",
                (prod_id_int,)
            )
            p_row = cursor.fetchone()
            if p_row:
                resolved_product_id = p_row[0]
        #ERROR
        except (ValueError, TypeError):
            pass
    #ERROR
    if not resolved_product_id:
        return {"error": "product_not_found"}
    #ADD PRICE
    try:
        parsed_data = parse_qty_input(str(value))
        price_value = parsed_data["value"]
        currency_value = parsed_data["unit"] or "eur" 
    except ValueError as e:
        return {"error": f"invalid_price_format: {str(e)}"}
    #LOCATION
    
    #SAVE ALL TO DATABASE
    try:
        cursor.execute(
            f"""
            INSERT INTO price_history (product_id, price, currency, organization_id)
            VALUES ({adpt.PLACEHOLDER}, {adpt.PLACEHOLDER}, {adpt.PLACEHOLDER}, {adpt.PLACEHOLDER})
            """,
            (resolved_product_id, price_value, currency_value, place)
        )
        conn.commit()
        return {"success": True, "id": cursor.lastrowid}
    except sqlite3.Error as e:
        return {"error": f"database_error: {str(e)}"}