#|==============================================================|#
# Made by IntSPstudio
# Thank you for using this plugin!
# ID: 980001023
#|==============================================================|#

#RULES
ALLOWED_TABLES = [
    "products",
    "price_history"
]

FIELD_ALIAS = {
    "qty": "qty_value",
    "qtyu": "qty_unit",
    "qtyd": "qty_default",
    "cat": "category"
}

ALLOWED_FIELDS = {
    "products": {
        "id",
        "gtin",
        "gtin_type",
        "code",
        "brand",
        "manufacturer",
        "name",
        "qty_value",
        "qty_default",
        "qty_unit",
        "info",
        "note",
        "madein",
        "additionalinfo",
        "status",
        "category"
    }
}

ALLOWED_FIELDS_PRODUCTS = ALLOWED_FIELDS["products"]
