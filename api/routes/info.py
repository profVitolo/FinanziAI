from fastapi import APIRouter, Request
from config import BASE_CURRENCY

from services.database_service import DatabaseService
from api.schemas import DatabaseRequest

router = APIRouter(prefix="/info", tags=["Info"])

@router.get("")
def get_info(request: Request):
    service = DatabaseService()
    try:
        app = request.app
        
        return {
            "application": app.title,
            "description": app.description,
            "version": app.version,
            "base_currency": BASE_CURRENCY,
            "database": service.get_current_vault()
        }
    finally:
        service.close()
    
@router.get("/databases")
def get_databases():
    service = DatabaseService()
    try:
        return {
            "selected": service.get_current_vault(),
            "databases": service.list_vaults()
        }
    finally:
        service.close()
    
@router.post("/database/create")
def create_database(request: DatabaseRequest):
    service = DatabaseService()
    try:
        return {
            "database": service.create_vault(request.db_name)
        }
    finally:
        service.close()
    
@router.post("/database/select")
def select_database(request: DatabaseRequest):
    service = DatabaseService()
    
    try:
        service.set_vault(request.db_name)
        return {
            "database": service.get_current_vault()
        }
    finally:
        service.close()
    
@router.delete("/database/{db_name}")
def delete_database(db_name: str):
    service = DatabaseService()
    try:
        return {
            "database": service.delete_vault(db_name)
        }
    finally:
        service.close()