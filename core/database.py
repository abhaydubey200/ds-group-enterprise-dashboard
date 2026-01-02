import snowflake.connector
import streamlit as st

@st.cache_resource
def get_connection():
    return snowflake.connector.connect(
        account=st.secrets["snowflake"]["account"],
        user=st.secrets["snowflake"]["user"],
        password=st.secrets["snowflake"]["password"],
        warehouse=st.secrets["snowflake"]["warehouse"],
        database=st.secrets["snowflake"]["database"],
        schema=st.secrets["snowflake"]["schema"],
        role=st.secrets["snowflake"]["role"],
    )

def run_query(query, params=None):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(query, params or [])
        return cur.fetchall()
    finally:
        cur.close()
