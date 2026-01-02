import pandas as pd
from core.database import run_query, get_connection

def fetch_table(table_name, limit=1000):
    query = f'SELECT * FROM {table_name} LIMIT {limit}'
    rows = run_query(query)
    columns = [desc[0] for desc in get_connection().cursor().execute(query).description]
    return pd.DataFrame(rows, columns=columns)

def delete_rows(table_name, condition):
    query = f"DELETE FROM {table_name} WHERE {condition}"
    run_query(query)

def insert_row(table_name, row_dict):
    cols = ",".join([f'"{c}"' for c in row_dict.keys()])
    values = ",".join(["%s"] * len(row_dict))
    query = f"INSERT INTO {table_name} ({cols}) VALUES ({values})"
    run_query(query, list(row_dict.values()))

def update_row(table_name, updates, condition):
    set_clause = ",".join([f'"{k}"=%s' for k in updates.keys()])
    query = f"UPDATE {table_name} SET {set_clause} WHERE {condition}"
    run_query(query, list(updates.values()))
