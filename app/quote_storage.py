
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "database" / "jobs.db"

def create_quotes_table():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Quotes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                builder TEXT,
                job_name TEXT,
                date TEXT,
                job_details TEXT,
                quote_breakdown TEXT,
                total_price REAL
            )
        """)
        conn.commit()

def save_quote(builder, job_name, date, job_details, quote_breakdown, total_price):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Quotes (builder, job_name, date, job_details, quote_breakdown, total_price)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (builder, job_name, date, job_details, quote_breakdown, total_price))
        conn.commit()

def get_all_quotes():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, builder, job_name, date, total_price FROM Quotes ORDER BY date DESC")
        return cursor.fetchall()

def delete_quote(quote_id):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Quotes WHERE id = ?", (quote_id,))
        conn.commit()
