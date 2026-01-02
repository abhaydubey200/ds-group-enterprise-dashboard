import pandas as pd

def load_file(file):
    if file.name.endswith(".csv"):
        return pd.read_csv(file)
    if file.name.endswith(".xlsx"):
        return pd.read_excel(file)
    if file.name.endswith(".json"):
        return pd.read_json(file)
    raise ValueError("Unsupported file type")
