import pandas as pd
import os

def inspect_csv(path):
    print(f"--- Inspecting {path} ---")
    if not os.path.exists(path):
        print("File not found.")
        return
    try:
        df = pd.read_csv(path, nrows=0, encoding='utf-8')
        print(df.columns.tolist())
    except UnicodeDecodeError:
        try:
            df = pd.read_csv(path, nrows=0, encoding='cp949')
            print(df.columns.tolist())
        except Exception as e:
            print(f"Error reading {path}: {e}")
    except Exception as e:
        print(f"Error reading {path}: {e}")

inspect_csv('데이터/서울시 안심귀갓길 경로.csv')
