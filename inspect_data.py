import pandas as pd
import os

def inspect_csv(path):
    print(f"--- Inspecting {path} ---")
    if not os.path.exists(path):
        print("File not found.")
        return
    try:
        df = pd.read_csv(path, nrows=0) # Read header only
        print(df.columns.tolist())
    except Exception as e:
        print(f"Error reading {path}: {e}")

inspect_csv('output/building_titles_all.csv')
