import sqlite3
import pandas as pd
from pathlib import Path

# Paths to CSV files
db_path = Path(__file__).parent / "jobs.db"
materials_csv = Path(__file__).parent / "materials.csv"
labor_csv = Path(__file__).parent / "labor_rates.csv"
equipment_csv = Path(__file__).parent / "equipment_rates.csv"
builders_csv = Path(__file__).parent / "builders.csv"

# Connect to SQLite DB
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS Materials (
    id INTEGER PRIMARY KEY,
    material_name TEXT,
    unit TEXT,
    price_per_unit REAL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS LaborRates (
    id INTEGER PRIMARY KEY,
    labor_type TEXT,
    hourly_rate REAL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS EquipmentRates (
    id INTEGER PRIMARY KEY,
    equipment_name TEXT,
    hourly_rate REAL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Builders (
    id INTEGER PRIMARY KEY,
    builder_name TEXT,
    discount_percent REAL
)
""")

# Load and insert data from CSVs
def load_csv_to_db(csv_path, table_name):
    df = pd.read_csv(csv_path)
    df.to_sql(table_name, conn, if_exists='replace', index=False)

load_csv_to_db(materials_csv, "Materials")
load_csv_to_db(labor_csv, "LaborRates")
load_csv_to_db(equipment_csv, "EquipmentRates")
load_csv_to_db(builders_csv, "Builders")

conn.commit()
conn.close()
print("Database setup complete.")
