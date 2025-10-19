import pandas as pd
from sqlalchemy import create_engine
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "../data_warehouse/ecommerce.db")
engine = create_engine(f"sqlite:///{DB_PATH}")

dim_product = pd.read_sql("SELECT * FROM dim_product", engine)
dim_platform = pd.read_sql("SELECT * FROM dim_platform", engine)
dim_time = pd.read_sql("SELECT * FROM dim_time", engine)
fact_sales = pd.read_sql("SELECT * FROM fact_sales", engine)

data = fact_sales.merge(dim_product, on='Product_ID').merge(dim_platform, on='Platform_ID').merge(dim_time, on='Time_ID')

top_expensive = data.sort_values('Price', ascending=False).head(5)
print("\nTop 5 most expensive products:")
print(top_expensive[['Product','Platform','Price']])

avg_rating = data.groupby('Platform')['Rating'].mean().reset_index()
print("\nAverage rating per platform:")
print(avg_rating)

count_products = data.groupby('Platform')['Product'].count().reset_index()
print("\nNumber of products per platform:")
print(count_products)

monthly_sales = data.groupby('Month')['Price'].sum().reset_index().sort_values('Month')
print("\nMonthly sales:")
print(monthly_sales)
