from pathlib import Path
import requests
import sys
from api_test_utils import *

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

server = start_server_if_needed()

try:
    
    print("\n=== TEST ANALYSIS ===")

    response = requests.get(f"{BASE_URL}/analysis/AAPL")

    print_response(response)
    if response.status_code >= 400:
        raise Exception("Analysis fallita")

    print("\n=== TEST API ANALYSIS COMPLETATO ===")

finally:
    stop_server(server)