from db_connection import get_connection

def create_schema():

    conn = get_connection()
    conn.execute("CREATE SCHEMA IF NOT EXISTS raw;")
    conn.execute("""
    CREATE TABLE IF NOT EXISTS raw.bookings (
        Flight_Date DATE,
        Booking_Date DATE,
        Booking_ID VARCHAR,
        Flight_ID VARCHAR,
        Departure_Airport VARCHAR,
        Arrival_Airport VARCHAR,
        Departure_Country VARCHAR,
        Arrival_Country VARCHAR,
        Passenger_ID VARCHAR,
        Passenger_Name VARCHAR,
        Email VARCHAR,
        Gender VARCHAR,
        Ticket_Class VARCHAR,
        Quantity INTEGER,
        Unit_Price DOUBLE,
        Revenue DOUBLE,
        load_date DATE
    );

    """)
    conn.close()
    print("✅ Schema created successfully!")

if __name__ == "__main__":
    create_schema()


'''What it does:

Creates the main table bookings if it doesn’t already exist.

Defines all the columns you’ll use later for analysis.'''