#|==============================================================|#
# Made by IntSPstudio
# Thank you for using this plugin!
# ID: 980001023
#|==============================================================|#

#SETTINGS
import sys
from core.products import (create_product, get_table)
from utils.printer import (printer, print_table)

#COMMAND LINE INTERFACE
def run_cli(conn):
    try:
        #INDEX
        if len(sys.argv) < 2:
            printer("")
            printer("            *** Welcome! Available commands ***")
            printer("")
            #printer("create                  | Create product to database")
            printer("products                | Show all products from database")
            #printer("update GTIN FIELD VALUE | Update product field value")
            #printer("status ID               | Change product status (Active / passive)")
            #printer("get GTIN VALUE          | Get product data. If value is empty show all")
            #printer("extra                   | Get or Add additional info")
            #printer("price add GTIN VALUE    | Add price history")
            #printer("price history GTIN      | Show price history")
            printer("")
            return
        #MAIN INPUT
        cmd = sys.argv[1]

        #ALL PRODUCTS
        if cmd == "products":
            results = get_table(conn, "products", 1)
            headers = results["title"]
            rows = results["content"]
            skip_cols = ["status", "created", "updated"]
            filtered_headers = [
                h for h in headers
                if h not in skip_cols
            ]
            filtered_rows = []
            for row in rows:
                filtered_rows.append([
                    row.get(header, "")
                    for header in filtered_headers
                ])
            results = print_table(filtered_headers, filtered_rows)
            for line in results:
                printer(line)
    except:
        printer("Error")