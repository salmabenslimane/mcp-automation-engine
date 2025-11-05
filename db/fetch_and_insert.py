import requests
import pandas as pd
from db_connection import get_connection
import io

import os
from dotenv import load_dotenv  

load_dotenv()

API_URL = os.getenv("API_URL")


def fetch_data():
    response = requests.get(API_URL)
    response.raise_for_status()
    # Convert CSV text to DataFrame
    df = pd.read_csv(io.StringIO(response.text))
    df["load_date"] = pd.Timestamp.now().normalize()
    return df



def insert_data(df):
    """Insert DataFrame into DuckDB"""
    conn = get_connection()
    conn.execute("CREATE SCHEMA IF NOT EXISTS raw;") # Ensure schema exists
    conn.register("df", df) # Register DataFrame FIRST before using it in SQL
    # Create table (only once)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS raw.bookings AS
        SELECT * FROM df LIMIT 0;
    """)
    # Clear any old data (for testing only — remove later when Airflow automates)
    conn.execute("DELETE FROM raw.bookings;")
    # Insert new data
    conn.execute("INSERT INTO raw.bookings SELECT * FROM df;")
    conn.close()

    print(f"✅ Inserted {len(df)} rows into raw.bookings!")

if __name__ == "__main__":

    df = fetch_data()
    print(f" ✅ Fetched {len(df)} rows from API.")
    insert_data(df)
    print(df.head())  # Display first few rows for verification

'''What it does:
Fetches csv data from a REST API, transforms it into a DataFrame, and loads it into a DuckDB database.'''