#|==============================================================|#
# Made by IntSPstudio
# Thank you for using this plugin!
# ID: 980001023
#|==============================================================|#

#SETTINGS
from flask import Blueprint, jsonify
from database import get_conn
from core.crud import get_all, get_by_id
from core.organizations import get_organization_by_key

organizations_bp = Blueprint("organizations", __name__)

#GET ALL
def list_org():
    conn = get_conn()
    try:
        return jsonify(get_all(conn, "organizations"))
    finally:
        conn.close()

#GET ONE
def get_org_by_key(org_name):
    conn = get_conn()
    try:
        result = get_organization_by_key(conn, org_name)
        status_code = 404 if "error" in result else 200
        return jsonify(result), status_code
    finally:
        conn.close()

#ALL ALIASES OPTIONS
URL_ALIASES = ["org", "organization", "organizations", "brand", "brands"]
for alias in URL_ALIASES:
    organizations_bp.add_url_rule(
        f"/api/{alias}",
        view_func=list_org,
        methods=["GET"],
        strict_slashes=False
    )
    organizations_bp.add_url_rule(
        f"/api/{alias}/<org_name>",
        view_func=get_org_by_key,
        methods=["GET"]
    )