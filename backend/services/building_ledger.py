import os
import pandas as pd
from typing import List, Optional

class BuildingLedgerService:
    # Use absolute path or relative to where main.py is run
    CSV_PATH = "output/building_titles_all.csv"

    def __init__(self):
        self.df = None
        self.load_data()

    def load_data(self):
        if os.path.exists(self.CSV_PATH):
            try:
                self.df = pd.read_csv(self.CSV_PATH)
                # Ensure string type for comparison
                # Korean column names: 지번주소 (platPlc), 도로명주소 (newPlatPlc)
                if '지번주소' in self.df.columns:
                    self.df['지번주소'] = self.df['지번주소'].astype(str)
                if '도로명주소' in self.df.columns:
                    self.df['도로명주소'] = self.df['도로명주소'].astype(str)
                    
                print(f"Loaded {len(self.df)} rows from {self.CSV_PATH}")
            except Exception as e:
                print(f"Error loading CSV: {e}")
                self.df = pd.DataFrame()
        else:
            print(f"CSV file not found at {self.CSV_PATH}")
            self.df = pd.DataFrame()

    def get_building_info(self, address: str) -> List[dict]:
        """
        Search building info by address.
        Returns a list of building items (dicts).
        """
        if self.df is None or self.df.empty:
            return []

    def get_building_info(self, address: str) -> List[dict]:
        """
        Search building info by address.
        Returns a list of building items (dicts).
        """
        if self.df is None or self.df.empty:
            return []

        # Simple containment search
        # Filter where address is in '지번주소' or '도로명주소'
        mask = pd.Series([False] * len(self.df))
        
        if '지번주소' in self.df.columns:
            mask |= self.df['지번주소'].str.contains(address, na=False)
        if '도로명주소' in self.df.columns:
            mask |= self.df['도로명주소'].str.contains(address, na=False)
        
        results = self.df[mask]
        
        # Convert to list of dicts
        return results.to_dict('records')
