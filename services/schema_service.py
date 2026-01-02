from core.database import get_connection


def compare_schema(df, table_name):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(f"DESC TABLE {table_name}")
    table_cols = {row[0].upper() for row in cur.fetchall()}

    df_cols = {c.upper().replace(" ", "_") for c in df.columns}

    return {
        "match": df_cols == table_cols,
        "missing": list(table_cols - df_cols),
        "extra": list(df_cols - table_cols),
    }
