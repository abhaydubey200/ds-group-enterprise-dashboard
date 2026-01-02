import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder
import pandas as pd
import numpy as np
import mysql.connector
from utils import clean_file, remove_duplicates, export_file
from auth import login_user, is_authenticated
from database import init_db, insert_data, fetch_data
from streamlit_option_menu import option_menu
import plotly.express as px

# -------------------- APP CONFIG --------------------
st.set_page_config(
    page_title="DS Group Enterprise Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .stApp { background-color: #ffffff; color: black; }
    .css-1d391kg { color: black; }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------- DS GROUP LOGO --------------------
st.sidebar.image("assets/ds_logo.png", width=150)

# -------------------- AUTHENTICATION --------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        if login_user(username, password):
            st.session_state.authenticated = True
            st.experimental_rerun()
        else:
            st.sidebar.error("Invalid credentials!")
else:
    # -------------------- SIDEBAR MENU --------------------
    with st.sidebar:
        selected = option_menu(
            menu_title="DS Group Dashboard",
            options=["Home", "Upload Data", "View Data", "Analytics", "Logs"],
            icons=["house", "cloud-upload", "table", "bar-chart-line", "file-earmark-text"],
            menu_icon="grid",
            default_index=0,
        )

    # -------------------- PAGE: HOME --------------------
    if selected == "Home":
        st.title("📊 DS Group Enterprise Dashboard")
        st.markdown("Welcome to the DS Group interactive admin dashboard.")
        st.markdown("Use the menu to upload, view, and analyze data.")

    # -------------------- PAGE: UPLOAD DATA --------------------
    elif selected == "Upload Data":
        st.header("📁 Upload CSV / Excel / JSON")
        uploaded_file = st.file_uploader(
            "Choose a file", type=["csv", "xlsx", "json"]
        )
        if uploaded_file is not None:
            df = clean_file(uploaded_file)
            df = remove_duplicates(df)
            st.success("✅ File cleaned and duplicates removed!")
            st.dataframe(df.head())

            if st.button("Save to Database"):
                insert_data(df)
                st.success("💾 Data saved to MySQL database!")

    # -------------------- PAGE: VIEW DATA --------------------
    elif selected == "View Data":
        st.header("🗃 View Database Tables")
        data = fetch_data()
        if not data.empty:
            gb = GridOptionsBuilder.from_dataframe(data)
            gb.configure_pagination()
            gb.configure_side_bar()
            grid_options = gb.build()
            AgGrid(data, gridOptions=grid_options)
        else:
            st.info("No data available in the database.")

    # -------------------- PAGE: ANALYTICS --------------------
    elif selected == "Analytics":
        st.header("📈 Analytics")
        data = fetch_data()
        if not data.empty:
            numeric_cols = data.select_dtypes(include=np.number).columns.tolist()
            if numeric_cols:
                selected_col = st.selectbox("Select column for visualization", numeric_cols)
                fig = px.histogram(data, x=selected_col)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("No numeric columns found for visualization.")
        else:
            st.info("No data to visualize.")

    # -------------------- PAGE: LOGS --------------------
    elif selected == "Logs":
        st.header("📝 Upload & System Logs")
        logs_df = fetch_data(table_name="upload_logs")
        if not logs_df.empty:
            st.dataframe(logs_df)
        else:
            st.info("No logs available yet.")
