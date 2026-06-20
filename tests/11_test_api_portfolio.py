from pathlib import Path
import requests
import sys
from api_test_utils import *

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

server = start_server_if_needed()

print_title("=== TEST API PORTFOLIO ===")
    
try:
    print("\n=== GET PORTFOLIO ===")

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
    stop_server(server)