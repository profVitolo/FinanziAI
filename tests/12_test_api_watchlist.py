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

        print("\n=== TEST WATCHLIST ADD ===")

        response = requests.post(f"{BASE_URL}/portfolio/watchlist/AAPL")

        print_response(response)
        if response.status_code >= 400:
            raise Exception("Watchlist add fallita")

        print("\n=== TEST WATCHLIST GET ===")

        response = requests.get(f"{BASE_URL}/portfolio/watchlist")

        print_response(response)
        if response.status_code >= 400:
            raise Exception("Watchlist get fallita")

        print("\n=== TEST WATCHLIST DELETE ===")

        response = requests.delete(f"{BASE_URL}/portfolio/watchlist/AAPL")

        print_response(response)
        if response.status_code >= 400:
            raise Exception("Watchlist delete fallita")

        print("\n=== TEST API WATCHLIST COMPLETATO ===")

    finally:
        print("\n=== ARRESTO UVICORN ===")

        server.terminate()

        try:
            server.wait(timeout=5)
        except Exception:
            server.kill()

        print("Server arrestato")