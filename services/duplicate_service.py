from core.database import fetch_df, execute_query
from core.audit import log_action

def find_duplicates(table, column):
    query = f"""
        SELECT {column}, COUNT(*) cnt
        FROM {table}
        GROUP BY {column}
        HAVING COUNT(*) > 1
    """
    return fetch_df(query)

def merge_duplicates(user, table, column, value):
    query = f"""
        DELETE FROM {table}
        WHERE {column}=%s
        AND ID NOT IN (
            SELECT MIN(ID) FROM {table} WHERE {column}=%s
        )
    """
    execute_query(query, (value, value))
    log_action(user, "MERGE", table, details=f"Merged {column}={value}")

