import streamlit as st

from core.auth import authenticate
from services.file_service import load_file
from services.schema_service import compare_schema
from services.table_creator import create_table_from_df
from services.upload_service import upload_df

MAIN_TABLE = "OUTLET_MASTER"

st.set_page_config(
    page_title="DS Group Database GUI",
    layout="wide"
)

# =========================================================
# LOGIN
# =========================================================
if "user" not in st.session_state:
    st.title("🔐 DS Group Secure Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    login_clicked = st.button("Login")

    if login_clicked:
        user = authenticate(username, password)
        if user:
            st.session_state.user = user
            st.rerun()
        else:
            st.error("❌ Invalid username or password")

    st.stop()

# =========================================================
# MAIN APP
# =========================================================
st.sidebar.success(
    f"👤 Logged in as: {st.session_state.user.get('role', 'USER')}"
)

st.title("🗃️ DS Group Database GUI")
st.caption("Upload • Validate • Create • Store (Snowflake)")

# =========================================================
# FILE UPLOAD
# =========================================================
file = st.file_uploader(
    "Upload CSV / Excel / JSON",
    type=["csv", "xlsx", "xls", "json"]
)

if file is None:
    st.info("📂 Please upload a file to continue")
    st.stop()

# =========================================================
# LOAD FILE
# =========================================================
try:
    df = load_file(file)
except Exception as e:
    st.error("❌ Failed to read file")
    st.exception(e)
    st.stop()

if df is None or df.empty:
    st.error("❌ Uploaded file is empty")
    st.stop()

st.subheader("📄 Data Preview")
st.dataframe(df.head(50), use_container_width=True)

# =========================================================
# SCHEMA COMPARISON
# =========================================================
try:
    schema_result = compare_schema(df, MAIN_TABLE)
except Exception:
    schema_result = {
        "match": False,
        "missing": [],
        "extra": list(df.columns)
    }

# =========================================================
# SCHEMA MATCH
# =========================================================
if schema_result["match"] is True:
    st.success("✅ Schema matches MAIN table (OUTLET_MASTER)")

    if st.button("⬆️ Upload to Main Table"):
        try:
            upload_df(df, MAIN_TABLE)
            st.success("🎉 Data uploaded successfully to OUTLET_MASTER")
        except Exception as e:
            st.error("❌ Upload failed")
            st.exception(e)

# =========================================================
# SCHEMA MISMATCH
# =========================================================
else:
    st.error("❌ Schema does NOT match main table")

    if schema_result.get("missing"):
        st.warning(f"🟡 Missing Columns: {schema_result['missing']}")

    if schema_result.get("extra"):
        st.warning(f"🔵 Extra Columns: {schema_result['extra']}")

    st.markdown("### ❓ Do you want to create another table?")

    new_table = st.text_input(
        "Enter new table name (UPPERCASE, no spaces)"
    ).strip()

    if st.button("✅ Yes, Create & Upload"):
        if not new_table:
            st.error("❌ Table name cannot be empty")
            st.stop()

        try:
            create_table_from_df(df, new_table)
            upload_df(df, new_table)
            st.success(
                f"✅ Table `{new_table}` created and data uploaded successfully"
            )
        except Exception as e:
            st.error("❌ Failed to create or upload table")
            st.exception(e)
