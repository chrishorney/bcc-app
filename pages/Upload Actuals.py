
import streamlit as st
import pandas as pd
import sqlite3
from pathlib import Path

st.set_page_config(page_title="Upload Actual Job Data", layout="centered")
st.title("Upload Past Job Actuals (QuickBooks Export)")

db_path = Path(__file__).parent.parent / "database" / "jobs.db"

# Ensure the table exists
def create_actuals_table():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ActualJobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            builder TEXT,
            job_name TEXT,
            date TEXT,
            concrete_yards REAL,
            rebar_feet REAL,
            dirt_yards REAL,
            labor_hours REAL,
            equipment_hours REAL,
            total_actual_cost REAL
        )
    """)
    conn.commit()
    conn.close()

create_actuals_table()

uploaded_file = st.file_uploader("Upload a QuickBooks job export (.csv)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("Preview of Uploaded Data:")
    st.dataframe(df)

    if st.button("Save to Database"):
        conn = sqlite3.connect(db_path)
        df.to_sql("ActualJobs", conn, if_exists="append", index=False)
        conn.commit()
        conn.close()
        st.success("Uploaded data saved to database.")
