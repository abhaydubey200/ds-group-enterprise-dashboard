# app.py
import streamlit as st
import pandas as pd
import mysql.connector
from mysql.connector import Error

st.set_page_config(
    page_title="DS Group Enterprise Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 DS Group Enterprise Dashboard")
st.markdown("Welcome to the DS Group interactive analytics dashboard.")

# --- Database Connection ---
def create_connection():
    try:
        connection = mysql.connector.connect(
            host=st.secrets["db"]["host"],
            user=st.secrets["db"]["user"],
            password=st.secrets["db"]["password"],
            database=st.secrets["db"]["name"],
            port=st.secrets["db"]["port"]
        )
        return connection
    except Error as e:
        st.error(f"Error connecting to database: {e}")
        return None

# --- Fetch Data ---
def fetch_data(query):
    conn = create_connection()
    if conn:
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    else:
        return pd.DataFrame()  # empty df if connection fails

# --- Sidebar Filters ---
st.sidebar.header("Filters")
table_option = st.sidebar.selectbox(
    "Select Table to View",
    ("Sales Data", "Products", "Customers")
)

# --- Load Data Based on Selection ---
if table_option == "Sales Data":
    query = "SELECT * FROM sales LIMIT 100;"  # adjust your table name
    df = fetch_data(query)
    st.subheader("📈 Sales Data")
elif table_option == "Products":
    query = "SELECT * FROM products LIMIT 100;"  # adjust your table name
    df = fetch_data(query)
    st.subheader("📦 Products Data")
else:
    query = "SELECT * FROM customers LIMIT 100;"  # adjust your table name
    df = fetch_data(query)
    st.subheader("👤 Customers Data")

# --- Display Data ---
if not df.empty:
    st.dataframe(df)  # Streamlit native table
else:
    st.info("No data found.")

# --- Summary Metrics ---
st.markdown("---")
st.subheader("📊 Summary Metrics")

if not df.empty:
    st.metric("Total Rows", len(df))
    numeric_cols = df.select_dtypes(include='number').columns
    for col in numeric_cols:
        st.metric(f"Sum of {col}", df[col].sum())
else:
    st.info("No numeric metrics to display.")

# --- Optional Charts ---
st.subheader("📉 Charts")

if not df.empty and "Sales" in df.columns:
    st.bar_chart(df[["Sales"]])
elif not df.empty and "Revenue" in df.columns:
    st.line_chart(df[["Revenue"]])
