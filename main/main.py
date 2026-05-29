#|==============================================================|#
# Made by IntSPstudio
# TIPROLIB PDB
# Thank you for using this plugin!
# Version: 0.0.0.0
# ID: 980001023
#|==============================================================|#

#SETTINGS
from database import get_conn
from database.setup import initialize_basics
from cli.commands import run_cli

#MAIN LOOP
def main():
    conn = get_conn()
    initialize_basics(conn)
    run_cli(conn)

#START
if __name__ == "__main__":
    main()