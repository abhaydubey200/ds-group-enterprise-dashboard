import streamlit as st
from core.auth import authenticate
from services.file_service import load_file
from services.schema_service import compare_schema
from services.table_creator import create_table_from_df
from services.upload_service import upload_df

MAIN_TABLE = "OUTLET_MASTER"

st.set_page_config("DS Group Database GUI", layout="wide")

# ---------------- LOGIN ----------------
if "user" not in st.session_state:
    st.title("🔐 DS Group Secure Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = authenticate(username, password)
        if user:
            st.session_state.user = user
            st.rerun()
        else:
            st.error("❌ Invalid credentials")

    st.stop()

# ---------------- UPLOAD ----------------
st.sidebar.success(f"Logged in as {st.session_state.user['role']}")
st.title("🗃️ DS Group Database GUI")

file = st.file_uploader("Upload CSV / Excel / JSON")

if file:
    df = load_file(file)
    st.subheader("📄 Preview")
    st.dataframe(df.head())

    schema_result = compare_schema(df, MAIN_TABLE)

    if schema_result["match"]:
        st.success("✅ Schema matched with main table")
        if st.button("Upload to Main Table"):
            upload_df(df, MAIN_TABLE)
            st.success("🎉 Data uploaded successfully")

    else:
        st.error("❌ Schema does NOT match main table")

        st.warning(f"Missing Columns: {schema_result['missing']}")
        st.warning(f"Extra Columns: {schema_result['extra']}")

        st.markdown("### ❓ Do you want to create another table?")
        new_table = st.text_input("Enter new table name")

        if st.button("Yes, Create & Upload"):
            create_table_from_df(df, new_table)
            upload_df(df, new_table)
            st.success(f"✅ Table `{new_table}` created & data uploaded")
