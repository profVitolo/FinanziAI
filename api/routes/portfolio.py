from datetime import datetime, date
from fastapi import APIRouter, HTTPException, Body, Depends

from data_engine.data_engine import DataEngine
from services.data_service import DataService
from services.portfolio_service import PortfolioService
from api.schemas import TransactionCreate

router = APIRouter(prefix="/portfolio", tags=["Portfolio"])


@router.get("/")
def get_portfolio():
    portfolio_service = PortfolioService()
    try:
        positions = (portfolio_service.get_all_positions())
        
        return positions
    finally:
        portfolio_service.close()
	
@router.get("/analysis")
def analyze_portfolio():
    data_engine = DataEngine()
    try:
        result = (data_engine.analyze_portfolio())
        
        if result is None:
            raise HTTPException(status_code=404, detail="Portfolio is empty")

        return result
    finally:
        data_engine.close()
