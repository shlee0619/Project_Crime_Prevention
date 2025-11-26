<<<<<<< HEAD
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Safe-Housing Map API")

# CORS setup for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AddressRequest(BaseModel):
    address: str

class RiskScoreResponse(BaseModel):
    address: str
    risk_score: int
    safety_index: int
    details: dict

@app.get("/")
def read_root():
    return {"message": "Safe-Housing Map API is running"}

from .services.risk_calculator import RiskCalculator
from .services.geo_service import GeoService
from .services.building_ledger import BuildingLedgerService

risk_calculator = RiskCalculator()
geo_service = GeoService()
ledger_service = BuildingLedgerService()

@app.get("/api/risk-score", response_model=RiskScoreResponse)
def get_risk_score(address: str):
    # 1. Geocode address (Mock)
    lat, lon = geo_service.geocode(address)
    
    # 2. Fetch building ledger info
    # We need to convert address to sigungu/bjdong codes. 
    # For prototype, we'll hardcode a sample location or use a lookup if possible.
    # Let's use the sample from api.py (Gangnam-gu Samsung-dong) for ANY address for now to show data flow.
    sigungu_cd = "11680" # Gangnam-gu
    bjdong_cd = "10500"  # Samsung-dong
    
    buildings = ledger_service.get_building_info(sigungu_cd, bjdong_cd)
    
    # Pick the first building found or a specific one
    target_building = buildings[0] if buildings else {}
    
    # 3. Calculate scores
    risk_score = risk_calculator.calculate_jeonse_risk(target_building)
    
    # Mock distances
    police_dist = 0.4 # km
    store_dist = 0.2 # km
    safety_index = risk_calculator.calculate_safety_index(police_dist, store_dist)
    
    return {
        "address": address,
        "risk_score": risk_score,
        "safety_index": safety_index,
        "details": {
            "building_name": target_building.get("bldNm", "Unknown"),
            "main_purpose": target_building.get("mainPurpsCdNm", "Unknown"),
            "nearest_police_station_km": police_dist,
            "nearest_store_km": store_dist
        }
    }
=======
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Safe-Housing Map API")

# CORS setup for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AddressRequest(BaseModel):
    address: str

class RiskScoreResponse(BaseModel):
    address: str
    risk_score: int
    safety_index: int
    details: dict

@app.get("/")
def read_root():
    return {"message": "Safe-Housing Map API is running"}

from .services.risk_calculator import RiskCalculator
from .services.geo_service import GeoService
from .services.building_ledger import BuildingLedgerService

risk_calculator = RiskCalculator()
geo_service = GeoService()
ledger_service = BuildingLedgerService()

@app.get("/api/risk-score", response_model=RiskScoreResponse)
def get_risk_score(address: str):
    # 1. Geocode address (Mock)
    lat, lon = geo_service.geocode(address)
    
    # 2. Fetch building ledger info
    # We need to convert address to sigungu/bjdong codes. 
    # For prototype, we'll hardcode a sample location or use a lookup if possible.
    # Let's use the sample from api.py (Gangnam-gu Samsung-dong) for ANY address for now to show data flow.
    sigungu_cd = "11680" # Gangnam-gu
    bjdong_cd = "10500"  # Samsung-dong
    
    buildings = ledger_service.get_building_info(sigungu_cd, bjdong_cd)
    
    # Pick the first building found or a specific one
    target_building = buildings[0] if buildings else {}
    
    # 3. Calculate scores
    risk_score = risk_calculator.calculate_jeonse_risk(target_building)
    
    # Mock distances
    police_dist = 0.4 # km
    store_dist = 0.2 # km
    safety_index = risk_calculator.calculate_safety_index(police_dist, store_dist)
    
    return {
        "address": address,
        "risk_score": risk_score,
        "safety_index": safety_index,
        "details": {
            "building_name": target_building.get("bldNm", "Unknown"),
            "main_purpose": target_building.get("mainPurpsCdNm", "Unknown"),
            "nearest_police_station_km": police_dist,
            "nearest_store_km": store_dist
        }
    }
>>>>>>> c345c6185857f7d82ccfa276e2c4a6625982f41c
