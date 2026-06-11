#|==============================================================|#
# Made by IntSPstudio
# Thank you for using this plugin!
# ID: 980001023
#|==============================================================|#

#SETTINGS
import click
from cli.utils import needs_conn, print_click_result
from cli.dictionary import create_dictionary_wiz
from core.products import get_or_create_complete_product

#MAIN
@click.group(name="prd")
def pdb_group():
    """- Product database commands"""
    pass

#CREATE NEW PRODUCT
@pdb_group.command(name="create")
@needs_conn
def create_product(conn):
    """- Add a new product via wizard"""