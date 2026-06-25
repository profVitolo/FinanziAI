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

@router.get("/watchlist")
def get_watchlist():
    portfolio_service = PortfolioService()
    data_service = DataService()
    try:
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
    finally:
        portfolio_service.close()
        data_service.close()
    
@router.post("/watchlist/{symbol}")
def add_to_watchlist(symbol: str):
    data_service = DataService()
    portfolio_service = PortfolioService()
    try:
        asset = (data_service.get_asset_by_symbol(symbol.upper()))

        if asset is None:
            raise HTTPException(status_code=404, detail="Asset not found")

        portfolio_service.add_to_watchlist(asset["id"])
        
        return {
            "status": "success",
            "symbol": symbol.upper()
        }
    finally:
        portfolio_service.close()
        data_service.close()
    
@router.delete("/watchlist/{symbol}")
def remove_from_watchlist(symbol: str):
    data_service = DataService()
    portfolio_service = PortfolioService()
    try:        
        asset = (data_service.get_asset_by_symbol(symbol.upper()))

        if asset is None:
            raise HTTPException(status_code=404, detail="Asset not found")

        portfolio_service.remove_from_watchlist(asset[0])

        return {
            "status": "success",
            "symbol": symbol.upper()
        }
    finally:
        portfolio_service.close()
        data_service.close()
    
