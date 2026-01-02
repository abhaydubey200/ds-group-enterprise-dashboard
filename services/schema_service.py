from core.database import run_query

def get_table_columns(table_name):
    query = f"""
        SELECT COLUMN_NAME
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = '{table_name.upper()}'
        ORDER BY ORDINAL_POSITION
    """
    return [row[0] for row in run_query(query)]

def compare_schema(df, table_name):
    table_cols = get_table_columns(table_name)
    file_cols = list(df.columns)

    missing = set(table_cols) - set(file_cols)
    extra = set(file_cols) - set(table_cols)

    return {
        "match": len(missing) == 0 and len(extra) == 0,
        "missing": list(missing),
        "extra": list(extra),
    }
