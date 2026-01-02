import pandas as pd
from core.database import get_connection
from services.audit_service import log_action


def insert_row(table, row, user):
    conn = get_connection()
    cur = conn.cursor()

    cols = ",".join(row.keys())
    vals = ",".join(["%s"] * len(row))
    cur.execute(f"INSERT INTO {table} ({cols}) VALUES ({vals})", list(row.values()))

    conn.commit()
    log_action(table, "INSERT", user, str(row))
    cur.close()
    conn.close()


def update_row(table, row, pk_col, pk_val, user):
    conn = get_connection()
    cur = conn.cursor()

    sets = ",".join([f"{k}=%s" for k in row])
    cur.execute(
        f"UPDATE {table} SET {sets} WHERE {pk_col}=%s",
        list(row.values()) + [pk_val],
    )

    conn.commit()
    log_action(table, "UPDATE", user, f"{pk_col}={pk_val}")
    cur.close()
    conn.close()


def delete_rows(table, pk_col, values, user):
    conn = get_connection()
    cur = conn.cursor()

    placeholders = ",".join(["%s"] * len(values))
    cur.execute(
        f"DELETE FROM {table} WHERE {pk_col} IN ({placeholders})",
        values,
    )

    conn.commit()
    log_action(table, "DELETE", user, f"{values}")
    cur.close()
    conn.close()
