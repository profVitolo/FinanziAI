from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

import sys
sys.path.insert(0, str(ROOT_DIR))

import subprocess
import requests

from api_test_utils import (BASE_URL, wait_for_server, print_response)

if __name__ == "__main__":
    print("\n=== AVVIO UVICORN ===\n")

    server = subprocess.Popen([sys.executable, "-m", "uvicorn", "api.app:app"])

    try:
        if not wait_for_server():
            print("Server non raggiungibile")
            sys.exit(1)

        print("Server pronto")

        print("\n=== RECUPERO ASSET ===")

        response = requests.get(f"{BASE_URL}/assets/AAPL")

        print_response(response)
        if response.status_code >= 400:
            raise Exception("Get asset fallita")

        asset_id = response.json()["id"]

        print("\n=== TEST TRANSACTION CREATE ===")

        response = requests.post(
            f"{BASE_URL}/portfolio/transactions",
            json={
                "asset_id": asset_id,
                "operation_type": "buy",
                "quantity": 1,
                "price": 100,
                "fees": 0
            }
        )

        print_response(response)
        if response.status_code >= 400:
            raise Exception("Transaction fallita")

        print("\n=== TEST GET TRANSACTIONS ===")

        response = requests.get(f"{BASE_URL}/portfolio/transactions")

        print_response(response)
        if response.status_code >= 400:
            raise Exception("Transactions get fallita")

        print("\n=== TEST PORTFOLIO ===")

        response = requests.get(f"{BASE_URL}/portfolio/")

        print_response(response)
        if response.status_code >= 400:
            raise Exception("Portfolio get fallita")

        print("\n=== TEST PORTFOLIO ANALYSIS ===")

        response = requests.get(f"{BASE_URL}/portfolio/analysis")

        print_response(response)
        if response.status_code >= 400:
            raise Exception("Portfolio analysis fallita")

        print("\n=== TEST API PORTFOLIO COMPLETATO ===")

    finally:
        print("\n=== ARRESTO UVICORN ===")

        server.terminate()

        try:
            server.wait(timeout=5)
        except Exception:
            server.kill()

        print("Server arrestato")