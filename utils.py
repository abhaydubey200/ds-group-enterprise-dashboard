import pandas as pd

def clean_file(uploaded_file):
    ext = uploaded_file.name.split(".")[-1]
    if ext == "csv":
        df = pd.read_csv(uploaded_file)
    elif ext == "xlsx":
        df = pd.read_excel(uploaded_file)
    elif ext == "json":
        df = pd.read_json(uploaded_file)
    else:
        df = pd.DataFrame()
    return df.fillna("")

def remove_duplicates(df):
    return df.drop_duplicates()

def export_file(df, file_type="csv"):
    if file_type == "csv":
        df.to_csv("export.csv", index=False)
    elif file_type == "xlsx":
        df.to_excel("export.xlsx", index=False)

def get_db_config():
    import streamlit as st
    return {
        "host": st.secrets["db"]["host"],
        "user": st.secrets["db"]["user"],
        "password": st.secrets["db"]["password"],
        "database": st.secrets["db"]["name"],
        "port": st.secrets["db"]["port"]
    }
