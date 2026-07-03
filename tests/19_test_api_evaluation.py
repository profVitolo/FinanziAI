from pathlib import Path
import requests
import sys

from test_utils import *

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

server = start_server_if_needed()

print_title("=== TEST API EVALUATION ===")

try:
    print("\n=== EVALUATE ASSET ===")
    response = requests.get(f"{BASE_URL}/evaluation/assets/AAPL")
    data = response.json()
    
    assert "messages" in data
    assert "summary" in data
    
    print_response(response)

    if response.status_code >= 400:
        raise Exception("Asset evaluation fallita")

    print("\n=== EVALUATE PORTFOLIO ===")
    response = requests.get(f"{BASE_URL}/evaluation/portfolio")
    data = response.json()

    assert "messages" in data
    assert "summary" in data
    
    print_response(response)

    if response.status_code >= 400:
        raise Exception("Portfolio evaluation fallita")

    print("\n=== EVALUATE FULL ===")
    response = requests.get(f"{BASE_URL}/evaluation/full")
    data = response.json()
    
    assert "portfolio" in data
    assert "assets" in data
    assert isinstance(data["assets"], list)
    
    print_response(response)

    if response.status_code >= 400:
        raise Exception("Full evaluation fallita")

    print("\n=== TEST API EVALUATION COMPLETATO ===")

finally:
    stop_server(server)