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
from core.locations import get_or_create_loc

#MAIN
@click.group(name="loc")
def loc_group():
    """- Locations"""
    pass

#GET ALL
@loc_group.command(name="get")
@click.argument('select', type=str)
@click.argument('target', required=False)
@needs_conn
def get_locations(conn, select, target):
    """- Options: all, id"""
    #DATA
    output =""
    if select == "all":
        output = print_crud_data(get_all(conn, "locations"))
    elif select == "id":
        if target:
            output = print_crud_data(get_by_id(conn, "locations", target))
    if output:
        print_click_result({"results":output})

#CREATE NEW PRODUCT
@loc_group.command(name="create")
@needs_conn
def create_location(conn):
    """- Add a new location via wizard"""
    #DATA
    output = create_dictionary_wiz("add_locations")
    results = get_or_create_loc(conn,output)
    print_click_result(results)