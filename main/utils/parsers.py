#|==============================================================|#
# Made by IntSPstudio
# Thank you for using this plugin!
# ID: 980001023
#|==============================================================|#

#SETTINGS
import re

#SEPARATE QTY UNIT FROM QTY VALUE
def parse_qty_input(value):
    match = re.match(r"^\s*(\d+(?:[.,]\d+)?)\s*([a-zA-Z€$]+)?\s*$", value)
    if not match:
        raise ValueError(f"Invalid format: {value}")
    qty = float(match.group(1).replace(",", "."))
    unit = match.group(2)
    #RULES
    if unit:
        unit = unit.lower()
        #CURRENCY
        if unit in {"€", "eur", "euro"}:
            unit = "eur"
        elif unit in {"$", "usd", "dollar"}:
            unit = "usd"
        #MORE RULES
        elif unit in {"g", "kg", "ml", "l"}:
            pass
        else:
            raise ValueError(f"Unknown unit/currency: {unit}")
    else:
        unit = None
    return {"value": qty, "unit": unit}