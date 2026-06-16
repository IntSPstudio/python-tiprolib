#|==============================================================|#
# Made by IntSPstudio
# Thank you for using this plugin!
# ID: 980001023
#|==============================================================|#

#SETTINGS
import click
from cli.utils import needs_conn, print_click_result
from cli.dictionary import create_dictionary_wiz
from utils.printer import print_crud_data 
from core.crud import get_all, get_by_id
from core.products import get_or_create_complete_product


#MAIN
@click.group(name="prd")
def prd_group():
    """- Product database"""
    pass

#GET ALL
@prd_group.command(name="get")
@click.argument('select', type=str)
@click.argument('target', required=False)
@needs_conn
def get_products(conn, select, target):
    """- Options: all, id"""
    #DATA
    output =""
    if select == "all":
        output = print_crud_data(get_all(conn, "products"))
    elif select == "id":
        if target:
            output = print_crud_data(get_by_id(conn, "products", target))
    if output:
        print_click_result({"results":output})

#CREATE NEW PRODUCT
@prd_group.command(name="create")
@needs_conn
def create_product(conn):
    """- Add a new product via wizard"""
    #DATA
    output = create_dictionary_wiz("add_complete_product")
    results = get_or_create_complete_product(conn,output)
    print_click_result(results)