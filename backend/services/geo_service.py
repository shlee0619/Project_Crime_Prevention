<<<<<<< HEAD
import math

class GeoService:
    def __init__(self):
        pass

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
=======
import math

class GeoService:
    def __init__(self):
        pass

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
>>>>>>> c345c6185857f7d82ccfa276e2c4a6625982f41c
