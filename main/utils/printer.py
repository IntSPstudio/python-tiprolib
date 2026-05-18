#|==============================================================|#
# Made by IntSPstudio
# Thank you for using this plugin!
# ID: 980001023
#|==============================================================|#

#SETTINGS
from os import get_terminal_size as cli_size

#CLI INTERFACE PRINT
def printer(text: str):
    text = "=] " + str(text)
    try:
        limit = cli_size().columns - 1
        if len(text) > limit:
            print(text[:limit])
        else:
            print(text)
    except Exception as e:
        print(f"Error printing object: {e}")

#CLI INTERFACE PRINT
def print_table(headers, rows):
    output = []
    data = [headers] + rows
    widths = [
        max(
            len(str(row[i]))
            for row in data
        )
        for i in range(len(headers))
    ]
    for row in data:
        line = " | ".join(
            str(row[i]).ljust(widths[i])
            for i in range(len(row))
        )
        line = line.replace("None", "    ")
        output.append(line)
    return output