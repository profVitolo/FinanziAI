from datetime import datetime, date
from fastapi import APIRouter, HTTPException, Body, Depends

from data_engine.data_engine import DataEngine
from services.data_service import DataService
from services.portfolio_service import PortfolioService
from api.schemas import TransactionCreate

router = APIRouter(prefix="/portfolio", tags=["Portfolio"])

data_engine = DataEngine()
data_service = DataService()
portfolio_service = PortfolioService()

@router.get("/")
def get_portfolio():
    positions = (portfolio_service.get_all_positions())

    return positions
	
@router.get("/analysis")
def analyze_portfolio():
    result = (data_engine.analyze_portfolio())

    if result is None:
        raise HTTPException(status_code=404, detail="Portfolio is empty")

    return result

@router.get("/watchlist")
def get_watchlist():
    watchlist = (portfolio_service.get_watchlist())

    result = []

    for item in watchlist:
        asset_id = item[1]

        asset = (data_service.get_asset_by_id(asset_id))

        if asset is None:
            continue

        result.append({
            "watchlist_id": item[0],
            "asset_id": asset[0],
            "symbol": asset[1],
            "name": asset[2],
            "type": asset[3],
            "currency": asset[4],
            "exchange": asset[5]
        })

    return result
    
@router.post("/watchlist/{symbol}")
def add_to_watchlist(symbol: str):
    asset = (data_service.get_asset_by_symbol(symbol.upper()))

    if asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")

    portfolio_service.add_to_watchlist(asset["id"])
    
    return {
        "status": "success",
        "symbol": symbol.upper()
    }
    
@router.delete("/watchlist/{symbol}")
def remove_from_watchlist(symbol: str):
    asset = (data_service.get_asset_by_symbol(symbol.upper()))

    if asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")

    portfolio_service.remove_from_watchlist(asset[0])

    return {
        "status": "success",
        "symbol": symbol.upper()
    }
    
