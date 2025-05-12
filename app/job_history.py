
import streamlit as st
import pandas as pd
import sqlite3
from pathlib import Path

st.set_page_config(page_title="Job History", layout="wide")
st.title("Uploaded Job History")

db_path = Path(__file__).parent.parent / "database" / "jobs.db"

@st.cache_data
def load_jobs():
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM ActualJobs ORDER BY date DESC", conn)
    conn.close()
    return df

df = load_jobs()
st.dataframe(df, use_container_width=True)
