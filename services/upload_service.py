import pandas as pd
from services.snowflake_service import get_connection


def upload_df(df: pd.DataFrame, table_name: str, chunk_size: int = 500):
    """
    Upload DataFrame to Snowflake table safely using executemany
    """

    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Normalize column names to match Snowflake table
        df = df.copy()
        df.columns = [
            col.upper()
            .replace(" ", "_")
            .replace("/", "_")
            .replace("-", "_")
            for col in df.columns
        ]

        # Replace NaN with None (Snowflake compatible)
        df = df.where(pd.notnull(df), None)

        columns = ",".join(df.columns)
        placeholders = ",".join(["%s"] * len(df.columns))

        insert_sql = f"""
        INSERT INTO {table_name} ({columns})
        VALUES ({placeholders})
        """

        # Upload in chunks (production safe)
        for i in range(0, len(df), chunk_size):
            chunk = df.iloc[i:i + chunk_size]
            cursor.executemany(insert_sql, chunk.values.tolist())

        conn.commit()

    except Exception as e:
        conn.rollback()
        raise RuntimeError(f"Upload failed: {str(e)}")

    finally:
        cursor.close()
        conn.close()
