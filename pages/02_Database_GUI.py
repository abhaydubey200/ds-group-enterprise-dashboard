import streamlit as st
import pandas as pd
from core.database import get_connection
from core.permissions import has_permission
from services.crud_service import insert_row, update_row, delete_rows

user = st.session_state.user
role = user["role"]

st.title("🗃️ DS Group Database GUI")

table = st.text_input("Table name")

if not table:
    st.stop()

conn = get_connection()
df = pd.read_sql(f"SELECT * FROM {table} LIMIT 500", conn)
st.dataframe(df, use_container_width=True)

pk_col = df.columns[0]  # assumed primary key

# ---------- INSERT ----------
if has_permission(role, "insert"):
    st.subheader("➕ Insert Row")
    with st.form("insert"):
        row = {col: st.text_input(col) for col in df.columns}
        if st.form_submit_button("Insert"):
            insert_row(table, row, user["username"])
            st.success("Inserted")
            st.rerun()

# ---------- UPDATE ----------
if has_permission(role, "update"):
    st.subheader("✏️ Update Row")
    pk = st.selectbox("Select Row", df[pk_col])
    selected = df[df[pk_col] == pk].iloc[0]

    with st.form("update"):
        updated = {
            col: st.text_input(col, str(selected[col]))
            for col in df.columns
        }
        if st.form_submit_button("Update"):
            update_row(table, updated, pk_col, pk, user["username"])
            st.success("Updated")
            st.rerun()

# ---------- BULK DELETE ----------
if has_permission(role, "delete"):
    st.subheader("❌ Bulk Delete")
    ids = st.multiselect("Select rows", df[pk_col])
    if st.button("Delete Selected"):
        delete_rows(table, pk_col, ids, user["username"])
        st.success("Deleted")
        st.rerun()
