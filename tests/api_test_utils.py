import os
import sys
import subprocess
import requests
import time

BASE_URL = "http://127.0.0.1:8000"


def wait_for_server(timeout=10):
    start = time.time()

    while time.time() - start < timeout:
        try:
            response = requests.get(f"{BASE_URL}/info")
            if response.status_code < 500:
                return True
        except Exception:
            pass

        time.sleep(0.5)

    return False


def start_server_if_needed():
    if os.getenv("FINANZIAI_TEST_RUNNER") == "1":
        return None

    print("\n=== AVVIO UVICORN ===\n")

    server = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "api.app:app"]
    )

    if not wait_for_server():
        server.kill()
        raise RuntimeError("Server non raggiungibile")

    print("Server pronto")

    return server


def stop_server(server):
    if server is None:
        return

    print("\n=== ARRESTO UVICORN ===")

    server.terminate()

    try:
        server.wait(timeout=5)
    except Exception:
        server.kill()

    print("Server arrestato")

def print_response(response):
    print(f"Status: {response.status_code}")

    try:
        print(response.json())
    except Exception:
        print(response.text)
        
    
def print_value(title, value):
    print(f"\n=== {title} ===")
    if value is None:
        print("None")
    else:
        print(value)

def print_dict(title, data):
    print(f"\n=== {title} ===")
    if data is None:
        print("None")
        return

    for key, value in data.items():
        print(f"{key}: {value}")

def print_collection(title, items):
    print(f"\n=== {title} ===")

    if not items:
        print("Empty")
        return

    for item in items:
        print(item)
    
def print_result(title, value):    
    if isinstance(value, dict):
        print_dict(title, value)
    elif isinstance(value, (list, tuple)):
        print_collection(title, value)
    else:
        print_value(title, value)
