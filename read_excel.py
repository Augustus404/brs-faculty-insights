import pandas as pd

try:
    df = pd.read_excel('BRS Fall 26-27.xlsx')
    print("Columns:", df.columns.tolist())
    print(df.head())
except Exception as e:
    print("Error:", e)
