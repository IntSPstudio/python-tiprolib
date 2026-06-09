#|==============================================================|#
# Made by IntSPstudio
# Thank you for using this plugin!
# ID: 980001023
#|==============================================================|#

#SETTINGS
from flask import Flask
from api.routes.health import health_bp
from api.routes.web import web_bp
from api.routes.organizations import organizations_bp
from api.routes.categories import categories_bp
from api.routes.products import products_bp
from database import get_conn
from database.setup import initialize_basics

#MAIN
def create_app():
    app = Flask(
        __name__,
        template_folder="../website/templates",
        static_folder="../website/static",
    )

    initialize_database() #CONNECT
    app.register_blueprint(health_bp) #BASIC
    app.register_blueprint(web_bp) #WEBSITE
    app.register_blueprint(organizations_bp) #ORGANIZATIONS
    app.register_blueprint(categories_bp) #CATEGORIES
    app.register_blueprint(products_bp) #PRODUCTS
    return app

#CONNECT
def initialize_database():
    conn = get_conn()
    try:
        initialize_basics(conn)
    finally:
        conn.close()