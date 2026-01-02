import streamlit as st
import pandas as pd
from services.crud_service import (
    fetch_table, insert_row, update_row, delete_row
)

st.set_page_config(page_title="Database GUI", layout="wide")

if "user" not in st.session_state:
    st.error("Unauthorized access")
    st.stop()

st.title("🗄️ DS Group Database GUI")

table_name = st.text_input("Enter Table Name")

if table_name:
    try:
        df = fetch_table(table_name)
        st.subheader("📊 Table Data")

        edited_df = st.data_editor(
            df,
            num_rows="dynamic",
            use_container_width=True,
            key="editor"
        )

        # ---------------- SAVE CHANGES ----------------
        if st.button("💾 Save Changes"):
            changed = edited_df.compare(df)

            for idx in changed.index:
                where = " AND ".join(
                    [f'"{col}" = %s' for col in df.columns]
                )
                update_row(
                    table_name,
                    edited_df.loc[idx].to_dict(),
                    where_clause=where
                )

            st.success("✅ Changes saved to Snowflake")

        # ---------------- DELETE ----------------
        st.subheader("🗑️ Delete Row")
        delete_index = st.number_input(
            "Row index to delete", min_value=0, max_value=len(df)-1, step=1
        )

        if st.button("Delete Selected Row"):
            row = df.iloc[delete_index]
            where = " AND ".join([f'"{c}" = %s' for c in df.columns])
            delete_row(table_name, where)
            st.success("🗑️ Row deleted")

        # ---------------- INSERT ----------------
        st.subheader("➕ Add New Row")
        new_row = {}
        for col in df.columns:
            new_row[col] = st.text_input(f"{col}")

        if st.button("Insert Row"):
            insert_row(table_name, new_row)
            st.success("➕ Row inserted")

    except Exception as e:
        st.error(f"❌ Error loading table: {e}")
