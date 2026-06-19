from fastapi import APIRouter, Request
from config import BASE_CURRENCY

router = APIRouter(prefix="/info", tags=["Info"])

@router.get("")
def get_info(request: Request):
    app = request.app

    return {
        "application": app.title,
        "description": app.description,
        "version": app.version,
        "base_currency": BASE_CURRENCY
    }