import bcrypt
from core.database import run_query

def authenticate(username, password):
    query = """
        SELECT username, password_hash, role
        FROM USERS
        WHERE username = %s AND active = TRUE
    """
    result = run_query(query, [username])
    if not result:
        return None

    db_user, db_hash, role = result[0]
    if bcrypt.checkpw(password.encode(), db_hash.encode()):
        return {"username": db_user, "role": role}
    return None
