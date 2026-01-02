from core.database import get_connection


def log_action(table, operation, user, details=""):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO AUDIT_LOG (TABLE_NAME, OPERATION, USERNAME, DETAILS)
        VALUES (%s, %s, %s, %s)
        """,
        (table, operation, user, details),
    )

    conn.commit()
    cur.close()
    conn.close()
