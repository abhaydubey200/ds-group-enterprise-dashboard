import streamlit as st
from streamlit_option_menu import option_menu
from st_aggrid import AgGrid, GridOptionsBuilder
import plotly.express as px
from utils import read_file, clean_data, export_csv, export_excel
from database import create_table, insert_data, fetch_tables, fetch_table_data, log_upload, fetch_logs, delete_table
from auth import login, is_admin

st.set_page_config(
    page_title="DS Group Enterprise Dashboard",
    page_icon="assets/ds_logo.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    login()
    st.stop()

st.sidebar.image("assets/ds_logo.png", width=160)
st.sidebar.markdown("## DS Group Dashboard")
st.sidebar.markdown(f"#### Role: **{st.session_state.get('role').capitalize()}**")

menu_items = ["Upload Data", "View Tables", "Analytics", "Logs"]
if is_admin():
    menu_items.append("Delete Table")

menu = option_menu(
    menu_title="DS Group Menu",
    options=menu_items,
    icons=["cloud-upload", "table", "bar-chart", "clock-history", "trash"],
    menu_icon="cast",
    default_index=0,
    styles={"container": {"padding": "10px"},
            "icon": {"color": "#2E7D32", "font-size": "18px"},
            "nav-link": {"font-size": "16px", "text-align": "left"},
            "nav-link-selected": {"background-color": "#2E7D32", "color": "white"}}
)

# -------- Upload Data --------
if menu == "Upload Data":
    if not is_admin():
        st.warning("Admin access required")
        st.stop()
    st.header("📤 Upload CSV / Excel / JSON Files")
    uploaded_files = st.file_uploader("Choose files", accept_multiple_files=True, type=["csv","xlsx","xls","json"])
    if uploaded_files:
        for file in uploaded_files:
            st.subheader(f"Processing file: {file.name}")
            df = read_file(file)
            if df is None:
                st.error("Unsupported file format")
                continue
            df, dup = clean_data(df)
            st.success(f"✅ {dup} duplicates removed")
            table_name = st.text_input("Table Name", value=file.name.split(".")[0])
            if st.button(f"Upload {file.name}"):
                create_table(table_name, df)
                insert_data(table_name, df)
                log_upload(file.name, table_name, len(df), dup)
                st.balloons()
                st.success(f"File `{file.name}` uploaded successfully!")

# -------- View Tables --------
elif menu == "View Tables":
    st.header("📋 View & Export Tables")
    tables = fetch_tables()
    if tables:
        table = st.selectbox("Select Table", tables)
        if table:
            df = fetch_table_data(table)
            gb = GridOptionsBuilder.from_dataframe(df)
            gb.configure_pagination(enabled=True)
            gb.configure_default_column(sortable=True, filter=True, editable=False, resizable=True)
            AgGrid(df, gridOptions=gb.build(), height=400, fit_columns_on_grid_load=True)
            st.subheader("⬇ Export Options")
            col1, col2 = st.columns(2)
            col1.download_button("Download CSV", export_csv(df), file_name=f"{table}.csv")
            col2.download_button("Download Excel", export_excel(df), file_name=f"{table}.xlsx")
    else:
        st.info("No tables available. Upload data first.")

# -------- Analytics --------
elif menu == "Analytics":
    st.header("📊 Upload Analytics")
    logs = fetch_logs()
    if not logs.empty:
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Uploads 🟢", logs.shape[0])
        col2.metric("Total Rows 📦", logs["rows_uploaded"].sum())
        col3.metric("Duplicates Removed ❌", logs["duplicates_removed"].sum())
        st.subheader("Uploads Over Time")
        fig = px.bar(logs, x="uploaded_at", y="rows_uploaded", color="table_name", text="rows_uploaded")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No upload logs to display.")

# -------- Logs --------
elif menu == "Logs":
    st.header("📜 Upload History Logs")
    logs = fetch_logs()
    if not logs.empty:
        gb = GridOptionsBuilder.from_dataframe(logs)
        gb.configure_pagination(enabled=True)
        gb.configure_default_column(sortable=True, filter=True, resizable=True)
        AgGrid(logs, gridOptions=gb.build(), height=450)
    else:
        st.info("No logs available.")

# -------- Delete Table --------
elif menu == "Delete Table" and is_admin():
    st.header("🗑️ Delete Tables (Admin Only)")
    tables = fetch_tables()
    if tables:
        table = st.selectbox("Select Table to Delete", tables)
        if st.button("Delete Permanently (Backup Created)"):
            backup_name = delete_table(table)
            st.success(f"Table `{table}` backed up as `{backup_name}` and deleted successfully!")
    else:
        st.info("No tables available to delete.")
