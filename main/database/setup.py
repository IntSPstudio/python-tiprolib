#|==============================================================|#
# Made by IntSPstudio
# Thank you for using this plugin!
# ID: 980001023
#|==============================================================|#

#SETTINGS
from config import DATABASE_TYPE, DATABASES
from database.schema import create_database

#START
def initialize_basics(conn):
    #In the future these would not be recreated every time....
    create_database(conn)