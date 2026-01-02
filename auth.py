import bcrypt

# Simple admin user (can extend to DB-backed)
USERS = {
    "admin": bcrypt.hashpw("admin123".encode(), bcrypt.gensalt())
}

def login_user(username, password):
    if username in USERS:
        return bcrypt.checkpw(password.encode(), USERS[username])
    return False

def is_authenticated():
    return "authenticated" in st.session_state and st.session_state.authenticated
