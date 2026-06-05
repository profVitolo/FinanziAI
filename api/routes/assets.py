from fastapi import APIRouter, HTTPException

from config import DB_PATH
from services.data_service import DataService
from data_manager.asset_data_manager import AssetDataManager

router = APIRouter(prefix="/assets", tags=["Assets"])

data_service = DataService(DB_PATH)
asset_data_manager = AssetDataManager(DB_PATH)


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
def sync_asset(symbol: str):
    try:

        result = data_service.sync_asset(symbol.upper())

        return {
            "status": "success",
            "symbol": symbol.upper(),
            "result": result
        }

    except Exception as exc:

        raise HTTPException(status_code=500, detail=str(exc))
        
        