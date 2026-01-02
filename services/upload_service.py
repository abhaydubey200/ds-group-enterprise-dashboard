import pandas as pd
from services.snowflake_service import get_connection


def upload_df(df: pd.DataFrame, table_name: str):
    """
    Upload DataFrame to Snowflake table safely
    """

    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Normalize column names
        df.columns = [c.upper().replace(" ", "_").replace("/", "_") for c in df.columns]

        # Build INSERT query dynamically
        columns = ", ".join(df.columns)
        placeholders = ", ".join(["%s"] * len(df.columns))

        insert_sql = f"""
        INSERT INTO {table_name} ({columns})
        VALUES ({placeholders})
        """

        # Convert NaN → None (Snowflake compatible)
        records = df.where(pd.notnull(df), None).values.tolist()

        cursor.executemany(insert_sql, records)
        conn.commit()

    except Exception as e:
        conn.rollback()
        raise RuntimeError(f"Upload failed: {str(e)}")

    finally:
        cursor.close()
        conn.close()
