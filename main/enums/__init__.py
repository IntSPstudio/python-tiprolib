#|==============================================================|#
# Made by IntSPstudio
# Thank you for using this plugin!
# ID: 980001023
#|==============================================================|#

#SETTINGS
from config import DATABASE_TYPE
if DATABASE_TYPE == "sqlite":
    from .sqlite import get_conn