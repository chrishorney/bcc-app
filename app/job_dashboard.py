
import streamlit as st
import pandas as pd
import sqlite3
from pathlib import Path

st.set_page_config(page_title="Job Insights Dashboard", layout="wide")
st.title("Job Insights from Actuals")

db_path = Path(__file__).parent.parent / "database" / "jobs.db"

@st.cache_data
def load_data():
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM ActualJobs", conn)
    conn.close()
    return df

df = load_data()

if df.empty:
    st.info("No job data found. Upload jobs to see insights.")
else:
    total_jobs = len(df)
    avg_cost = df["total_actual_cost"].mean()
    top_builders = df["builder"].value_counts().head(5)

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Jobs", total_jobs)
    col2.metric("Avg Job Cost", f"${avg_cost:,.0f}")
    col3.metric("Top Builder", top_builders.index[0] if not top_builders.empty else "N/A")

    st.subheader("Top 5 Builders by Job Count")
    st.bar_chart(top_builders)
