#|==============================================================|#
# Made by IntSPstudio
# Thank you for using this plugin!
# ID: 980001023
#|==============================================================|#

#SETTINGS
from flask import Blueprint, jsonify
from config import APP_NAME
health_bp = Blueprint("health", __name__)

#API SOURCE
@health_bp.get("/api")
def api_index():
    return jsonify({
        "app": APP_NAME,
        "status": "ok",
        "routes": {
            "api": "/api",
            "health": "/api/health",
            "organizations": "/api/organizations",
            "products": "/api/products/"
        },
    })

#HEALT SETTINGS
@health_bp.get("/api/health")
def health():
    return jsonify({"status": "ok"})