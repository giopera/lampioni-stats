from datetime import datetime
import json
import time
import os
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


OVERPASS_ENDPOINTS = [
    "https://overpass-api.de/api/interpreter",
    "https://maps.mail.ru/osm/tools/overpass/api/interpreter",
    "https://overpass.private.coffee/api/interpreter"
]


ITALY_RELATION_ID = 365331

BASELINE_DATE = "2026-02-01T00:00:00Z"

DATA_DIR = "./data/"
OUT_DIR = DATA_DIR + datetime.today().strftime('%Y-%m-%d') + "/"

def fetchOsmData(since_date=BASELINE_DATE):
    query = f"""
        [out:json][timeout:180];
        rel({ITALY_RELATION_ID});
        map_to_area->.italy;
        node["highway"="street_lamp"](area.italy)(newer:"{since_date}");
        out meta;
    """
    return overpass_query(query)

def overpass_query(query, timeout_sec=300, retries=5):
    data = query.encode('utf-8')
    last_error = None
    tries = 0
    for endpoint in OVERPASS_ENDPOINTS:
        while tries < retries: 
            try:
                req = Request(endpoint, data=data, headers={
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'User-Agent': 'LampStats/1.0 (https://github.com/giopera/Lamp-Stats)'
                })
                print(f"  Trying {endpoint.split('/')[2]}...")

                with urlopen(req, timeout=timeout_sec) as response:
                    result = response.read().decode('utf-8')
                    return result

            except HTTPError as e:
                print(f"    HTTP {e.code}: {e.reason}")
                last_error = e
                if e.code == 429:  # Rate limited - wait before trying next
                    time.sleep(5)

            except URLError as e:
                print(f"    Error: {e.reason}")
                last_error = e

            except Exception as e:
                print(f"    Error: {e}")
                last_error = e
            tries = tries + 1
        tries = 0
    raise Exception(f"All Overpass endpoints failed. Last error: {last_error}")

if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(OUT_DIR + "data.json", 'w') as f:
        f.write(fetchOsmData())