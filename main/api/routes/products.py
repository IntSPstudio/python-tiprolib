#|==============================================================|#
# Made by IntSPstudio
# Thank you for using this plugin!
# ID: 980001023
#|==============================================================|#

#SETTINGS
from flask import Blueprint, jsonify, request
from database import get_conn
from core.products import get_product, search_products 

products_bp = Blueprint("products", __name__)

#GET BY ID
def get_product_by_id(product_id):
    conn = get_conn()
    try:
        result = get_product(conn, product_id)
        if "error" in result:
            return jsonify(result), 404
        return jsonify(result), 200
    finally:
        conn.close()

#SEARCH PRODUCTS
def list_and_search_products():
    query = request.args.get("q", "").strip() or request.args.get("query", "").strip()
    limit_param = request.args.get("limit", 50)
    try:
        slimit = int(limit_param)
    except ValueError:
        slimit = 50

    conn = get_conn()
    try:
        result = search_products(conn, query, slimit=slimit)
        return jsonify(result), 200
    finally:
        conn.close()

#ALL ALIASES OPTIONS
URL_ALIASES = ["products", "product", "prd"]

for alias in URL_ALIASES:
    products_bp.add_url_rule(
        f"/api/{alias}",
        view_func=list_and_search_products,
        methods=["GET"],
        strict_slashes=False
    )
    products_bp.add_url_rule(
        f"/api/{alias}/<int:product_id>",
        view_func=get_product_by_id,
        methods=["GET"]
    )