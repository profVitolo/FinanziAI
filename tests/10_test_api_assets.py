from pathlib import Path
import requests
from api_test_utils import *
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

server = start_server_if_needed()

print_title("=== TEST UVICORN API ===")
    
try:
    print("\n=== TEST ASSET SYNC ===")
    
    payload = {"start_date": "2026-01-01"}
    response = requests.post(f"{BASE_URL}/assets/AAPL/sync",json=payload)

    print_response(response)
    if response.status_code >= 400:
        raise Exception("Asset sync fallita")

    print("\n=== TEST GET ASSET ===")

    response = requests.get(f"{BASE_URL}/assets/AAPL")

    print_response(response)
    if response.status_code >= 400:
        raise Exception("Get asset fallita")
    
    print("\n=== TEST GET ASSET DETAILS ===")
    
    qs = "start_date=2026-01-01&end_date=2026-01-31"
    response = requests.get(f"{BASE_URL}/assets/AAPL/details?{qs}")

    print_response(response)
    if response.status_code >= 400:
        raise Exception("Get asset details fallita")
        
    print("\n=== TEST LIST ASSETS ===")

    response = requests.get(f"{BASE_URL}/assets/")

    print_response(response)
    if response.status_code >= 400:
        raise Exception("List assets fallita")
        
    print("\n=== TEST SYNC TRACKED ASSETS ===")

    response = requests.put(f"{BASE_URL}/assets/sync-tracked")

    print_response(response)
    if response.status_code >= 400:
        raise Exception("Sync tracked assets fallita")

    print("\n=== TEST DELETE ASSET ===")

    response = requests.delete(f"{BASE_URL}/assets/AAPL")
    print_response(response)

    if response.status_code >= 400 and response.status_code != 409:
        raise Exception("Delete asset fallita")
        
    print("\n=== TEST API ASSETS COMPLETATO ===")

finally:
    stop_server(server)