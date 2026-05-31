#|==============================================================|#
# Made by IntSPstudio
# Thank you for using this plugin!
# ID: 980001023
#|==============================================================|#

#SETTINGS
from flask import Blueprint, render_template
web_bp = Blueprint("web", __name__)

@web_bp.get("/")
def index():
    return render_template("index.html")