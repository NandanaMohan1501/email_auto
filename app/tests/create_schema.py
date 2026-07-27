from app.db import get_cursor, SCHEMA

with get_cursor() as cur:
    cur.execute(f"CREATE SCHEMA {SCHEMA}")

print(f"✅ Schema '{SCHEMA}' created successfully.")