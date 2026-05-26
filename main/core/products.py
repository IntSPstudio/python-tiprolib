#|==============================================================|#
# Made by IntSPstudio
# Thank you for using this plugin!
# ID: 980001023
#|==============================================================|#

#SETTINGS
from core import organizations, identifiers, locations
from utils.parsers import parse_qty_input
from core.settings import FIELD_ALIAS_BASIC
import sqlite3

#CREATE PRODUCT
def create_product(conn, input: dict):
    events =[]
    data ={}