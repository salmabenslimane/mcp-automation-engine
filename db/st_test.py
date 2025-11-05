import streamlit as st
import duckdb
import pandas as pd
from datetime import date

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="✈️ Flight Sales Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------
# CONNECT TO DUCKDB
# -------------------------------
DB_PATH = "../db/raw_data.duckdb"

@st.cache_data
def load_data(query):
    with duckdb.connect(DB_PATH, read_only=True) as conn:
        return conn.execute(query).fetchdf()

# -------------------------------
# HEADER
# -------------------------------
st.title("✈️ Flight Sales Analytics Dashboard")
st.markdown(f"📅 Last updated: `{date.today()}`")

# -------------------------------
# LOAD KPI SUMMARY
# -------------------------------
summary_df = load_data("SELECT * FROM processed.bookings_summary ORDER BY load_date DESC LIMIT 1;")

if summary_df.empty:
    st.warning("⚠️ No data found in processed.bookings_summary — please run your ETL pipeline first.")
else:
    total_revenue = summary_df['total_revenue'].iloc[0]
    total_bookings = summary_df['total_bookings'].iloc[0]
    avg_price = summary_df['avg_ticket_price'].iloc[0]
    total_passengers = summary_df['total_passengers'].iloc[0]

    # KPIs in columns
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💰 Total Revenue", f"${total_revenue:,.0f}")
    col2.metric("🧾 Total Bookings", f"{total_bookings:,}")
    col3.metric("🎟️ Avg Ticket Price", f"${avg_price:,.2f}")
    col4.metric("👥 Total Passengers", f"{total_passengers:,}")

# -------------------------------
# DETAILED VISUALIZATIONS
# -------------------------------
st.divider()
st.subheader("📊 Detailed Metrics")

# Revenue by Ticket Class
st.markdown("#### 💼 Revenue by Ticket Class")
revenue_by_class = load_data("SELECT * FROM processed.revenue_by_class;")
if not revenue_by_class.empty:
    st.bar_chart(revenue_by_class.set_index("Ticket_Class"))
else:
    st.info("No revenue_by_class data available yet.")

# Top Routes
st.markdown("#### 🌍 Top 10 Routes by Revenue")
top_routes = load_data("SELECT * FROM processed.top_routes;")
if not top_routes.empty:
    st.dataframe(top_routes)
else:
    st.info("No top_routes data available yet.")

# Top Countries
st.markdown("#### 🗺️ Top Arrival Countries by Revenue")
top_countries = load_data("SELECT * FROM processed.top_countries;")
if not top_countries.empty:
    st.bar_chart(top_countries.set_index("Arrival_Country"))
else:
    st.info("No top_countries data available yet.")

# Daily Revenue Trend
st.markdown("#### 📈 Daily Revenue Trend")
daily_revenue = load_data("SELECT * FROM processed.daily_revenue ORDER BY Flight_Date;")
if not daily_revenue.empty:
    st.line_chart(
        daily_revenue.set_index("Flight_Date")[["Revenue", "Revenue_Growth_Pct"]]
    )
else:
    st.info("No daily_revenue data available yet.")

st.divider()
st.caption("Built with ❤️ using Streamlit + DuckDB | Flight Intelligence Automation Agent")

import subprocess
import streamlit as st

st.header("💡 AI-Generated Insights")

if st.button("Generate Insights"):
    with st.spinner("Generating insights..."):
        result = subprocess.check_output(
            ["python", "../agents/insights_agent.py"], text=True
        )
        st.text(result)
