from fastapi import APIRouter, Request
from config import BASE_CURRENCY

from services.database_service import DatabaseService
from api.schemas import DatabaseRequest

router = APIRouter(prefix="/info", tags=["Info"])

@router.get("")
def get_info(request: Request):
    app = request.app
    service = DatabaseService()
    
    return {
        "application": app.title,
        "description": app.description,
        "version": app.version,
        "base_currency": BASE_CURRENCY,
        "database": service.get_current_vault()
    }
    
@router.get("/databases")
def get_databases():
    service = DatabaseService()

    return {
        "selected": service.get_current_vault(),
        "databases": service.list_vaults()
    }
    
@router.post("/database/create")
def create_database(request: DatabaseRequest):
    service = DatabaseService()

    return {
        "database": service.create_vault(request.db_name)
    }
    
@router.post("/database/select")
def select_database(request: DatabaseRequest):
    service = DatabaseService()
    service.set_vault(request.db_name)

    return {
        "database": service.get_current_vault()
    }