#|==============================================================|#
# Made by IntSPstudio
# Thank you for using this plugin!
# ID: 980001023
#|==============================================================|#

#SETTINGS
import re

#
def boring_text(input, mode: int):
    if mode == 0:
        return str("").join(i for i in input if i.isalnum())
    elif mode == 1:
        return re.sub(r"[^a-zA-Z0-9_-.,!# ]","",input)