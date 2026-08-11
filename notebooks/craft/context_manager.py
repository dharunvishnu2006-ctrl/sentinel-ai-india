import sqlite3
from contextlib import contextmanager


@contextmanager
def db_connection(path="test.db"):
    conn = sqlite3.connect(path)
    try:
        yield conn
    finally:
        conn.close()
        print("Connection closed.")


try:
    with db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM nonexistent_table")
except sqlite3.OperationalError as e:
    print("Query failed (expected):", e)
