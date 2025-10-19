import pandas as pd
import os
import re
from glob import glob

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
data_lake_dir = os.path.join(BASE_DIR, "../data_lake")
warehouse_dir = os.path.join(BASE_DIR, "../data_warehouse")
os.makedirs(warehouse_dir, exist_ok=True)

csv_files = glob(os.path.join(data_lake_dir, "*_raw.csv"))
all_data = []
for file in csv_files:
    df = pd.read_csv(file)
    platform = os.path.basename(file).replace("_raw.csv", "")
    df["Platform"] = platform.capitalize()
    all_data.append(df)

data = pd.concat(all_data, ignore_index=True)
data["Price"] = data["Price"].astype(str).apply(lambda x: re.sub(r"[₹$,]", "", x))
data["Price"] = pd.to_numeric(data["Price"], errors="coerce")
data["Rating"] = data["Rating"].astype(str).apply(lambda x: re.search(r"\d+(\.\d+)?", x).group(0) if re.search(r"\d+(\.\d+)?", x) else None)
data["Rating"] = pd.to_numeric(data["Rating"], errors="coerce")
data.dropna(subset=["Price"], inplace=True)
clean_path = os.path.join(warehouse_dir, "ecommerce_clean.csv")
data.to_csv(clean_path, index=False)
print(f" Data transformed and saved to {clean_path}")
