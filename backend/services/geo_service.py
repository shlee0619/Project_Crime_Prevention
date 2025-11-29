import math
import pandas as pd
import os
import requests
import random

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

    def get_police_stations(self, region_keyword: str, center_lat: float, center_lon: float) -> list:
        """
        Get list of police stations in the region.
        Since CSV has no coordinates, we mock them around the center for visualization.
        In a real app, we would geocode these or use a dataset with coords.
        """
        if self.police_df is None or self.police_df.empty:
            return []

        # Filter by address containing the keyword
        mask = self.police_df['주소'].str.contains(region_keyword, na=False)
        filtered_df = self.police_df[mask]
        
        stations = []
        for idx, row in filtered_df.iterrows():
            # Mock coordinates: random offset from center within ~1km
            # 1 deg lat ~ 111km, 0.01 ~ 1.1km
            lat_offset = random.uniform(-0.005, 0.005)
            lon_offset = random.uniform(-0.005, 0.005)
            
            stations.append({
                "name": row['관서명'],
                "address": row['주소'],
                "lat": center_lat + lat_offset,
                "lng": center_lon + lon_offset,
                "type": row['구분']
            })
            
            # Limit to 10 for demo
            if len(stations) >= 10:
                break
                
        return stations

    def geocode(self, address: str):
        """
        Convert address to (lat, lon) using Nominatim (OSM).
        """
        try:
            url = "https://nominatim.openstreetmap.org/search"
            params = {
                "q": address,
                "format": "json",
                "limit": 1
            }
            headers = {
                "User-Agent": "SafeHousingMap/1.0 (shlee@example.com)" 
            }
            response = requests.get(url, params=params, headers=headers, timeout=5)
            response.raise_for_status()
            data = response.json()
            
            if data:
                return float(data[0]["lat"]), float(data[0]["lon"])
        except Exception as e:
            print(f"Geocoding failed for {address}: {e}")
        
        # Fallback: Seoul City Hall
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
