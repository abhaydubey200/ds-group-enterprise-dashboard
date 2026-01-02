from core.database import execute_query
from datetime import datetime

def log_action(user, action, table, record_id=None, details=None):
    query = """
        INSERT INTO AUDIT_LOG
        (USERNAME, ROLE, ACTION, TABLE_NAME, RECORD_ID, DETAILS, TIMESTAMP)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
    """
    execute_query(query, (
        user["username"],
        user["role"],
        action,
        table,
        record_id,
        details,
        datetime.utcnow()
    ))

