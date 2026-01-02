import streamlit as st
from core.auth import authenticate

st.set_page_config("DS Group Database GUI", layout="wide")

if "user" not in st.session_state:
    st.title("🔐 DS Group Login")

    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Login"):
        user = authenticate(u, p)
        if user:
            st.session_state.user = user
            st.rerun()
        else:
            st.error("Invalid login")

    st.stop()

st.sidebar.success(f"Logged in as {st.session_state.user['role']}")

page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Database GUI"],
)

if page == "Dashboard":
    import pages.dashboard

if page == "Database GUI":
    import pages.database_gui
