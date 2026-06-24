from pathlib import Path
import requests
import sys
from api_test_utils import *

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

server = start_server_if_needed()
print_title("=== TEST API DATABASE ===")

try:
    print("\n=== TEST GET DATABASES ===")

    response = requests.get(f"{BASE_URL}/info/databases")

    print_response(response)

    if response.status_code >= 400:
        raise Exception("Get databases fallita")
        
    print("\n=== TEST CREATE DATABASE ===")

    payload = {"db_name": "test_vault"}
    response = requests.post(f"{BASE_URL}/info/database/create", json=payload)

    print_response(response)

    if response.status_code >= 400:
        raise Exception("Create database fallita")
        
    print("\n=== TEST DATABASE PRESENT IN LIST ===")

    response = requests.get(f"{BASE_URL}/info/databases")
    print_response(response)

    databases = response.json()["databases"]

    if "test_vault.db" not in databases:
        raise Exception("Database non trovato")
    else:
        print_result("DB founded", databases)
        
    print("\n=== TEST SELECT DATABASE ===")

    payload = {"db_name": "test_vault"}
    response = requests.post(f"{BASE_URL}/info/database/select",json=payload)
    print_response(response)

    if response.status_code >= 400:
        raise Exception("Select database fallita")
    
    print("\n=== TEST CURRENT DATABASE ===")

    response = requests.get(f"{BASE_URL}/info/databases")
    print_response(response)
    selected = response.json()["selected"]

    if selected != "test_vault.db":
        raise Exception("Database corrente errato")

    print("\n=== TEST ASSET SYNC ===")
    
    payload = {"start_date": "2026-01-01"}
    response = requests.post(f"{BASE_URL}/assets/SCPX/sync",json=payload)

    print_response(response)
    if response.status_code >= 400:
        raise Exception("Asset sync fallita")

    print("\n=== TEST GET ASSET ===")

    response = requests.get(f"{BASE_URL}/assets/SCPX")

    print_response(response)
    if response.status_code >= 400:
        raise Exception("Get asset fallita")
    
    print("\n=== TEST SELECT OLD DATABASE ===")

    payload = {"db_name": "vault"}
    response = requests.post(f"{BASE_URL}/info/database/select",json=payload)
    print_response(response)

    if response.status_code >= 400:
        raise Exception("Select database fallita")
        
    print("\n=== TEST GET ASSET ===")

    response = requests.get(f"{BASE_URL}/assets/")

    print("Should be 'Not found'")
    print_response(response)
        
finally:
    stop_server(server)