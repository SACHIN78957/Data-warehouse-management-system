import pandas as pd
from sqlalchemy import create_engine
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
warehouse_dir = os.path.join(BASE_DIR, "../data_warehouse")
cleaned_csv = os.path.join(warehouse_dir, "ecommerce_clean.csv")
data = pd.read_csv(cleaned_csv)

dim_product = data[['Product']].drop_duplicates().reset_index(drop=True)
dim_product['Product_ID'] = dim_product.index + 1
dim_platform = data[['Platform']].drop_duplicates().reset_index(drop=True)
dim_platform['Platform_ID'] = dim_platform.index + 1

data['Transaction_Date'] = pd.date_range(start='2024-01-01', periods=len(data), freq='D')
dim_time = pd.DataFrame({'Transaction_Date': data['Transaction_Date'].unique()})
dim_time['Transaction_Date'] = pd.to_datetime(dim_time['Transaction_Date'])
dim_time['Year'] = dim_time['Transaction_Date'].dt.year
dim_time['Month'] = dim_time['Transaction_Date'].dt.month
dim_time['Day'] = dim_time['Transaction_Date'].dt.day
dim_time['Time_ID'] = dim_time.index + 1

fact_sales = data.merge(dim_product, on='Product', how='left')
fact_sales = fact_sales.merge(dim_platform, on='Platform', how='left')
fact_sales['Transaction_Date'] = pd.to_datetime(fact_sales['Transaction_Date'], errors='coerce')
dim_time['Transaction_Date'] = pd.to_datetime(dim_time['Transaction_Date'], errors='coerce')
fact_sales = fact_sales.merge(dim_time, on='Transaction_Date', how='left')
fact_sales = fact_sales[['Product_ID','Platform_ID','Time_ID','Price','Rating']]

engine = create_engine(f"sqlite:///{os.path.join(warehouse_dir, 'ecommerce.db')}")
dim_product.to_sql('dim_product', con=engine, if_exists='replace', index=False)
dim_platform.to_sql('dim_platform', con=engine, if_exists='replace', index=False)
dim_time.to_sql('dim_time', con=engine, if_exists='replace', index=False)
fact_sales.to_sql('fact_sales', con=engine, if_exists='replace', index=False)

print(" Data successfully loaded into SQLite warehouse: ecommerce.db")
print(" Tables created: dim_product, dim_platform, dim_time, fact_sales")
