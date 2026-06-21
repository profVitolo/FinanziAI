import os
import sys
import subprocess
import requests
import time
import json
import sqlite3 

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
        
    
def print_title(title):
    str_len = len(title)

    end = ""
    char = "="
    if str_len % 2:
        str_len += 1
        end = char
    
    tot_len = str_len + 8
    
    print(f"\n\n{char * (tot_len * 2)}")
    print(f"\n{char * int(tot_len / 2)}{char * 3} {title} {char * 3}{char * int(tot_len / 2)}{end}")
    print(f"\n{char * (tot_len * 2)}\n")
 
def print_value(title, value):
    if title != "":
        print(f"\n=== {title} ===")
    if value is None:
        print("None")
    else:
        print(value)

def print_dict(title, data):
    if title != "":
        print(f"\n=== {title} ===")
    if data is None:
        print("None")
        return
    
    for key, value in data.items():
        if isinstance(value, dict):
            print(f"{key}: {value}")
        else:
            print_result(key, value)

def print_json(title, data):
    if title:
        print(f"\n=== {title} ===")

    if data is None:
        print("None")
        return

    print(json.dumps(data, indent=4, ensure_ascii=False))
    
def print_collection(title, items):
    if title != "":
        print(f"\n=== {title} ===")

    if not items:
        print("Empty")
        return

    for item in items:
        if isinstance(item, sqlite3.Row):
            print_json("", dict(item))
        else:
            print(item)
    
def print_result(title, value):    
    if isinstance(value, dict):
        print_dict(title, value)
    elif isinstance(value, (list, tuple)):
        print_collection(title, value)
    elif isinstance(value, sqlite3.Row):
        print_json(title, dict(value))
    else:
        print_value(title, value)
