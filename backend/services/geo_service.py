import math
import pandas as pd
import os

class GeoService:
    POLICE_CSV_PATH = "데이터/경찰청_전국 지구대 파출소 주소 현황_20241231.csv"

    def __init__(self):
        self.police_df = None
        self.load_police_data()

    def load_police_data(self):
        if os.path.exists(self.POLICE_CSV_PATH):
            try:
                # Try reading with cp949 (common for Korean public data)
                self.police_df = pd.read_csv(self.POLICE_CSV_PATH, encoding='cp949')
                print(f"Loaded {len(self.police_df)} police stations.")
            except UnicodeDecodeError:
                try:
                    self.police_df = pd.read_csv(self.POLICE_CSV_PATH, encoding='utf-8')
                    print(f"Loaded {len(self.police_df)} police stations (utf-8).")
                except Exception as e:
                    print(f"Error loading police CSV: {e}")
                    self.police_df = pd.DataFrame()
            except Exception as e:
                print(f"Error loading police CSV: {e}")
                self.police_df = pd.DataFrame()
        else:
            print(f"Police CSV not found at {self.POLICE_CSV_PATH}")
            self.police_df = pd.DataFrame()

    def get_police_count(self, region_keyword: str) -> int:
        """
        Count police stations in the region (e.g., 'Samsung-dong').
        """
        if self.police_df is None or self.police_df.empty:
            return 0
            
        # Filter by address containing the keyword
        mask = self.police_df['주소'].str.contains(region_keyword, na=False)
        return int(mask.sum())

    def geocode(self, address: str):
        """
        Convert address to (lat, lon).
        Mock implementation for now.
        """
        # Seoul City Hall as default mock
        return 37.5665, 126.9780

    def calculate_distance(self, lat1, lon1, lat2, lon2):
        """
        Haversine formula to calculate distance in km.
        """
        R = 6371  # Earth radius in km
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat / 2) * math.sin(dlat / 2) + \
            math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * \
            math.sin(dlon / 2) * math.sin(dlon / 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        d = R * c
        return d
