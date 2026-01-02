# app.py
import streamlit as st
import pandas as pd
import mysql.connector
from mysql.connector import Error

st.set_page_config(
    page_title="DS Group Enterprise Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 DS Group Enterprise Dashboard")
st.markdown("Welcome to the DS Group interactive analytics dashboard.")

# --- Database Connection ---
def create_connection():
    try:
        conn = mysql.connector.connect(
            host=st.secrets["db"]["host"],
            user=st.secrets["db"]["user"],
            password=st.secrets["db"]["password"],
            database=st.secrets["db"]["name"],
            port=st.secrets["db"]["port"]
        )
        return conn
    except Error as e:
        st.error(f"Database connection error: {e}")
        return None

# --- Create Table if Not Exists ---
def create_main_table():
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        create_query = """
        CREATE TABLE IF NOT EXISTS main_dashboard (
            Region_Name VARCHAR(255),
            Region_ID VARCHAR(50),
            ASM_Area VARCHAR(255),
            ASM_Area_Id VARCHAR(50),
            Stockist_Id VARCHAR(50),
            Stockist_Code VARCHAR(50),
            Stockist_Name VARCHAR(255),
            Stockist_Created_Date DATE,
            Outlet_Type VARCHAR(255),
            Outlet_Type_Id VARCHAR(50),
            Stockiest_Town VARCHAR(255),
            Stockiest_District VARCHAR(255),
            Stockist_State VARCHAR(255),
            Stockist_Business_Type VARCHAR(255),
            Stockiest_Type VARCHAR(255),
            Pin_Code VARCHAR(20),
            Stockiest_PAN_No VARCHAR(50),
            Stockiest_GSTIN_No VARCHAR(50),
            Area_ID VARCHAR(50),
            Retailer_Id VARCHAR(50),
            Retailer_Name VARCHAR(255),
            Last_Visited DATE,
            Retailer_Active_Inactive VARCHAR(50),
            Retailer_Address VARCHAR(255),
            Latitude VARCHAR(50),
            Longitude VARCHAR(50),
            Retailer_Town VARCHAR(255),
            Retailer_District VARCHAR(255),
            Retailer_State VARCHAR(255),
            Retailer_Pin_Code VARCHAR(20),
            Retailer_PAN_No VARCHAR(50),
            Retailer_GSTIN_No VARCHAR(50),
            Owner_Name VARCHAR(255),
            Outlet_Contact_Number VARCHAR(50),
            Owner_Contact_Number VARCHAR(50),
            Outlet_Category_ID VARCHAR(50),
            Outlet_Category VARCHAR(255),
            Beat_ID VARCHAR(50),
            Beat_Name VARCHAR(255),
            Beat_Status VARCHAR(50),
            User_id VARCHAR(50),
            Position_Code VARCHAR(50),
            User_Name VARCHAR(255),
            User_Emplyoee_ID VARCHAR(50),
            Designation VARCHAR(255),
            Reporting_To VARCHAR(255),
            Retailer_Creation_Date DATE,
            Created_UserId VARCHAR(50),
            Created_User_Name VARCHAR(255),
            Emp_ID VARCHAR(50),
            Reporting_Manager_Name VARCHAR(255),
            Reprting_Manager_Of_Reporting_manger VARCHAR(255),
            KYC_Approval_Status VARCHAR(50),
            Required VARCHAR(50),
            KYC_Form VARCHAR(255),
            Correct_Outlet_Name VARCHAR(255),
            Proprietor_Partner_Name_Owner_Name VARCHAR(255),
            Town VARCHAR(255),
            GST_Registration_Status VARCHAR(50),
            GST_Number VARCHAR(50),
            GST_invoice_Settlements VARCHAR(255),
            Upload_GST_Certificate VARCHAR(255),
            PAN_Card_Number VARCHAR(50),
            Upload_Pan_card_image VARCHAR(255),
            Name_of_Payee_of_Bank_Ac VARCHAR(255),
            Bank_Name VARCHAR(255),
            Branch VARCHAR(255),
            Account_Number VARCHAR(50),
            IFSC_Code VARCHAR(50),
            Upload_Cancelled_Cheque VARCHAR(255),
            Upload_GST_Form VARCHAR(255),
            Hi_Po_Outlet VARCHAR(50),
            Outlet_Status VARCHAR(50),
            Wholesale_Class VARCHAR(50),
            ASM_User_Id VARCHAR(50),
            ASM_Position_Code VARCHAR(50),
            ASM_Designation VARCHAR(255),
            RSM_User_Id VARCHAR(50),
            RSM_Position_Code VARCHAR(50),
            RSM_Designation VARCHAR(255),
            Inactive_Outlet_Date DATE,
            Outlet_Status_1 VARCHAR(50),
            Wholesale_Addition_Source VARCHAR(255),
            Wholesaler_Codes_given_on_maps VARCHAR(255)
        );
        """
        cursor.execute(create_query)
        conn.commit()
        cursor.close()
        conn.close()

# --- Upload Data ---
def upload_data(file):
    if file is not None:
        try:
            df = pd.read_excel(file) if file.name.endswith(".xlsx") else pd.read_csv(file)
            conn = create_connection()
            if conn:
                cursor = conn.cursor()
                for i, row in df.iterrows():
                    # Build insert query dynamically
                    placeholders = ", ".join(["%s"] * len(df.columns))
                    columns = ", ".join([f"`{c}`" for c in df.columns])
                    sql = f"INSERT INTO main_dashboard ({columns}) VALUES ({placeholders})"
                    cursor.execute(sql, tuple(row))
                conn.commit()
                cursor.close()
                conn.close()
                st.success("Data uploaded successfully!")
        except Exception as e:
            st.error(f"Error uploading data: {e}")

# --- Main Table Creation ---
create_main_table()

# --- Sidebar ---
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["View Data", "Upload Data"])

# --- Upload Page ---
if page == "Upload Data":
    st.subheader("Upload Excel/CSV to Dashboard")
    uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx"])
    if uploaded_file:
        upload_data(uploaded_file)

# --- View Page ---
elif page == "View Data":
    st.subheader("View Main Dashboard Data")
    conn = create_connection()
    if conn:
        df = pd.read_sql("SELECT * FROM main_dashboard LIMIT 500", conn)
        conn.close()
        st.dataframe(df)
        if not df.empty:
            st.markdown("### Summary Metrics")
            st.metric("Total Rows", len(df))
            numeric_cols = df.select_dtypes(include='number').columns
            for col in numeric_cols:
                st.metric(f"Sum of {col}", df[col].sum())
    else:
        st.info("No data available.")
