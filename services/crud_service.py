from core.database import execute_query, fetch_df
from core.audit import log_action

def fetch_table(table):
    return fetch_df(f"SELECT * FROM {table}")

def insert_row(user, table, data):
    cols = ",".join(data.keys())
    vals = ",".join(["%s"] * len(data))
    query = f"INSERT INTO {table} ({cols}) VALUES ({vals})"
    execute_query(query, tuple(data.values()))
    log_action(user, "CREATE", table, details=str(data))

def update_row(user, table, pk, updates):
    sets = ",".join([f"{k}=%s" for k in updates])
    query = f"UPDATE {table} SET {sets} WHERE ID=%s"
    execute_query(query, (*updates.values(), pk))
    log_action(user, "UPDATE", table, pk, str(updates))

def delete_row(user, table, pk):
    execute_query(f"DELETE FROM {table} WHERE ID=%s", (pk,))
    log_action(user, "DELETE", table, pk)
