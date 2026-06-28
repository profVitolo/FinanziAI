import subprocess
import sys
import time
import requests

from test_utils import *


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

server = start_server_if_needed()

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
    stop_server(server)