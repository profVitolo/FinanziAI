from datetime import datetime
from fastapi import APIRouter, HTTPException, Body

from data_engine.data_engine import DataEngine
from data_manager.portfolio_data_manager import PortfolioDataManager
from data_manager.asset_data_manager import AssetDataManager

router = APIRouter(prefix="/portfolio", tags=["Portfolio"])

data_engine = DataEngine()
portfolio_data_manager = PortfolioDataManager()
asset_data_manager = AssetDataManager()

@router.get("/")
def get_portfolio():
    positions = (portfolio_data_manager.get_all_positions())

    return positions
	
@router.get("/analysis")
def analyze_portfolio():
    result = (data_engine.analyze_portfolio())

    if result is None:
        raise HTTPException(status_code=404, detail="Portfolio is empty")

    return result
	
@router.post("/transactions")
def create_transaction(
    asset_id: int = Body(...),
    transaction_type: str = Body(...),
    quantity: float = Body(...),
    price: float = Body(...),
    commission: float = Body(0)
):
    portfolio_data_manager.create_transaction(
        asset_id=asset_id,
        transaction_date=datetime.now().date(),
        transaction_type=transaction_type,
        quantity=quantity,
        price=price,
        commission=commission
    )

    return {"status": "success"}
    
@router.get("/watchlist")
def get_watchlist():
    watchlist = (portfolio_data_manager.get_watchlist())

    result = []

    for item in watchlist:
        asset_id = item[1]

        asset = (asset_data_manager.get_asset_by_id(asset_id))

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
    asset = (asset_data_manager.get_asset_by_symbol(symbol.upper()))

    if asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")

    portfolio_data_manager.add_to_watchlist(asset[0])

    return {
        "status": "success",
        "symbol": symbol.upper()
    }
    
@router.delete("/watchlist/{symbol}")
def remove_from_watchlist(symbol: str):
    asset = (asset_data_manager.get_asset_by_symbol(symbol.upper()))

    if asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")

    portfolio_data_manager.remove_from_watchlist(asset[0])

    return {
        "status": "success",
        "symbol": symbol.upper()
    }
    
