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

        print("\n=== TEST API ASSETS COMPLETATO ===")

    finally:
        print("\n=== ARRESTO UVICORN ===")
        server.terminate()

        try:
            server.wait(timeout=5)
        except Exception:
            server.kill()
        print("Server arrestato")