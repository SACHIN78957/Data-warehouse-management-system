import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")

print("--- Starting ETL Pipeline ---")

os.system(f"python \"{os.path.join(SCRIPTS_DIR,'extract_data.py')}\"")

os.system(f"python \"{os.path.join(SCRIPTS_DIR,'transform_data.py')}\"")

os.system(f"python \"{os.path.join(SCRIPTS_DIR,'data_validation.py')}\"")

os.system(f"python \"{os.path.join(SCRIPTS_DIR,'load_data.py')}\"")
print("--- ETL Complete. Starting Analysis ---")

os.system(f"python \"{os.path.join(SCRIPTS_DIR,'analysis.py')}\"")

os.system(f"python \"{os.path.join(SCRIPTS_DIR,'sales_trend_analysis.py')}\"")
print("\n--- Pipeline and Analysis Complete ---")