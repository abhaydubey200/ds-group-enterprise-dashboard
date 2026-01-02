import streamlit as st
import bcrypt
from database import get_connection

def login():
    st.title("🟢 DS Group Admin Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT password, role FROM users WHERE username=%s", (username,))
        row = cur.fetchone()
        conn.close()

        if row and bcrypt.checkpw(password.encode(), row[0].encode()):
            st.session_state["authenticated"] = True
            st.session_state["role"] = row[1]
            st.experimental_rerun()
        else:
            st.error("Invalid credentials")

def is_admin():
    return st.session_state.get("role") == "admin"
