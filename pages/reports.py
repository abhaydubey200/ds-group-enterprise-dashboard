import streamlit as st
import pandas as pd
from core.database import get_connection

st.title("📜 Audit Logs")

conn = get_connection()
df = pd.read_sql("SELECT * FROM AUDIT_LOG ORDER BY CHANGE_TIME DESC", conn)
st.dataframe(df, use_container_width=True)
