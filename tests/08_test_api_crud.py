import subprocess
import sys
import time
import requests

BASE_URL = "http://127.0.0.1:8000"


def wait_for_server(timeout=15):
    start = time.time()

    while time.time() - start < timeout:

        try:

            response = requests.get(f"{BASE_URL}/")

            if response.status_code == 200:
                return True

        except Exception:
            pass

        time.sleep(1)

    return False


def print_response(response):
    print(f"Status: {response.status_code}")

    try:
        print(response.json())
    except Exception:
        print(response.text)


if __name__ == "__main__":
    print("\n=== AVVIO UVICORN ===\n")

    server = subprocess.Popen( [sys.executable, "-m", "uvicorn", "api.app:app"] )

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
            raise Exception("Sync fallita")

        print("\n=== TEST GET ASSET ===")

        response = requests.get(f"{BASE_URL}/assets/AAPL")

        print_response(response)

        if response.status_code >= 400:
            raise Exception("Get asset fallita")

        asset = response.json()

        asset_id = asset["id"]

        print("\n=== TEST ANALYSIS ===")

        response = requests.get(f"{BASE_URL}/analysis/AAPL")

        print_response(response)

        if response.status_code >= 400:
            raise Exception("Analysis fallita")

        print("\n=== TEST WATCHLIST ADD ===")

        response = requests.post(f"{BASE_URL}/portfolio/watchlist/AAPL")

        print_response(response)

        if response.status_code >= 400:
            raise Exception("Watchlist add fallita")

        print("\n=== TEST WATCHLIST GET ===")

        response = requests.get( f"{BASE_URL}/portfolio/watchlist")

        print_response(response)

        if response.status_code >= 400:
            raise Exception("Watchlist get fallita")

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

        print("\n=== TEST WATCHLIST DELETE ===")

        response = requests.delete(f"{BASE_URL}/portfolio/watchlist/AAPL")

        print_response(response)

        if response.status_code >= 400:
            raise Exception("Watchlist delete fallita")

        print(
            "\n=== TEST API COMPLETATO ==="
        )

    finally:
        print("\n=== ARRESTO UVICORN ===")
        server.terminate()

        try:
            server.wait(timeout=5)
        except Exception:
            server.kill()

        print("Server arrestato")