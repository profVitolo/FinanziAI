import subprocess
import sys
import time
import requests

from api_test_utils import (BASE_URL, wait_for_server, print_response)


def test_endpoint(method, path):
    url = f"{BASE_URL}{path}"

    print(f"\n=== {method} {path} ===")

    if method == "GET":
        response = requests.get(url)

    elif method == "POST":
        response = requests.post(url)

    elif method == "DELETE":
        response = requests.delete(url)

    else:
        raise ValueError(method)

    print("Status:", response.status_code)

    try:
        print("Response:", response.json())
    except Exception:
        print("Response:", response.text)
        
    return response.status_code


server = None

if __name__ == "__main__":
    print("\n=== AVVIO UVICORN ===\n")

    server = subprocess.Popen([sys.executable, "-m", "uvicorn", "api.app:app"])
    
    if not wait_for_server():
        print("Server non raggiungibile")
        sys.exit(1)

    print("Server pronto")

try:
    if not wait_for_server():

        print("Server non raggiungibile")

        server.kill()
        sys.exit(1)
        
    info = requests.get(f"{BASE_URL}/info").json()
    print(f"FinanziAI {info['version']} avviato correttamente")
    
    failures = []

    endpoints = [
        ("GET", "/info"),
        ("GET", "/assets/"),
        ("GET", "/portfolio/"),
        ("GET", "/portfolio/analysis"),
    ]

    for method, path in endpoints:
        status = test_endpoint(method, path)

        if status >= 400:
            failures.append(path)

    print("\n=== REPORT ===")

    if failures:
        print("Endpoint falliti:")

        for endpoint in failures:
            print("-", endpoint)

        sys.exit(1)

    print("Tutti gli endpoint testati correttamente")

finally:
    if server:
        print("\n=== ARRESTO UVICORN ===")
        server.terminate()

        try:
            server.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server.kill()

        print("Server arrestato")