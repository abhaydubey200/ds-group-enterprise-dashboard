import pandas as pd
import io

def read_file(file):
    if file.name.endswith(".csv"):
        return pd.read_csv(file)
    elif file.name.endswith((".xlsx", ".xls")):
        return pd.read_excel(file)
    elif file.name.endswith(".json"):
        return pd.read_json(file)
    return None

def clean_data(df, schema=None):
    before = len(df)
    df = df.drop_duplicates()
    duplicates_removed = before - len(df)
    df = df.fillna("NA")

    if schema:
        for col, dtype in schema.items():
            if col in df.columns:
                try:
                    df[col] = df[col].astype(dtype)
                except:
                    df[col] = df[col].apply(lambda x: str(x))
    return df, duplicates_removed

def export_csv(df):
    return df.to_csv(index=False).encode("utf-8")

def export_excel(df):
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False)
    return buffer.getvalue()
