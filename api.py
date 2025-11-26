import csv
import csv
import json
import os
import time
from pathlib import Path
from typing import Iterable, List, Tuple

import requests

BASE_URL = "https://apis.data.go.kr/1613000/BldRgstHubService"
API_KEY = os.getenv("API_KEY", "d83c5cdcc8a694c59f25d870112b6f04de67237090952b20fc9be158e0e6b6d5")

OUTPUT_DIR = Path("output")
TARGETS_FILE = Path("targets.csv")  # expected columns: sigunguCd,bjdongCd,platGbCd(optional)
PAGE_SIZE = 100
REQUEST_INTERVAL = 0.15  # seconds between requests to be gentle on the API

# 통합분류코드 기준 컬럼명 한글 매핑 (모르는 필드는 원본 그대로 둠)
COLUMN_KO_MAP = {
    "archArea": "건축면적",
    "atchBldArea": "부속건축물면적",
    "atchBldCnt": "부속건축물수",
    "bcRat": "건폐율",
    "bjdongCd": "법정동코드",
    "bldNm": "건물명",
    "block": "블록",
    "bun": "번",
    "bylotCnt": "부지내동수",
    "crtnDay": "작성일",
    "dongNm": "동명칭",
    "emgenUseElvtCnt": "비상용승강기수",
    "engrEpi": "에너지소요량지표(EPI)",
    "engrGrade": "에너지효율등급",
    "engrRat": "에너지절약율",
    "etcPurps": "기타용도",
    "etcRoof": "기타지붕",
    "etcStrct": "기타구조",
    "fmlyCnt": "세대수",
    "gnBldCert": "녹색건축인증구분",
    "gnBldGrade": "녹색건축인증등급",
    "grndFlrCnt": "지상층수",
    "heit": "건축높이",
    "hhldCnt": "가구수",
    "hoCnt": "호수",
    "indrAutoArea": "옥내자주식주차면적",
    "indrAutoUtcnt": "옥내자주식주차대수",
    "indrMechArea": "옥내기계식주차면적",
    "indrMechUtcnt": "옥내기계식주차대수",
    "itgBldCert": "통합건축인증구분",
    "itgBldGrade": "통합건축인증등급",
    "ji": "지",
    "lot": "롯트",
    "mainAtchGbCd": "주부속구분코드",
    "mainAtchGbCdNm": "주부속구분명",
    "mainPurpsCd": "주용도코드",
    "mainPurpsCdNm": "주용도명",
    "mgmBldrgstPk": "관리건축물대장PK",
    "naBjdongCd": "도로명법정동코드",
    "naMainBun": "도로명본번",
    "naRoadCd": "도로명코드",
    "naSubBun": "도로명부번",
    "naUgrndCd": "지상지하코드",
    "newPlatPlc": "도로명주소",
    "oudrAutoArea": "옥외자주식주차면적",
    "oudrAutoUtcnt": "옥외자주식주차대수",
    "oudrMechArea": "옥외기계식주차면적",
    "oudrMechUtcnt": "옥외기계식주차대수",
    "platArea": "대지면적",
    "platGbCd": "대지구분코드",
    "platPlc": "지번주소",
    "pmsDay": "허가일",
    "pmsnoGbCd": "허가번호구분코드",
    "pmsnoGbCdNm": "허가번호구분명",
    "pmsnoKikCd": "허가권자코드",
    "pmsnoKikCdNm": "허가권자명",
    "pmsnoYear": "허가연도",
    "regstrGbCd": "대장구분코드",
    "regstrGbCdNm": "대장구분명",
    "regstrKindCd": "대장종류코드",
    "regstrKindCdNm": "대장종류명",
    "rideUseElvtCnt": "승용승강기수",
    "rnum": "일련번호",
    "roofCd": "지붕코드",
    "roofCdNm": "지붕명",
    "rserthqkAblty": "내진능력",
    "rserthqkDsgnApplyYn": "내진설계적용여부",
    "sigunguCd": "시군구코드",
    "splotNm": "특수지명",
    "stcnsDay": "착공일",
    "strctCd": "구조코드",
    "strctCdNm": "구조명",
    "totArea": "연면적",
    "totDongTotArea": "전체동연면적",
    "ugrndFlrCnt": "지하층수",
    "useAprDay": "사용승인일",
    "vlRat": "용적률",
    "vlRatEstmTotArea": "용적률산정연면적",
}


