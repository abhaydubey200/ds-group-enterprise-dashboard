import hashlib
from services.snowflake_service import get_connection


def hash_password(password: str) -> str:
    """
    Hash password using SHA256
    """
    return hashlib.sha256(password.encode()).hexdigest()


def authenticate(username: str, password: str):
    """
    Authenticate user against Snowflake USERS table
    Returns user dict if valid else None
    """

    if not username or not password:
        return None

    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            SELECT USERNAME, PASSWORD, ROLE
            FROM USERS
            WHERE USERNAME = %s
              AND IS_ACTIVE = TRUE
        """

        cursor.execute(query, (username,))
        row = cursor.fetchone()

        if not row:
            return None

        db_username, db_password, role = row

        # Accept both plain & hashed passwords (production safe)
        if db_password == password or db_password == hash_password(password):
            return {
                "username": db_username,
                "role": role
            }

        return None

    except Exception as e:
        # Fail silently (security best practice)
        return None

    finally:
        if conn:
            conn.close()
