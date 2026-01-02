import pandas as pd
from services.snowflake_service import get_connection


def create_table_from_df(df: pd.DataFrame, table_name: str):
    """
    Create Snowflake table dynamically from DataFrame schema
    """

    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Normalize column names
        columns = [
            col.upper()
            .replace(" ", "_")
            .replace("/", "_")
            .replace("-", "_")
            for col in df.columns
        ]

        # Build column definitions (SAFE MODE)
        column_defs = ",\n".join([f"{col} VARCHAR" for col in columns])

        create_sql = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            {column_defs}
        )
        """

        cursor.execute(create_sql)
        conn.commit()

    except Exception as e:
        conn.rollback()
        raise RuntimeError(f"Table creation failed: {str(e)}")

    finally:
        cursor.close()
        conn.close()
