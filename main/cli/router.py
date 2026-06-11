#|==============================================================|#
# Made by IntSPstudio
# Thank you for using this plugin!
# ID: 980001023
#|==============================================================|#

#SETTINGS
import click
from cli.products import pdb_group
from cli.organization import org_group

#MAIN
@click.group()
def router():
    """Tiprolib product database"""
    pass

#PLUGINS
router.add_command(pdb_group)
router.add_command(org_group)

#START COMMAND LINE
def run_cli(conn):
    router(obj={
        "conn": conn,
        "debug_mode": True
    })