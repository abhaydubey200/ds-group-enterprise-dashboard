import streamlit as st
from services.crud_service import fetch_table, delete_rows, insert_row, update_row

def table_gui(table_name):
    st.subheader(f"📊 Table: {table_name}")

    df = fetch_table(table_name)

    # 🔍 Search
    search = st.text_input("🔍 Search")
    if search:
        df = df[df.astype(str).apply(lambda r: r.str.contains(search, case=False).any(), axis=1)]

    edited_df = st.data_editor(
        df,
        use_container_width=True,
        num_rows="dynamic",
        key=f"editor_{table_name}"
    )

    col1, col2, col3 = st.columns(3)

    # 💾 UPDATE
    if col1.button("💾 Save Changes"):
        for i in range(len(df)):
            if not df.iloc[i].equals(edited_df.iloc[i]):
                condition = " AND ".join(
                    [f'"{c}" = \'{df.iloc[i][c]}\'' for c in df.columns[:1]]
                )
                update_row(table_name, edited_df.iloc[i].to_dict(), condition)
        st.success("✅ Changes saved")

    # ➕ INSERT
    if col2.button("➕ Add Row"):
        insert_row(table_name, {c: "" for c in df.columns})
        st.success("Row added")

    # ❌ DELETE
    if col3.button("❌ Delete Selected"):
        selected = st.multiselect("Select rows by index", df.index)
        for i in selected:
            condition = " AND ".join(
                [f'"{c}" = \'{df.iloc[i][c]}\'' for c in df.columns[:1]]
            )
            delete_rows(table_name, condition)
        st.success("Rows deleted")
