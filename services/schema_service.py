from services.snowflake_service import get_connection


def get_table_schema(table_name: str):
    """
    Fetch column names from Snowflake table
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        query = f"""
        SELECT COLUMN_NAME
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = '{table_name.upper()}'
        ORDER BY ORDINAL_POSITION
        """
        cursor.execute(query)
        return [row[0] for row in cursor.fetchall()]

    finally:
        cursor.close()
        conn.close()


def compare_schema(df, table_name: str):
    """
    Compare uploaded DataFrame schema with Snowflake table schema
    """

    try:
        table_columns = get_table_schema(table_name)
    except Exception:
        return {
            "match": False,
            "error": f"Table `{table_name}` does not exist",
            "missing": [],
            "extra": list(df.columns)
        }

    df_columns = [col.upper() for col in df.columns]
    table_columns = [col.upper() for col in table_columns]

    missing = sorted(set(table_columns) - set(df_columns))
    extra = sorted(set(df_columns) - set(table_columns))

    return {
        "match": len(missing) == 0 and len(extra) == 0,
        "missing": missing,
        "extra": extra
    }
