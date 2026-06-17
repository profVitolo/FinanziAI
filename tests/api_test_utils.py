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
        if isinstance(item, dict):
            print("-" * 40)
            for key, value in item.items():
                print(f"{key}: {value}")
        else:
            print(item)
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
