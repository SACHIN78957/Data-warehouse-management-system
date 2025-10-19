import pandas as pd
from sqlalchemy import create_engine
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "../data_warehouse/ecommerce.db")
engine = create_engine(f"sqlite:///{DB_PATH}")

fact_sales = pd.read_sql("SELECT * FROM fact_sales", engine)
dim_product = pd.read_sql("SELECT * FROM dim_product", engine)
dim_time = pd.read_sql("SELECT * FROM dim_time", engine)

data = fact_sales.merge(dim_product, on='Product_ID').merge(dim_time[['Time_ID','Year','Month']], on='Time_ID')
monthly_sales = data.groupby(['Product','Year','Month'])['Price'].sum().reset_index().sort_values(['Product','Year','Month'])
monthly_sales['MoM_Change'] = monthly_sales.groupby('Product')['Price'].diff()
monthly_sales['Trend'] = monthly_sales['MoM_Change'].apply(lambda x: 'Increase' if x>0 else ('Decrease' if x<0 else 'No change'))

print("\nMonthly sales trend per product:")
for product in monthly_sales['Product'].unique():
    product_data = monthly_sales[monthly_sales['Product']==product]
    print(f"\nProduct: {product}")
    print(product_data[['Year','Month','Price','MoM_Change','Trend']])
