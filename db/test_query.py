# !! data added here for testing will be deleted later with Airflow tasks !!

from db_connection import get_connection
import pandas as pd

def insert_sample_data():
    conn = get_connection()
    # Ensure the schema and table exist
    conn.execute("CREATE SCHEMA IF NOT EXISTS raw;") # Ensure schema exists
    conn.execute("DELETE FROM raw.bookings;") # Clean up before inserting test data
    conn.execute("""
        INSERT INTO raw.bookings (
            Booking_Date,
            Flight_ID,
            Passenger_ID,
            Passenger_Name,
            Email,
            Gender,
            Ticket_Class,
            Quantity,
            Unit_Price,
            Revenue
        ) VALUES
        ('2025-11-02 10:00:00', 'AF123', 'PAX001', 'Alice Martin', 'alice@email.com', 'F', 'Economy', 2, 350.00, 700.00),
        ('2025-11-03 15:30:00', 'AF456', 'PAX002', 'John Doe', 'john@email.com', 'M', 'Business', 1, 900.00, 900.00);
    """)
    conn.close()
    print("Inserted sample data into raw.bookings!")

def test_on_sql_query():
    conn = get_connection()

    # Read all records
    results = conn.execute("SELECT * FROM raw.bookings;").fetchdf()
    print("\nAll Records:")
    print(results)

    # Example aggregation query
    results2 = conn.execute("""
        SELECT Ticket_Class, SUM(Revenue) AS total_revenue
        FROM raw.bookings
        GROUP BY Ticket_Class;
    """).fetchdf()
    print("\n Revenue by Ticket Class:")
    print(results2)

    conn.close()

if __name__ == "__main__":
    insert_sample_data()
    test_on_sql_query()

'''What it does:
Inserts sample data into the bookings table.
Runs two test SQL queries to verify data insertion and aggregation functionality.'''

