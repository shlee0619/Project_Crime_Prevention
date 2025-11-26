class RiskCalculator:
    def __init__(self):
        pass

    def calculate_jeonse_risk(self, building_item: dict) -> int:
        """
        Calculate Jeonse Fraud Risk Score (0-100).
        Higher score means HIGHER RISK.
        """
        score = 0
        
        # 1. Violation Building Check
        # 'etcPurps' or specific field might indicate violation, but usually there is a specific field 'otherConst' or similar in detailed ledger.
        # In TitleInfo (getBrTitleInfo), we check 'etcStrct' or look for keywords in 'bldNm' if labeled as violation? 
        # Actually, 'violationBldYn' is often in the response if available, or we infer.
        # Let's assume we check specific keywords or fields available in COLUMN_KO_MAP from api.py.
        # api.py didn't have 'violationBldYn' mapped, but let's check if it exists in data.
        # If not, we use a placeholder logic based on 'useAprDay' (age of building) or 'hhldCnt' vs 'fmlyCnt' (multi-family housing risk).
        
        # Example: Old buildings might be riskier? Or new villas? 
        # "Kkangtong Jeonse" often happens in new villas (multi-household).
        
        # Logic:
        # If 'mainPurpsCdNm' is '단독주택' (Single family) or '공동주택' (Apartment/Multi-unit), check details.
        
        # Placeholder Risk Factors:
        # 1. Is it a "Villa" (Multi-household)? -> Higher risk of price inflation.
        main_purps = building_item.get("mainPurpsCdNm", "")
        if "다세대" in main_purps or "연립" in main_purps:
            score += 30
            
        # 2. Violation (Mock check as field might not be in TitleInfo)
        # If we had 'violationBldYn', we would use it.
        
        return min(score, 100)

    def calculate_safety_index(self, police_dist_km: float, store_dist_km: float) -> int:
        """
        Calculate Safety Index (0-100).
        Higher score means SAFER.
        """
        score = 100
        
        # Penalize for distance
        if police_dist_km > 1.0:
            score -= 20
        elif police_dist_km > 0.5:
            score -= 10
            
        if store_dist_km > 0.5:
            score -= 10
            
        return max(score, 0)
