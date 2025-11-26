<<<<<<< HEAD
import os
import requests
from typing import List, Optional

class BuildingLedgerService:
    BASE_URL = "https://apis.data.go.kr/1613000/BldRgstHubService"
    # Use environment variable or default key from api.py
    API_KEY = os.getenv("API_KEY", "d83c5cdcc8a694c59f25d870112b6f04de67237090952b20fc9be158e0e6b6d5")

    def __init__(self):
        pass

    def get_building_info(self, sigungu_cd: str, bjdong_cd: str, plat_gb_cd: str = "0") -> List[dict]:
        """
        Fetch building info for a specific location.
        Returns a list of building items.
        """
        # For prototype, we might want to fetch just the title info
        endpoint = f"{self.BASE_URL}/getBrTitleInfo"
        params = {
            "serviceKey": self.API_KEY,
            "sigunguCd": sigungu_cd,
            "bjdongCd": bjdong_cd,
            "platGbCd": plat_gb_cd,
            "numOfRows": 100,
            "pageNo": 1,
            "_type": "json"
        }
        
        try:
            res = requests.get(endpoint, params=params, timeout=10)
            res.raise_for_status()
            data = res.json()
            return self._extract_items(data)
        except Exception as e:
            print(f"Error fetching building info: {e}")
            return []

    def _extract_items(self, response_json):
        try:
            items = response_json["response"]["body"]["items"]["item"]
            if isinstance(items, list):
                return items
            if items:
                return [items]
            return []
        except (KeyError, TypeError):
            return []
=======
import os
import requests
from typing import List, Optional

class BuildingLedgerService:
    BASE_URL = "https://apis.data.go.kr/1613000/BldRgstHubService"
    # Use environment variable or default key from api.py
    API_KEY = os.getenv("API_KEY", "d83c5cdcc8a694c59f25d870112b6f04de67237090952b20fc9be158e0e6b6d5")

    def __init__(self):
        pass

    def get_building_info(self, sigungu_cd: str, bjdong_cd: str, plat_gb_cd: str = "0") -> List[dict]:
        """
        Fetch building info for a specific location.
        Returns a list of building items.
        """
        # For prototype, we might want to fetch just the title info
        endpoint = f"{self.BASE_URL}/getBrTitleInfo"
        params = {
            "serviceKey": self.API_KEY,
            "sigunguCd": sigungu_cd,
            "bjdongCd": bjdong_cd,
            "platGbCd": plat_gb_cd,
            "numOfRows": 100,
            "pageNo": 1,
            "_type": "json"
        }
        
        try:
            res = requests.get(endpoint, params=params, timeout=10)
            res.raise_for_status()
            data = res.json()
            return self._extract_items(data)
        except Exception as e:
            print(f"Error fetching building info: {e}")
            return []

    def _extract_items(self, response_json):
        try:
            items = response_json["response"]["body"]["items"]["item"]
            if isinstance(items, list):
                return items
            if items:
                return [items]
            return []
        except (KeyError, TypeError):
            return []
>>>>>>> c345c6185857f7d82ccfa276e2c4a6625982f41c
