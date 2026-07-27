from contextlib import contextmanager
import pyodbc

from app.config.settings import settings

SCHEMA = settings.sql_schema


def get_connection():
    return pyodbc.connect(
        f"DRIVER={{{settings.sql_driver}}};"
        f"SERVER={settings.sql_server};"
        f"DATABASE={settings.sql_database};"
        f"UID={settings.sql_user};"
        f"PWD={settings.sql_password};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
    )


@contextmanager
def get_cursor():

    conn = get_connection()
    cursor = conn.cursor()

    try:
        yield cursor
        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        cursor.close()
        conn.close()