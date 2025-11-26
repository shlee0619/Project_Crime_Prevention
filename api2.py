import csv
import json
import os
import time
from pathlib import Path
from typing import Iterable, List, Tuple
import requests

BASE_URL = "https://apis.data.go.kr/B553077/api/open/sdsc2"
API_KEY = os.getenv("API_KEY", "d83c5cdcc8a694c59f25d870112b6f04de67237090952b20fc9be158e0e6b6d5")

OUTPUT_DIR = Path("output")
TARGETS_FILE = Path("targets2.csv")  # expected columns: emdongNm

PAGE_SIZE = 100
REQUEST_INTERVAL = 0.15  # seconds

def build_params(emdong_nm: str, page_no: int, num_of_rows: int):
    return {
        "serviceKey": API_KEY,
        "emdongNm": emdong_nm,      # 행정동명
        "numOfRows": num_of_rows,   # 페이지 당 데이터 개수
        "pageNo": page_no,          # 페이지 번호
        "resultType": "json",       # JSON 형태 결과
    }

def fetch_page(emdong_nm: str, page_no: int, num_of_rows: int):
    params = build_params(emdong_nm, page_no, num_of_rows)
    res = requests.get(BASE_URL, params=params, timeout=20)
    res.raise_for_status()
    return res.json()

def extract_items(response_json):
    try:
        items = response_json["body"]["items"]
    except (KeyError, TypeError):
        return []
    return items if isinstance(items, list) else [items]

def get_total_count(response_json) -> int:
    try:
        return int(response_json["body"]["totalCount"])
    except Exception:
        return 0

def fetch_all_for_area(emdong_nm: str) -> List[dict]:
    all_items: List[dict] = []
    page_no = 1
    total_count = None

    while True:
        data = fetch_page(emdong_nm, page_no, PAGE_SIZE)
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

def save_csv(items, path: Path):
    if not items:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = sorted({key for item in items for key in item.keys()})
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for item in items:
            writer.writerow(item)

def load_targets() -> Iterable[str]:
    if not TARGETS_FILE.exists():
        yield "역삼동"
        return

    with TARGETS_FILE.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            emdong_nm = row.get("emdongNm")
            if emdong_nm:
                yield emdong_nm.strip()

def main():
    aggregated: List[dict] = []

    for emdong_nm in load_targets():
        print(f"Fetching {emdong_nm} ...")
        try:
            items = fetch_all_for_area(emdong_nm)
        except requests.HTTPError as e:
            print(f"HTTP error for {emdong_nm}: {e}")
            continue
        except requests.RequestException as e:
            print(f"Request error for {emdong_nm}: {e}")
            continue

        print(f"  -> {len(items)} rows")
        aggregated.extend(items)

    if not aggregated:
        print("No data returned.")
        return

    json_path = OUTPUT_DIR / "stores_by_emdong.json"
    csv_path = OUTPUT_DIR / "stores_by_emdong.csv"

    save_json(aggregated, json_path)
    save_csv(aggregated, csv_path)

    print(f"Saved: {json_path} / {csv_path} (total rows: {len(aggregated)})")

if __name__ == "__main__":
    main()
