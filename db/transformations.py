"""
It’s the bridge between:

the data engineering layer (ETL) and
the AI + analytics layer (insights_agent & dashboard).

-------------------
Transforms raw flight sales data from DuckDB into summarized business KPIs.

✅ Generates:
    - Total Revenue
    - Total Bookings
    - Average Ticket Price
    - Total Passengers
    - Revenue by Ticket Class
    - Top Routes
    - Top Arrival Countries
    - Daily Revenue Growth (%)

Outputs results into:
    processed.bookings_summary (aggregated daily KPIs)
"""

import duckdb
from db_connection import get_connection
import pandas as pd


def transform_data():
    print("🚀 Starting data transformation process...")

    conn = get_connection()

    # Create processed schema if it doesn't exist
    conn.execute("CREATE SCHEMA IF NOT EXISTS processed;")

    # Read all raw data
    df_raw = conn.execute("SELECT * FROM raw.bookings;").fetchdf()

    if df_raw.empty:
        print("⚠️ No data found in raw.bookings — skipping transformation.")
        conn.close()
        return

    # --- Compute KPIs ---
    total_revenue = float(df_raw["Revenue"].sum())
    total_bookings = int(df_raw["Booking_ID"].nunique())
    avg_ticket_price = float(df_raw["Unit_Price"].mean())
    total_passengers = int(df_raw["Quantity"].sum())

    # Grouped KPIs
    revenue_by_class = (
        df_raw.groupby("Ticket_Class")["Revenue"].sum().reset_index()
    )
    top_routes = (
        df_raw.groupby(["Departure_Airport", "Arrival_Airport"])["Revenue"]
        .sum()
        .reset_index()
        .sort_values("Revenue", ascending=False)
        .head(10)
    )
    top_countries = (
        df_raw.groupby("Arrival_Country")["Revenue"]
        .sum()
        .reset_index()
        .sort_values("Revenue", ascending=False)
        .head(10)
    )

    # Daily revenue trend for growth calculation
    daily_revenue = (
        df_raw.groupby("Flight_Date")["Revenue"].sum().reset_index().sort_values("Flight_Date")
    )
    daily_revenue["Revenue_Growth_Pct"] = daily_revenue["Revenue"].pct_change() * 100

    # --- Store summary in processed schema ---
    conn.execute("""
        CREATE TABLE IF NOT EXISTS processed.bookings_summary (
            load_date DATE,
            total_revenue DOUBLE,
            total_bookings INTEGER,
            avg_ticket_price DOUBLE,
            total_passengers INTEGER
        );
    """)

    conn.execute("DELETE FROM processed.bookings_summary WHERE load_date = CURRENT_DATE;")

    conn.execute(
        """
        INSERT INTO processed.bookings_summary
        SELECT CURRENT_DATE,
               ?, ?, ?, ?;
        """,
        [total_revenue, total_bookings, avg_ticket_price, total_passengers],
    )

    print("✅ Stored main KPIs in processed.bookings_summary.")

    # --- Optional: store detailed breakdowns (for dashboard use) ---
    conn.execute("""
        CREATE TABLE IF NOT EXISTS processed.revenue_by_class AS SELECT * FROM revenue_by_class LIMIT 0;
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS processed.top_routes AS SELECT * FROM top_routes LIMIT 0;
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS processed.top_countries AS SELECT * FROM top_countries LIMIT 0;
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS processed.daily_revenue AS SELECT * FROM daily_revenue LIMIT 0;
    """)

    # Register DataFrames
    conn.register("revenue_by_class", revenue_by_class)
    conn.register("top_routes", top_routes)
    conn.register("top_countries", top_countries)
    conn.register("daily_revenue", daily_revenue)

    # Clear and reload processed tables
    conn.execute("DELETE FROM processed.revenue_by_class;")
    conn.execute("DELETE FROM processed.top_routes;")
    conn.execute("DELETE FROM processed.top_countries;")
    conn.execute("DELETE FROM processed.daily_revenue;")

    conn.execute("INSERT INTO processed.revenue_by_class SELECT * FROM revenue_by_class;")
    conn.execute("INSERT INTO processed.top_routes SELECT * FROM top_routes;")
    conn.execute("INSERT INTO processed.top_countries SELECT * FROM top_countries;")
    conn.execute("INSERT INTO processed.daily_revenue SELECT * FROM daily_revenue;")

    conn.close()
    print("✅ All KPI tables created and populated successfully!")


if __name__ == "__main__":
    transform_data()
'''What it does:    
Transforms raw booking data into key performance indicators (KPIs) and stores them in a processed schema.   '''