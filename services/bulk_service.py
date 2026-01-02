from core.database import execute_query
from core.audit import log_action

def bulk_delete(user, table, condition):
    query = f"DELETE FROM {table} WHERE {condition}"
    execute_query(query)
    log_action(user, "BULK_DELETE", table, details=condition)
