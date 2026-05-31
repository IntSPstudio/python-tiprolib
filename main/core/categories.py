#|==============================================================|#
# Made by IntSPstudio
# Thank you for using this plugin!
# ID: 980001023
#|==============================================================|#

#SETTINGS
import sqlite3
import database.adapter as adpt
from utils.textutils import boring_text

#GET OR CREATE
def get_or_create_cat(conn, name, description=None):
    #RULES
    name = boring_text(name,0)
    if name:
        #TRY
        cursor = conn.cursor()
        command = f"SELECT id FROM categories WHERE name = {adpt.PLACEHOLDER}"
        cursor.execute(command, (name,))
        row = cursor.fetchone()
        #IF EXISTS
        if row:
            return {"id": row[0]} 
        #CREATE
        try:
            command = f"INSERT INTO categories (name, info) VALUES ({adpt.PLACEHOLDER}, {adpt.PLACEHOLDER})"
            cursor.execute(command,(name, description))
            conn.commit()
            return {"id": cursor.lastrowid}
        #ERROR
        except sqlite3.IntegrityError:
            command = f"SELECT id FROM categories WHERE name = {adpt.PLACEHOLDER}"
            cursor.execute(command, (name,))
            row = cursor.fetchone()
            if row:
                return {"id": row[0]}
            raise
    return {"error":"Invalid name"}

#CREATE LINK PRODUCT - CATEGORY
def link_product_to_category(conn, product_id: int, category_id: int):
    if product_id and category_id:
        cursor = conn.cursor()
        query = f"""
            INSERT OR IGNORE INTO route_categories (product_id, category_id)
            VALUES ({adpt.PLACEHOLDER}, {adpt.PLACEHOLDER})
        """
        try:
            cursor.execute(query, (product_id, category_id))
            conn.commit()
            if cursor.rowcount > 0:
                return {"status": "linked", "product_id": product_id, "category_id": category_id}
            else:
                return {"status": "already_exists", "product_id": product_id, "category_id": category_id}
        except Exception as e:
            return {"status": "error", "message": str(e)}