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