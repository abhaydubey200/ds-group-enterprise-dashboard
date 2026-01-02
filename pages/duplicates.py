import streamlit as st
import pandas as pd
from services.duplicate_service import find_duplicates, merge_duplicates

st.title("🔁 Duplicate Detection")

uploaded = st.file_uploader("Upload file")

if uploaded:
    df = pd.read_csv(uploaded)
    cols = st.multiselect("Duplicate 기준 columns", df.columns)

    if cols:
        dup = find_duplicates(df, cols)
        st.dataframe(dup)

        if st.button("Merge & Remove Duplicates"):
            clean = merge_duplicates(df, cols)
            st.success("Merged")
            st.dataframe(clean)
