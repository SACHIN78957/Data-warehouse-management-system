import pandas as pd
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WAREHOUSE_DIR = os.path.join(BASE_DIR, "../data_warehouse")
CLEANED_CSV_PATH = os.path.join(WAREHOUSE_DIR, "ecommerce_clean.csv")

# Ensure the cleaned data file exists
if not os.path.exists(CLEANED_CSV_PATH):
    print(f"ERROR: Cleaned data file not found at {CLEANED_CSV_PATH}. Aborting validation.")
    sys.exit(1)

data = pd.read_csv(CLEANED_CSV_PATH)

print("\n--- Starting Data Validation ---")
initial_count = len(data)
validation_errors = 0

# 1. Null Value Check in critical fields
null_prices = data['Price'].isnull().sum()
if null_prices > 0:
    print(f" - WARNING: Found {null_prices} null Price values. Dropping these rows.")
    data.dropna(subset=['Price'], inplace=True)
    validation_errors += null_prices

# 2. Price Range Check (Price must be positive)
invalid_prices = data[data['Price'] <= 0]
if not invalid_prices.empty:
    print(f" - WARNING: Found {len(invalid_prices)} non-positive Price values. Dropping these rows.")
    data.drop(invalid_prices.index, inplace=True)
    validation_errors += len(invalid_prices)

# 3. Platform Consistency Check (Ensure Platforms are one of the expected values)
allowed_platforms = {'Laptops', 'Phones', 'Tablets', 'Cameras'}
invalid_platforms = data[~data['Platform'].isin(allowed_platforms)]
if not invalid_platforms.empty:
    print(f" - WARNING: Found {len(invalid_platforms)} products with invalid Platforms. Dropping these rows.")
    data.drop(invalid_platforms.index, inplace=True)
    validation_errors += len(invalid_platforms)

# 4. Rating Range Check (Ratings are between 0 and 5, assuming a 5-star system)
invalid_ratings = data[(data['Rating'] < 0) | (data['Rating'] > 5)]
if not invalid_ratings.empty:
    print(f" - WARNING: Found {len(invalid_ratings)} invalid Rating values (not 0-5). These will be set to None.")
    data.loc[invalid_ratings.index, 'Rating'] = None
    # Note: We don't drop rows for rating since it's common to have missing ratings.

# Overwrite the cleaned CSV with the validated data
final_count = len(data)
data.to_csv(CLEANED_CSV_PATH, index=False)

print(f" Validation Complete: {initial_count} records checked.")
print(f" {initial_count - final_count} records were dropped due to critical errors (Null Price, Non-Positive Price, Invalid Platform).")
print(f" Final validated record count: {final_count}")

if validation_errors > 0:
    print(" Validation finished with WARNINGS. See log above.")
else:
    print(" Validation finished with NO CRITICAL ERRORS.")
print("--- Data Validation Complete ---")