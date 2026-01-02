import streamlit as st
from services.crud_service import fetch_table, update_row, delete_row
from core.permissions import can_access

TABLE = "OUTLET_MASTER"
user = st.session_state.user

st.title("🗃️ Database GUI")

df = fetch_table(TABLE)
st.dataframe(df, use_container_width=True)

if can_access(user, TABLE, "UPDATE"):
    st.subheader("✏️ Edit Row")
    row_id = st.number_input("Row ID", step=1)
    column = st.selectbox("Column", df.columns)
    value = st.text_input("New Value")

    if st.button("Update"):
        update_row(user, TABLE, row_id, {column: value})
        st.success("Updated")

if can_access(user, TABLE, "DELETE"):
    st.subheader("🗑️ Delete Row")
    del_id = st.number_input("Delete ID", step=1)
    if st.button("Delete"):
        delete_row(user, TABLE, del_id)
        st.success("Deleted")

