#|==============================================================|#
# Made by IntSPstudio
# Thank you for using this plugin!
# ID: 980001023
#|==============================================================|#

#SETTINGS
from flask import Blueprint, jsonify, request
from database import get_conn
from core.crud import get_all, get_by_id
from core.organizations import get_or_create_org
organizations_bp = Blueprint("organizations", __name__)

#
@organizations_bp.get("/api/organizations")
def list_org():
    conn = get_conn()
    try:
        return jsonify(get_all(conn, "organizations"))
    finally:
        conn.close()

@organizations_bp.get("/api/organizations/<org_name>")
def get_org_by_id(org_name):
    conn = get_conn()
    try:
        org_id = get_or_create_org(conn, org_name, "", 0)
        if org_id:
            result = get_by_id(conn, "organizations", org_id)
            status_code = 404 if result.get("error") else 200
            return jsonify(result), status_code
    finally:
        conn.close()