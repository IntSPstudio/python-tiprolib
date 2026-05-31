#|==============================================================|#
# Made by IntSPstudio
# TIPROLIB PDB
# Thank you for using this plugin!
# Version: 0.0.0.0
# ID: 980001023
#|==============================================================|#

#SETTINGS
from api.app import create_app
from config import DEBUG

#MAIN
def main():
    app = create_app()
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=DEBUG,
    )

#START
if __name__ == "__main__":
    main()