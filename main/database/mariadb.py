#|==============================================================|#
# Made by IntSPstudio
# Thank you for using this plugin!
# ID: 980001023
#|==============================================================|#

#SETTINGS
from config import DATABASES

#BASIC CONNECTION
def get_conn():
    try:
        import mariadb
    except ImportError as exc:
        raise RuntimeError("MariaDB error") from exc

    settings = DATABASES["mariadb"]
    conn = mariadb.connect(
        host=settings["host"],
        user=settings["user"],
        password=settings["password"],
        database=settings["database"],
    )
    return conn