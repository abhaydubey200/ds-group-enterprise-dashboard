import streamlit as st
from services.duplicate_service import find_duplicates, merge_duplicates

st.title("🔁 Duplicate Manager")

col = st.text_input("Duplicate Check Column")
if col:
    dups = find_duplicates("OUTLET_MASTER", col)
    st.dataframe(dups)

    val = st.text_input("Value to merge")
    if st.button("Merge"):
        merge_duplicates(st.session_state.user, "OUTLET_MASTER", col, val)
        st.success("Merged")

