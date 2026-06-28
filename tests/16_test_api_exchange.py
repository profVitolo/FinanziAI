from pathlib import Path
import requests
import sys
from test_utils import *

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

server = start_server_if_needed()
print_title("=== TEST API EXCHANGE ===")
try:
    print("\n=== TEST SYNC RATE ===")
    payload = {"from_currency": "USD", "to_currency": "EUR"}
    
    response = requests.post(f"{BASE_URL}/exchange/sync", json=payload)
    print_response(response)

    if response.status_code >= 400:
        raise Exception("Sync rate fallita")

    print("\n=== TEST GET LATEST RATE ===")
    payload = {"from_currency": "USD", "to_currency": "EUR"}
    
    response = requests.get(f"{BASE_URL}/exchange/latest", params=payload)
    print_response(response)

    if response.status_code >= 400:
        raise Exception("Get latest rate fallita")

    print("\n=== TEST GET RATES ===")

    response = requests.get(f"{BASE_URL}/exchange/rates")
    print_response(response)

    if response.status_code >= 400:
        raise Exception("Get rates fallita")

    print("\n=== TEST CONVERT ===")
    payload = {"amount": 100, "from_currency": "USD", "to_currency": "EUR"}
    
    response = requests.get(f"{BASE_URL}/exchange/convert", params=payload)
    print_response(response)

    if response.status_code >= 400:
        raise Exception("Convert fallita")

    print("\n=== TEST MISSING DATES ===")
    payload = {"from_currency": "USD", "to_currency": "EUR", "start_date": "2026-01-01", "end_date": "2026-01-31"}
    
    response = requests.get(f"{BASE_URL}/exchange/missing", params=payload)
    print_response(response)

    if response.status_code >= 400:
        raise Exception("Missing dates fallita")

    print("\n=== TEST SYNC RANGE ===")

    response = requests.post(
        f"{BASE_URL}/exchange/sync-range",
        json={
            "from_currency": "USD",
            "to_currency": "EUR",
            "start_date": "2026-03-01",
            "end_date": "2026-03-31"
        }
    )

    print_response(response)

    if response.status_code >= 400:
        raise Exception("Sync range fallita")
        
    print("\n=== TEST MISSING DATES AFTER RANGE SYNC ===")
    payload = {"from_currency": "USD", "to_currency": "EUR", "start_date": "2026-03-01", "end_date": "2026-03-31"}
    
    response = requests.get(f"{BASE_URL}/exchange/missing", params=payload)
    print_response(response)

    print("\n=== TEST GET RATES AFTER SYNC ===")

    response = requests.get(
        f"{BASE_URL}/exchange/rates",
        params={
            "from_currency": "USD",
            "to_currency": "EUR",
            "start_date": "2026-03-01",
            "end_date": "2026-03-31"
        }
    )
    print_response(response)
    
    print("\n=== TEST GET FROM_CURRENCIES ===")

    response = requests.get(f"{BASE_URL}/exchange/from-currencies")
    print_response(response)
    
    print("\n=== TEST API EXCHANGE COMPLETATO ===")

finally:
    stop_server(server)