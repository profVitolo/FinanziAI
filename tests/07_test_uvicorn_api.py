import subprocess
import sys
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


if __name__ == "__main__":
    print("\n=== AVVIO UVICORN ===\n")

    server = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "api.app:app"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    try:
        if not wait_for_server():

            print("Server non raggiungibile")

            server.kill()
            sys.exit(1)

        print("Server avviato correttamente")

        failures = []

        endpoints = [
            ("GET", "/"),
            ("GET", "/assets"),
            ("GET", "/portfolio"),
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

        print("\n=== ARRESTO UVICORN ===")
        server.terminate()

        try:
            server.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server.kill()

        print("Server arrestato")