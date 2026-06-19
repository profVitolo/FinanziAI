from pathlib import Path
import requests
import sys
from api_test_utils import *

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

server = start_server_if_needed()

try:
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
    stop_server(server)