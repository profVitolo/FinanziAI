from pathlib import Path
import requests
import sys
from api_test_utils import *

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

server = start_server_if_needed()

print_title("=== TEST API TRNASACTION ===")

try:

    print("\n=== RECUPERO ASSET ===")

    response = requests.get(f"{BASE_URL}/assets/AAPL")

    print_response(response)

    if response.status_code >= 400:
        raise Exception("Get asset fallita")

    asset_id = response.json()["id"]

    print("\n=== CREATE TRANSACTION ===")
    
    payload = {
            "asset_id": asset_id,
            "operation_type": "buy",
            "quantity": 1,
            "price": 100,
            "fees": 0,
            "transaction_date": "2026-06-15"
    }
    response = requests.post(f"{BASE_URL}/transactions/",json=payload)

    print_response(response)

    if response.status_code >= 400:
        raise Exception(f"Transaction create fallita")

    transaction_id = response.json()["transaction_id"]

    print("\n=== GET TRANSACTIONS ===")

    response = requests.get(f"{BASE_URL}/transactions/")

    print_response(response)

    if response.status_code >= 400:
        raise Exception("Transactions get fallita")

    print("\n=== UPDATE TRANSACTION ===")

    payload = {
            "asset_id": asset_id,
            "operation_type": "buy",
            "quantity": 2,
            "price": 120,
            "fees": 1,
            "transaction_date": "2026-06-15"
    }
    response = requests.put(f"{BASE_URL}/transactions/{transaction_id}", json=payload)

    print_response(response)

    if response.status_code >= 400:
        raise Exception("Transaction update fallita")

    print("\n=== GET TRANSACTIONS AFTER UPDATE ===")

    response = requests.get(f"{BASE_URL}/transactions/")

    print_response(response)

    if response.status_code >= 400:
        raise Exception("Transactions get fallita")

    print("\n=== DELETE TRANSACTION ===")

    response = requests.delete(f"{BASE_URL}/transactions/{transaction_id}")

    print_response(response)

    if response.status_code >= 400:
        raise Exception("Transaction delete fallita")

    print("\n=== GET TRANSACTIONS AFTER DELETE ===")

    response = requests.get(f"{BASE_URL}/transactions/")

    print_response(response)

    if response.status_code >= 400:
        raise Exception("Transactions get fallita")

    print("\n=== TEST API TRANSACTIONS COMPLETATO ===")

finally:
    stop_server(server)