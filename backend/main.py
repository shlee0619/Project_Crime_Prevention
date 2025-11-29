from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List

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
    lat: float
    lng: float
    risk_score: int
    safety_index: int
    details: dict
    police_stations: List[dict]

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
    # 1. Search building info from CSV
    buildings = ledger_service.get_building_info(address)
    
    # Pick the first building found or a specific one
    target_building = buildings[0] if buildings else {}
    
    # 2. Get Police Count
    # Use 'dongNm' or '동명칭' from building if available
    region_keyword = target_building.get("동명칭", "") or target_building.get("dongNm", "")
    if not region_keyword:
        # Fallback: try to extract Dong from address (e.g. "Samsung-dong")
        # Simple heuristic: split by space and find part ending with 'dong'
        parts = address.split()
        for part in parts:
            if part.endswith("동"):
                region_keyword = part
                break
        if not region_keyword:
            region_keyword = address # Last resort
            
    police_count = geo_service.get_police_count(region_keyword)
    
    # 3. Geocode Address
    lat, lng = geo_service.geocode(address)
    
    # 4. Get Police Stations for Map
    police_stations = geo_service.get_police_stations(region_keyword, lat, lng)
    
    # 5. Calculate scores
    risk_score = risk_calculator.calculate_jeonse_risk(target_building)
    
    # Mock store distance for now (or implement similar density logic if data available)
    store_dist = 0.2 # km
    
    safety_index = risk_calculator.calculate_safety_index(police_count, store_dist)
    
    return {
        "address": address,
        "lat": lat,
        "lng": lng,
        "risk_score": risk_score,
        "safety_index": safety_index,
        "details": {
            "building_name": target_building.get("건물명", "") or target_building.get("bldNm", "Unknown"),
            "main_purpose": target_building.get("주용도명", "") or target_building.get("mainPurpsCdNm", "Unknown"),
            "police_count_in_region": police_count,
            "region_keyword": region_keyword,
            "nearest_store_km": store_dist
        },
        "police_stations": police_stations
    }
