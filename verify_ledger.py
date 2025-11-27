from backend.services.building_ledger import BuildingLedgerService

service = BuildingLedgerService()
print("--- DataFrame Head ---")
if service.df is not None:
    print(service.df[['건물명', '도로명주소']].head())
    
print("--- Searching for '강남구' ---")
results = service.get_building_info("강남구")
print(f"Found {len(results)} results.")
if results:
    print(results[0])
else:
    print("No results found.")
