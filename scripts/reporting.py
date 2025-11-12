import pandas as pd
from sqlalchemy import create_engine
import os
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "../data_warehouse/ecommerce.db")
engine = create_engine(f"sqlite:///{DB_PATH}")
REPORTS_DIR = os.path.join(BASE_DIR, "../reports/charts")

os.makedirs(REPORTS_DIR, exist_ok=True)

dim_product = pd.read_sql("SELECT * FROM dim_product", engine)
dim_platform = pd.read_sql("SELECT * FROM dim_platform", engine)
dim_time = pd.read_sql("SELECT * FROM dim_time", engine)
fact_sales = pd.read_sql("SELECT * FROM fact_sales", engine)

data = fact_sales.merge(dim_product, on='Product_ID').merge(dim_platform, on='Platform_ID').merge(dim_time, on='Time_ID')

monthly_sales = data.groupby('Month')['Price'].sum().reset_index().sort_values('Month')

plt.figure(figsize=(10, 6))
plt.plot(monthly_sales['Month'], monthly_sales['Price'], marker='o', linestyle='-', color='skyblue')
plt.title('Monthly Total Sales Trend')
plt.xlabel('Month')
plt.ylabel('Total Sales ($)')
plt.grid(True)
plt.xticks(monthly_sales['Month'])
plt.savefig(os.path.join(REPORTS_DIR, 'monthly_sales_trend.png'))
plt.close()
print(f" Monthly Sales Trend chart saved to {os.path.join(REPORTS_DIR, 'monthly_sales_trend.png')}")


avg_rating = data.groupby('Platform')['Rating'].mean().reset_index()

plt.figure(figsize=(8, 5))
plt.bar(avg_rating['Platform'], avg_rating['Rating'], color='lightcoral')
plt.title('Average Rating per Platform')
plt.xlabel('Platform')
plt.ylabel('Average Rating')
plt.ylim(0, 5) 
plt.savefig(os.path.join(REPORTS_DIR, 'avg_rating_by_platform.png'))
plt.close()
print(f" Average Rating by Platform chart saved to {os.path.join(REPORTS_DIR, 'avg_rating_by_platform.png')}")