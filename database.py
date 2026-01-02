import mysql.connector
import streamlit as st
import pandas as pd
from datetime import datetime

def get_connection():
    return mysql.connector.connect(
        host=st.secrets["db"]["host"],
        user=st.secrets["db"]["user"],
        password=st.secrets["db"]["password"],
        database=st.secrets["db"]["name"],
        port=int(st.secrets["db"].get("port", 3306))
    )

def create_table(table_name, df):
    conn = get_connection()
    cur = conn.cursor()
    columns = ", ".join([f"`{col}` TEXT" for col in df.columns])
    try:
        cur.execute(f"CREATE TABLE IF NOT EXISTS `{table_name}` ({columns})")
        conn.commit()
    finally:
        conn.close()

def insert_data(table_name, df, chunk_size=5000):
    conn = get_connection()
    cur = conn.cursor()
    placeholders = ",".join(["%s"] * len(df.columns))
    sql = f"INSERT INTO `{table_name}` VALUES ({placeholders})"
    try:
        for i in range(0, len(df), chunk_size):
            chunk = df.iloc[i:i+chunk_size]
            cur.executemany(sql, chunk.values.tolist())
            conn.commit()
    finally:
        conn.close()

def fetch_tables():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SHOW TABLES")
    tables = [t[0] for t in cur.fetchall() if t[0] not in ["users","upload_logs","audit_logs"]]
    conn.close()
    return tables

def fetch_table_data(table_name):
    conn = get_connection()
    df = pd.read_sql(f"SELECT * FROM `{table_name}`", conn)
    conn.close()
    return df

def delete_table(table_name):
    conn = get_connection()
    cur = conn.cursor()
    backup_name = f"backup_{table_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    cur.execute(f"RENAME TABLE `{table_name}` TO `{backup_name}`")
    conn.commit()
    conn.close()
    return backup_name

def log_upload(file_name, table_name, rows, duplicates):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO upload_logs (file_name, table_name, rows_uploaded, duplicates_removed) VALUES (%s,%s,%s,%s)",
        (file_name, table_name, rows, duplicates)
    )
    conn.commit()
    conn.close()

def fetch_logs():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM upload_logs ORDER BY uploaded_at DESC", conn)
    conn.close()
    return df
