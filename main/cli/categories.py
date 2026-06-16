#|==============================================================|#
# Made by IntSPstudio
# Thank you for using this plugin!
# ID: 980001023
#|==============================================================|#

#SETTINGS
import click
from cli.utils import needs_conn, print_click_result
from utils.printer import print_crud_data 
from core.crud import get_all, get_by_id
from core.categories import get_or_create_cat

#MAIN
@click.group(name="cat")
def cat_group():
    """- Category"""
    pass

#GET ALL
@cat_group.command(name="get")
@click.argument('select', type=str)
@click.argument('target', required=False)
@needs_conn
def get_cat(conn, select, target):
    """- Options: all, id"""
    #DATA
    output =""
    if select == "all":
        output = print_crud_data(get_all(conn, "categories"))
    elif select == "id":
        if target:
            output = print_crud_data(get_by_id(conn, "categories", target))
    if output:
        print_click_result({"results":output})

#CREATE
@cat_group.command(name="create")
@click.argument('name', type=str)
@click.argument('info', required=False)
@needs_conn
def create_cat(conn, name, info):
    """- Options: name and info"""
    if info:
        output = get_or_create_cat(conn, name, info)
    else:
        output = get_or_create_cat(conn, name)
    print_click_result(output)