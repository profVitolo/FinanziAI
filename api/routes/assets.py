from fastapi import APIRouter, HTTPException

from config import DB_PATH
from services.data_service import DataService
from services.portfolio_service import PortfolioService
from data_manager.asset_data_manager import AssetDataManager
from api.schemas import AssetSync

router = APIRouter(prefix="/assets", tags=["Assets"])
    
data_service = DataService(DB_PATH)
portfolio_service = PortfolioService()
asset_data_manager = AssetDataManager(DB_PATH)

@router.get("/")
def list_assets():
    assets = asset_data_manager.get_all_assets()
    
    return [
        {
            "id": asset[0],
            "symbol": asset[1],
            "name": asset[2],
            "type": asset[3],
            "currency": asset[4],
            "exchange": asset[5]
        }
        for asset in assets
    ]


@router.get("/{symbol}")
def get_asset(symbol: str):
    asset = asset_data_manager.get_asset_by_symbol(symbol.upper())

    if asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")

    return {
        "id": asset[0],
        "symbol": asset[1],
        "name": asset[2],
        "type": asset[3],
        "currency": asset[4],
        "exchange": asset[5]
    }

    
@router.post("/{symbol}/sync")
def sync_asset(symbol: str, payload: AssetSync):
    try:
        result = data_service.sync_asset(
            symbol.upper(), 
            start_date=payload.start_date, 
            end_date=payload.end_date
        )

        return {
            "status": "success",
            "symbol": symbol.upper(),
            "result": result
        }

    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
 
 
@router.put("/sync-tracked")
def sync_tracked_assets():
    try:
        tracked_assets = portfolio_service.get_tracked_assets()
        result = data_service.sync_assets(tracked_assets)

        return {
            "status": "success",
            "assets_processed": len(tracked_assets),
            "results": result
        }

    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))