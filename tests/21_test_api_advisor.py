from pathlib import Path
import requests
import sys

from test_utils import *

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

server = start_server_if_needed()

print_title("=== TEST API ADVISOR ===")

try:

    print("\n=== INVESTOR PROFILES ===")

    response = requests.get(f"{BASE_URL}/advisor/investor-profiles")

    data = response.json()

    assert isinstance(data, list)
    assert len(data) > 0

    for profile in data:
        assert "value" in profile
        assert "label" in profile

    print_response(response)

    if response.status_code >= 400:
        raise Exception("Investor profiles fallita")


    print("\n=== ADVISE ===")

    response = requests.post(
        f"{BASE_URL}/advisor/advise",
        json={
            "prompt": "Analizza il mio portafoglio e dammi tre suggerimenti.",
            "investor_profile": "balanced",
        },
    )

    data = response.json()

    print_response(response)

    if response.status_code >= 400:
        raise Exception("Advisor fallito")


    print("\n=== TEST API ADVISOR COMPLETATO ===")

finally:
    stop_server(server)