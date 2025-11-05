import duckdb
import os

def get_connection():
    db_path = os.path.join(os.path.dirname(__file__), "raw_data.duckdb")
    conn = duckdb.connect(database=db_path)
    return conn

'''What it does:

Creates or connects to a local raw_data.duckdb file.

Returns a connection object you can use to run SQL commands.'''