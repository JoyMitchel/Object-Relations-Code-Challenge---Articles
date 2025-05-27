import sqlite3
from lib.db.connection import get_connection

with open('code-challenge/lib/db/schema.sql', 'r') as f:
    schema_sql = f.read()

conn = get_connection()
conn.executescript(schema_sql)
conn.commit()
conn.close()
