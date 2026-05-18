#|==============================================================|#
# Made by IntSPstudio
# Thank you for using this plugin!
# ID: 980001023
#|==============================================================|#

#SETTINGS
from config import DATABASE_TYPE

#CHECK
if DATABASE_TYPE == "sqlite":
    PLACEHOLDER = "?"
    AUTOINCREMENT = "AUTOINCREMENT"
else:
    PLACEHOLDER = "%s"
    AUTOINCREMENT = "AUTO_INCREMENT"