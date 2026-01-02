from core.database import run_query

def create_table_from_df(df, table_name):
    columns_sql = []
    for col in df.columns:
        columns_sql.append(f'"{col}" STRING')

    query = f"""
    CREATE TABLE {table_name} (
        {",".join(columns_sql)}
    )
    """
    run_query(query)
