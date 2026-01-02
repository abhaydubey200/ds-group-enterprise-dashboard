import mysql.connector
import pandas as pd
from utils import get_db_config

def init_db():
    cfg = get_db_config()
    conn = mysql.connector.connect(**cfg)
    cursor = conn.cursor()
    # Create main table if not exists
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ds_data (
        id INT AUTO_INCREMENT PRIMARY KEY,
        data JSON,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    cursor.close()
    conn.close()

def insert_data(df):
    cfg = get_db_config()
    conn = mysql.connector.connect(**cfg)
    cursor = conn.cursor()
    for _, row in df.iterrows():
        cursor.execute("INSERT INTO ds_data (data) VALUES (%s)", (row.to_json(),))
    conn.commit()
    cursor.close()
    conn.close()

def fetch_data(table_name="ds_data"):
    cfg = get_db_config()
    conn = mysql.connector.connect(**cfg)
    query = f"SELECT * FROM {table_name}"
    try:
        df = pd.read_sql(query, conn)
    except:
        df = pd.DataFrame()
    conn.close()
    return df
