import pandas as pd


def find_duplicates(df, subset_cols):
    return df[df.duplicated(subset=subset_cols, keep=False)]


def merge_duplicates(df, subset_cols):
    return df.drop_duplicates(subset=subset_cols, keep="first")
