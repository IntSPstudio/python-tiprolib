#|==============================================================|#
# Made by IntSPstudio
# Thank you for using this plugin!
# ID: 980001023
#|==============================================================|#

#SETTINGS
import click
from functools import wraps
from utils.printer import printer

#CONNECTION
def needs_conn(f):
    @click.pass_context
    @wraps(f)
    def wrapper(ctx, *args, **kwargs):
        ctx_obj = ctx.obj or {}
        conn = ctx_obj.get("conn")
        if not conn:
            click.secho("Error: Database connection not found.", fg="red", bold=True)
            ctx.exit(1)
        return f(conn, *args, **kwargs)
    return wrapper

#BASIC PRINT
def print_click_result(result):
    #IF EMPTY
    if not result:
        click.secho("Error: The system returned an empty response.", fg="red", bold=True)
        return
    #IF DICTIONARY
    if isinstance(result, dict):
        #ERRORS
        if "error" in result:
            #MAIN
            click.secho(f"\n Error: {result['error']}", fg="red", bold=True)
            #INFO
            if "events" in result and result["events"]:
                click.echo("Details:")
                for event in result["events"]:
                    click.echo(f"  - {event}")
            return
        #BASICS
        status = result.get("status")
        if status:
            click.echo(f"Status: {status}")
        item_id = result.get("id")
        if item_id:
            click.echo(f"ID: {item_id}")
        success = result.get("success")
        if success:
            click.echo(f"Succes: {success}")
        #RESULTS
        if result.get("results"):
            if isinstance(result["results"], list):
                    for i in result["results"]:
                        printer(i)
            elif isinstance(result["results"], dict):
                for key, value in result["results"].items():
                    printer(f"{key}: {value}")
            else:
                printer(result["results"])
        #ADDITIONAL EVENTS
        if "events" in result and result["events"]:
            click.echo("\nInfo:")
            for event in result["events"]:
                click.echo(f"  {event}")