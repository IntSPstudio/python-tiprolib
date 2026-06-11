#|==============================================================|#
# Made by IntSPstudio
# Thank you for using this plugin!
# ID: 980001023
#|==============================================================|#

#SETTINGS
import click
from cli.utils import needs_conn

#MAIN
@click.group(name="org")
def org_group():
    """- Organizations"""
    pass

#GET ALL
@org_group.command(name="get")
@click.argument('select', type=str)
@click.argument('target', required=False)
@needs_conn
def get_org(conn, select, target):
    """- Options: all"""