def build_params(sigungu_cd: str, bjdong_cd: str, plat_gb_cd: str, page_no: int, num_of_rows: int):
    return {
        "serviceKey": API_KEY,
        "sigunguCd": sigungu_cd,
        "bjdongCd": bjdong_cd,
        "platGbCd": plat_gb_cd,
        "pageNo": page_no,
        "numOfRows": num_of_rows,
        "_type": "json",
    }


def fetch_page(sigungu_cd: str, bjdong_cd: str, plat_gb_cd: str, page_no: int, num_of_rows: int):
    endpoint = f"{BASE_URL}/getBrTitleInfo"
    params = build_params(sigungu_cd, bjdong_cd, plat_gb_cd, page_no, num_of_rows)
    res = requests.get(endpoint, params=params, timeout=20)
    res.raise_for_status()
    return res.json()


def extract_items(response_json):
    """Pull out the item list from the API response. If item is a single dict, wrap it."""
    try:
        items = response_json["response"]["body"]["items"]["item"]
    except (KeyError, TypeError):
        return []

    if isinstance(items, list):
        return items
    if items:
        return [items]
    return []


def get_total_count(response_json) -> int:
    try:
        return int(response_json["response"]["body"]["totalCount"])
    except Exception:
        return 0


def fetch_all_for_area(sigungu_cd: str, bjdong_cd: str, plat_gb_cd: str) -> List[dict]:
    all_items: List[dict] = []
    page_no = 1
    total_count = None

    while True:
        data = fetch_page(sigungu_cd, bjdong_cd, plat_gb_cd, page_no, PAGE_SIZE)
        items = extract_items(data)
        if total_count is None:
            total_count = get_total_count(data)

        if not items:
            break

        all_items.extend(items)

        if total_count and len(all_items) >= total_count:
            break
        if len(items) < PAGE_SIZE:
            break

        page_no += 1
        time.sleep(REQUEST_INTERVAL)

    return all_items


def save_json(items, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)


def translate_row_keys(item: dict) -> dict:
    """Return a new dict with keys translated to Korean if mapping exists."""
    return {COLUMN_KO_MAP.get(k, k): v for k, v in item.items()}


def save_csv(items, path: Path):
    if not items:
        return

    path.parent.mkdir(parents=True, exist_ok=True)

    translated_items = [translate_row_keys(item) for item in items]
    fieldnames = sorted({key for item in translated_items for key in item.keys()})

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for item in translated_items:
            writer.writerow(item)


def load_targets() -> Iterable[Tuple[str, str, str]]:
    """
    Load target (sigunguCd, bjdongCd, platGbCd) rows from targets.csv.
    If the file is missing, fall back to a single sample row so the script still runs.
    """
    if not TARGETS_FILE.exists():
        # sample fallback
        yield ("11680", "10300", "0")
        return

    with TARGETS_FILE.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            sigungu = row.get("sigunguCd") or row.get("sigungu_cd")
            bjdong = row.get("bjdongCd") or row.get("bjdong_cd")
            plat = row.get("platGbCd") or row.get("plat_gb_cd") or "0"
            if sigungu and bjdong:
                yield (sigungu.strip(), bjdong.strip(), plat.strip())


def main():
    aggregated: List[dict] = []

    for sigungu_cd, bjdong_cd, plat_gb_cd in load_targets():
        print(f"Fetching {sigungu_cd}-{bjdong_cd} (platGbCd={plat_gb_cd}) ...")
        try:
            items = fetch_all_for_area(sigungu_cd, bjdong_cd, plat_gb_cd)
        except requests.HTTPError as e:
            print(f"HTTP error for {sigungu_cd}-{bjdong_cd}: {e}")
            continue
        except requests.RequestException as e:
            print(f"Request error for {sigungu_cd}-{bjdong_cd}: {e}")
            continue

        print(f"  -> {len(items)} rows")
        aggregated.extend(items)

    if not aggregated:
        print("No data returned.")
        return

    json_path = OUTPUT_DIR / "building_titles_all.json"
    csv_path = OUTPUT_DIR / "building_titles_all.csv"

    save_json(aggregated, json_path)
    save_csv(aggregated, csv_path)

    print(f"Saved: {json_path} / {csv_path} (total rows: {len(aggregated)})")


if __name__ == "__main__":
    main()
