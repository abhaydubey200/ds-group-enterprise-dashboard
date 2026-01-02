import pandas as pd
from core.database import get_connection


def upload_df(df, table):
    conn = get_connection()
    cur = conn.cursor()

    df.columns = [c.upper().replace(" ", "_") for c in df.columns]
    df = df.where(pd.notnull(df), None)

    cols = ",".join(df.columns)
    vals = ",".join(["%s"] * len(df.columns))

    sql = f"INSERT INTO {table} ({cols}) VALUES ({vals})"
    cur.executemany(sql, df.values.tolist())

    conn.commit()
    cur.close()
    conn.close()
