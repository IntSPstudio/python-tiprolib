#|==============================================================|#
# Made by IntSPstudio
# Thank you for using this plugin!
# ID: 980001023
#|==============================================================|#

#SETTINGS
import sys
from utils.printer import printer

#COMMAND LINE INTERFACE
def run_cli(conn):
    try:
        #INDEX
        if len(sys.argv) < 2:
            printer("")
            printer("            *** Welcome! Available commands ***")
            printer("")
    except:
        printer("Error")