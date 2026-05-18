#|==============================================================|#
# Made by IntSPstudio
# Thank you for using this plugin!
#
# ID: 980001023
#|==============================================================|#

#SETTINGS
from database import get_conn
from database.schema import create_database
from cli.commands import run_cli

#MAIN LOOP
def main():
    conn = get_conn()
    create_database(conn)
    run_cli(conn)

#START
if __name__ == "__main__":
    main()