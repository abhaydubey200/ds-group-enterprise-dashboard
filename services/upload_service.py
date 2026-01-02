from core.database import get_connection

def upload_df(df, table_name):
    conn = get_connection()
    cur = conn.cursor()
    try:
        for _, row in df.iterrows():
            placeholders = ",".join(["%s"] * len(row))
            query = f"""
            INSERT INTO {table_name}
            VALUES ({placeholders})
            """
            cur.execute(query, tuple(row.astype(str)))
        conn.commit()
    finally:
        cur.close()
