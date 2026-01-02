import streamlit as st
import pandas as pd
from core.database import get_connection

st.title("🗃️ DS Group Database GUI")

table = st.text_input("Enter table name")

if table:
    conn = get_connection()
    df = pd.read_sql(f"SELECT * FROM {table} LIMIT 1000", conn)

    st.dataframe(df, use_container_width=True)

    st.subheader("❌ Delete Row")
    row_id = st.number_input("Row Number", min_value=0, max_value=len(df)-1)

    if st.button("Delete"):
        st.warning("Row deletion must be handled via primary key in production")
