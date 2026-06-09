#|==============================================================|#
# Made by IntSPstudio
# Thank you for using this plugin!
# ID: 980001023
#|==============================================================|#

#SETTINGS
from flask import Blueprint, jsonify
from database import get_conn
from core.crud import get_all

categories_bp = Blueprint("categories", __name__)

#GET ALL
def list_org():
    conn = get_conn()
    try:
        return jsonify(get_all(conn, "categories"))
    finally:
        conn.close()

#ALL ALIASES OPTIONS
URL_ALIASES = ["cat", "categories", "group", "groups"]
for alias in URL_ALIASES:
    categories_bp.add_url_rule(
        f"/api/{alias}",
        view_func=list_org,
        methods=["GET"],
        strict_slashes=False
    )