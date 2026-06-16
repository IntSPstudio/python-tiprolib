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

#MAIN
@click.group(name="jrn")
def jrn_group():
    """- Journal"""
    pass

#GET ALL
@jrn_group.command(name="get")
@click.argument('select', type=str)
@click.argument('target', required=False)
@needs_conn
def get_journals(conn, select, target):
    """- Options: all, id"""
    #DATA
    output =""
    if select == "all":
        output = print_crud_data(get_all(conn, "journal"))
    elif select == "id":
        if target:
            output = print_crud_data(get_by_id(conn, "journal", target))
    if output:
        print_click_result({"results":output})