from app.db import get_cursor, SCHEMA

with get_cursor() as cur:

    cur.execute("""
        SELECT name
        FROM sys.schemas
        WHERE name=?
    """, (SCHEMA,))

    row = cur.fetchone()

    if row:
        print(f"✅ Schema '{SCHEMA}' exists.")
    else:
        print(f"❌ Schema '{SCHEMA}' does not exist.")