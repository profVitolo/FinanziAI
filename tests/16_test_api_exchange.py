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
                "start_date": "2026-01-01",
                "end_date": "2026-01-31"
            }
        )

        print_response(response)

        if response.status_code >= 400:
            raise Exception("Sync range fallita")

        print("\n=== TEST API EXCHANGE COMPLETATO ===")

    finally:
        print("\n=== ARRESTO UVICORN ===")
        server.terminate()

        try:
            server.wait(timeout=5)
        except Exception:
            server.kill()

        print("Server arrestato")