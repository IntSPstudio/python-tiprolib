#|==============================================================|#
# Made by IntSPstudio
# Thank you for using this plugin!
# ID: 980001023
#|==============================================================|#

#SETTINGS
from datetime import datetime

#BASIC TIME
def currentdatetime(mode: int = 0):
    if mode == 0:
        now = str(datetime.now().isoformat("#", "auto"))
        now = now.replace("-", ".")
        now = now.replace("#", "-")
    elif mode == 1:
        now = str(datetime.now().strftime("%Y.%m.%d %H:%M:%S"))
    return now