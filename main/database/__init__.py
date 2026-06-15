#|==============================================================|#
# Made by IntSPstudio
# Thank you for using this plugin!
# ID: 980001023
#|==============================================================|#

#SETTINGS
from config import DATABASE_TYPE
if DATABASE_TYPE == "sqlite":
    from .sqlite import get_conn
elif DATABASE_TYPE == "mariadb":
    from .mariadb import get_conn
else:
    raise ValueError(f"Unsupported database type: {DATABASE_TYPE}")