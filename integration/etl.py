
import pandas as pd

def load_csv(path):
    return pd.read_csv(path)

def transform(df):
    df = df.copy()
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
    df["popularity"] = df["rating"] * 20
    df["price_bucket"] = pd.cut(
        df["price"], 
        bins=[0, 200, 500, 2000, 10000],
        labels=["Low", "Medium", "Premium", "Luxury"]
    )
    return df

def save_processed(df, out_path):
    df.to_csv(out_path, index=False)
    return out_path
