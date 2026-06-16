#|==============================================================|#
# Made by IntSPstudio
# Thank you for using this plugin!
# ID: 980001023
#|==============================================================|#

#SETTINGS
from config import DEBUG
import click
from cli.products import prd_group
from cli.organization import org_group
from cli.locations import loc_group
from cli.categories import cat_group
from cli.journal import jrn_group

#MAIN
@click.group()
def router():
    """Tiprolib product database"""
    pass

#PLUGINS
router.add_command(prd_group) #Products
router.add_command(org_group) #Organizations
router.add_command(loc_group) #Locations
router.add_command(cat_group) #Categories
router.add_command(jrn_group) #Journal

#START COMMAND LINE
def run_cli(conn):
    router(obj={
        "conn": conn,
        "debug_mode": DEBUG
    })