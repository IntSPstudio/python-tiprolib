#|==============================================================|#
# Made by IntSPstudio
# Thank you for using this plugin!
# ID: 980001023
#|==============================================================|#

#SETTINGS
import re

def boring_text(text_input, mode: int = 0) -> str:
    #RULES
    text = str(text_input or "").strip()
    if not text:
        return ""
    #BASIC
    if mode == 0:
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    #LETTERS AND DIGITS
    elif mode == 1:
        return re.sub(r'[^a-zA-Z0-9åäöÅÄÖ]', '', text)
    #PRODUCT CODE & INPUTS
    elif mode == 2:
        text = re.sub(r'\s+', ' ', text)
        return re.sub(r'[^a-zA-Z0-9åäöÅÄÖ .,$€&%+\-/()]', '', text).strip()
    #DATA KEYS
    elif mode == 3:
        text = text.lower()
        text = re.sub(r'[ \.\-]+', '_', text)
        text = re.sub(r'[^a-z0-9åäö_]', '', text)
        text = re.sub(r'_+', '_', text)
        return text.strip('_')
    return text