class RiskCalculator:
    def __init__(self):
        pass

    def calculate_jeonse_risk(self, building_item: dict) -> int:
        """
        Calculate Jeonse Fraud Risk Score (0-100).
        Higher score means HIGHER RISK.
        
        Factors:
        1. Housing Type (Villa/Multi-household) -> Higher Risk
        2. Building Age (New < 2 years) -> Higher Risk (Price bubble)
        3. Violation Building -> Critical Risk (Mock)
        """
        score = 0
        current_year = 2024 # Mock current year, or use datetime
        
        # 1. Housing Type Risk (+30)
        # "Kkangtong Jeonse" is most common in Villas (Multi-household/Row houses)
        # Korean key: 주용도명 (mainPurpsCdNm)
        main_purps = building_item.get("주용도명", "") or building_item.get("mainPurpsCdNm", "")
        if "다세대" in main_purps or "연립" in main_purps:
            score += 30
        elif "오피스텔" in main_purps: # Officetels are also risky
            score += 20
            
        # 2. Building Age Risk (+20)
        # New buildings often have inflated prices and no market price history.
        # Korean key: 사용승인일 (useAprDay)
        use_apr_day = building_item.get("사용승인일") or building_item.get("useAprDay")
        age = 0
        if use_apr_day and len(str(use_apr_day)) >= 4:
            try:
                build_year = int(str(use_apr_day)[:4])
                age = current_year - build_year
                if age <= 2:
                    score += 20
            except ValueError:
                pass
                
        # 3. Violation Building Risk (+50)
        # If 'violationBldYn' is 'Y' or inferred from other fields.
        # For now, we don't have this field in TitleInfo usually, but let's check a mock condition
        # or if specific keywords exist in 'etcPurps' or 'bldNm'.
        # Mock: Randomly assign violation risk for demonstration if not real data?
        # Better: Check if 'etcStrct' contains '위반' (Violation) - unlikely but possible.
        # Let's leave it as a placeholder comment for now.
        
        # 4. Base Risk (+10)
        # General market uncertainty
        score += 10
        
        return min(score, 100)

    def calculate_safety_index(self, police_count: int, store_dist_km: float) -> int:
        """
        Calculate Safety Index (0-100).
        Higher score means SAFER.
        
        Factors:
        - Police Station Density (40%) -> Count in Dong
        - Distance to 24h Store (30%) -> Mock distance for now (or density if data available)
        - Base Score (30%)
        """
        # 1. Police Score (0-40)
        # 0: 0 pts
        # 1-2: 20 pts
        # 3+: 40 pts
        if police_count >= 3:
            police_score = 40
        elif police_count >= 1:
            police_score = 20
        else:
            police_score = 0
            
        # 2. Store Score (0-30)
        # < 0.3km: 30 pts
        # 0.3 - 0.7km: 15 pts
        # > 0.7km: 0 pts
        if store_dist_km <= 0.3:
            store_score = 30
        elif store_dist_km <= 0.7:
            store_score = 15
        else:
            store_score = 0
            
        # 3. Base Score (30)
        base_score = 30
        
        total_score = police_score + store_score + base_score
        return min(max(total_score, 0), 100)
