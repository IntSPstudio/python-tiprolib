#|==============================================================|#
# Made by IntSPstudio
# Thank you for using this plugin!
# ID: 980001023
#|==============================================================|#

#SETTINGS
import sys
from utils.printer import printer, print_crud_data
from utils.prompt import cli_screen_clear
from enums.status import Status
from cli.dictionary import create_dictionary_wiz
from core.crud import get_all, get_by_id, update_status, update_record
from core.products import get_or_create_complete_product, get_product, search_products
from core.pricing import add_price
from core.categories import get_or_create_cat
from core.organizations import get_or_create_org, get_organization_by_key
from core.locations import get_or_create_loc
from core.identifiers import get_by_identifier

#COMMAND LINE INTERFACE
def run_cli(conn):
    #START
    cli_screen_clear()
    #
    # INDEX
    #
    if len(sys.argv) < 2:
        printer("")
        printer("/Index")
        printer("            *** Welcome! Available commands ***")
        printer("")
        printer(" -Products")
        printer(" -Identifiers")
        printer(" -Inventory")
        printer(" -Organizations")
        printer(" -Locations")
        printer(" -Journal")
        printer("")
    #OPTIONS
    else:
        results ={}
        master = sys.argv[1]
        #
        # PRODUCTS
        #
        if master == "product" or master == "products" or master == "prd":
            if len(sys.argv) < 3:
                printer("")
                printer("            *** Products: Available commands ***")
                printer("")
                printer(" -Get ID/ALL")
                printer(" -Lookup QUERY")
                printer(" -Create")
                printer(" -Add price ID/IDENTIFIER PRICE LOCATION")
            else:
                #GET ALL PRODUCTS WITHOUT ADD INFO
                if len(sys.argv) == 4  and sys.argv[2] == "get" and sys.argv[3] == "all":
                    output = get_all(conn, "products")
                    results = print_crud_data(output)
                #GET ID
                if len(sys.argv) == 5 and sys.argv[2] == "get" and sys.argv[3] == "id" and sys.argv[4]:
                    output = get_product(conn, sys.argv[4])
                    results = output["result"]
                #SEARCH
                elif len(sys.argv) == 4 and sys.argv[2] == "lookup" and sys.argv[3]:
                    output = search_products(conn, sys.argv[3])
                    results = output["results"]
                #CREATE PRODUCT
                elif len(sys.argv) == 3 and sys.argv[2] == "create":
                    #CREATING CONTENT
                    output = create_dictionary_wiz("add_complete_product")
                    results = get_or_create_complete_product(conn,output)
                #PRICING
                if len(sys.argv) == 6 and sys.argv[2] == "add" and sys.argv[3] == "price" and sys.argv[4] and sys.argv[5]:
                    # 4: Product id or identifier
                    # 5: Price
                    output = add_price(conn, sys.argv[4], sys.argv[5])
                    results = output
                #PRICING
                if len(sys.argv) == 7 and sys.argv[2] == "add" and sys.argv[3] == "price" and sys.argv[4] and sys.argv[5] and sys.argv[6]:
                    # 4: Product id or identifier
                    # 5: Price
                    # 6: Location
                    output = add_price(conn, sys.argv[4], sys.argv[5], sys.argv[6])
                    results = output
        #
        # IDENTIFIERS
        #
        if master == "identifiers" or master == "code" or master == "gtin":
            if len(sys.argv) < 3:
                printer("")
                printer("            *** Identifiers: Available commands ***")
                printer("")
                printer(" -Get ALL/CODE")
            else:
                #GET
                if len(sys.argv) == 4  and sys.argv[2] == "get" and sys.argv[3]:
                    if sys.argv[3] == "all":
                        output = get_all(conn, "identifiers")
                        results = print_crud_data(output)
                    else:
                        output = get_by_identifier(conn, sys.argv[3])
                        if output:
                            results = output["results"]
        #
        # CATEGORIES
        #
        if master == "categories" or master == "category" or master == "cat":
            if len(sys.argv) < 3:
                printer("")
                printer("            *** Categories: Available commands ***")
                printer("")
                printer(" - get ALL")
                printer(" - create NAME INFO")
                printer("")
            else:
                #GET ALL
                if len(sys.argv) == 4  and sys.argv[2] == "get" and sys.argv[3] == "all":
                    output = get_all(conn, "categories")
                    results = print_crud_data(output)
                #GET OR CREATE CATEGORIES
                elif len(sys.argv) == 4 and sys.argv[2] == "create" and sys.argv[3]:
                    results = get_or_create_cat(conn,sys.argv[3],"")
                elif len(sys.argv) == 5 and sys.argv[2] == "create" and sys.argv[3] and sys.argv[4]:
                    results = get_or_create_cat(conn, sys.argv[3], sys.argv[4])
        #
        # INVENTORY
        #
        elif master == "inventory" or master == "inv":
            if len(sys.argv) < 3:
                printer("")
                printer("            *** Inventory: Available commands ***")
                printer("")
        #
        # ORGANIZATIONS
        #
        elif master == "organizations" or master == "org":
            if len(sys.argv) < 3:
                printer("")
                printer("            *** Organizations: Available commands ***")
                printer("")
                printer(" - get all/id")
                printer(" - create NAME INFO")
                printer(" - status STATE ID ")
                printer("")
            else:
                #GET ALL
                if len(sys.argv) == 4  and sys.argv[2] == "get" and sys.argv[3]:
                    if sys.argv[3] == "all":
                        output = get_all(conn, "organizations")
                    else:
                        output = get_by_id(conn, "organizations", sys.argv[3])
                    results = print_crud_data(output)
                #GET OR CREATE ORGANIZATIONS
                elif len(sys.argv) == 4 and sys.argv[2] == "create" and sys.argv[3]:
                    results = get_or_create_org(conn,sys.argv[3],"")
                elif len(sys.argv) == 5 and sys.argv[2] == "create" and sys.argv[3] and sys.argv[4]:
                    results = get_or_create_org(conn, sys.argv[3], sys.argv[4])
                #STATUS
                """
                elif len(sys.argv) == 5 and sys.argv[2] == "status" and sys.argv[3] and sys.argv[4]:
                    if sys.argv[3] == "active":
                        results = update_status(conn, "organizations", sys.argv[4], Status.ACTIVE.value)
                    elif sys.argv[3] == "passive":
                        results = update_status(conn, "organizations", sys.argv[4], Status.PASSIVE.value)
                    elif sys.argv[3] == "delete":
                        results = update_status(conn, "organizations", sys.argv[4], Status.DELETED.value)"""
        #
        # LOCATIONS
        #
        elif master == "locations" or master == "loc" or master == "places":
            if len(sys.argv) < 3:
                printer("")
                printer("            *** Locations: Available commands ***")
                printer("")
                printer(" - get all/id")
                printer(" - create")
                printer("")
            else:
                #GET ALL OR ONE
                if len(sys.argv) == 4  and sys.argv[2] == "get" and sys.argv[3]:
                    if sys.argv[3] == "all":
                        output = get_all(conn, "locations")
                    else:
                        output = get_by_id(conn, "locations", sys.argv[3])
                    results = print_crud_data(output)
                #GET OR CREATE LOCATIONS
                elif len(sys.argv) == 3 and sys.argv[2] == "create":
                    output = create_dictionary_wiz("add_locations")
                    results = get_or_create_loc(conn,output)
                #EDIT BY ID
                if len(sys.argv) == 6  and sys.argv[2] == "edit" and sys.argv[3] and sys.argv[4] and sys.argv[5]:
                    # 3: ID
                    # 4: KEY
                    # 5: VALUE
                    data = {sys.argv[4] : sys.argv[5]}
                    output = update_record(conn, "locations", sys.argv[3], data)
                    results = output
        #
        # OUTPUT
        #
        if results:
            printer("Results:")
            if isinstance(results, list):
                    for i in results:
                        printer(i)
            elif isinstance(results, dict):
                for key, value in results.items():
                    printer(f"{key}: {value}")
            else:
                printer(results)