import streamlit as st
from services.bulk_service import bulk_delete

st.title("🔥 Bulk Delete")

condition = st.text_input("SQL Condition (example: CITY='Delhi')")
if st.button("Execute Bulk Delete"):
    bulk_delete(st.session_state.user, "OUTLET_MASTER", condition)
    st.success("Bulk delete completed")
