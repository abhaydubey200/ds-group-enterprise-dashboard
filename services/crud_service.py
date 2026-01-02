import pandas as pd
from core.database import run_query, get_connection

def fetch_table(table_name, limit=1000):
    query = f'SELECT * FROM {table_name} LIMIT {limit}'
    rows = run_query(query)

    col_query = f"""
        SELECT COLUMN_NAME
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = '{table_name.upper()}'
        ORDER BY ORDINAL_POSITION
    """
    columns = [c[0] for c in run_query(col_query)]
    return pd.DataFrame(rows, columns=columns)


def insert_row(table_name, row_dict):
    cols = ",".join(f'"{c}"' for c in row_dict.keys())
    placeholders = ",".join(["%s"] * len(row_dict))
    query = f'INSERT INTO {table_name} ({cols}) VALUES ({placeholders})'
    run_query(query, list(row_dict.values()))


def update_row(table_name, row_dict, where_clause):
    set_clause = ",".join([f'"{k}"=%s' for k in row_dict.keys()])
    query = f'UPDATE {table_name} SET {set_clause} WHERE {where_clause}'
    run_query(query, list(row_dict.values()))


def delete_row(table_name, where_clause):
    query = f'DELETE FROM {table_name} WHERE {where_clause}'
    run_query(query)
