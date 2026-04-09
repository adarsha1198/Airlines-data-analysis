import os
from sqlalchemy import create_engine
import pandas as pd

folder_path = r'C:\Users\adars\OneDrive\Desktop\airlines data'
server = 'ADS_G15\\SQLEXPRESS'
database = 'MyDatabase'
conn = create_engine(
    f"mssql+pyodbc://@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server")

for file_name in os.listdir(folder_path):
    if file_name.endswith('.csv'):
        file_path = os.path.join(folder_path, file_name)
        print(f"Reading file: {file_name}")
        df = pd.read_csv(file_path)
        table_name = os.path.splitext(file_name)[0]
        df.to_sql(table_name,conn, if_exists='replace', index=False)
        print(f"Loaded '{table_name}' into table '{table_name}'")



