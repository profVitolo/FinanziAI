from fastapi import APIRouter, HTTPException

from services.data_service import DataService
from services.portfolio_service import PortfolioService
from api.schemas import AssetSync

router = APIRouter(prefix="/assets", tags=["Assets"])


@router.get("/")
def list_assets():
    data_service = DataService()
    try:
        assets = data_service.get_all_assets()
        
        return [dict(asset) for asset in assets]
    finally:
        data_service.close()

@router.put("/sync-tracked")
def sync_tracked_assets():
    data_service = DataService()
    portfolio_service = PortfolioService()
    
    try:
        tracked_assets = portfolio_service.get_tracked_assets()
        result = data_service.sync_tracked_assets(tracked_assets)

        return {
            "status": "success",
            "assets_processed": len(tracked_assets),
            "results": result
        }

    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    finally:
        data_service.close()
        portfolio_service.close()
        
@router.get("/{symbol}/details")
def get_asset_details(symbol: str, start_date: str | None = None, end_date: str | None = None):
    data_service = DataService()

    try:
        asset_details = data_service.get_asset_details(
            symbol.upper(),
            start_date=start_date,
            end_date=end_date
        )

        if asset_details is None:
            raise HTTPException(status_code=404, detail="Asset not found")

        return {
            "asset": dict(asset_details["asset"]),
            "prices": [dict(price) for price in asset_details["prices"]]
        }
    finally:
        data_service.close()
        
@router.post("/{symbol}/sync")
def sync_asset(symbol: str, payload: AssetSync):
    data_service = DataService()
    
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
    finally:
        data_service.close()
        
@router.delete("/{symbol}")
def delete_asset(symbol: str):
    data_service = DataService()

    try:
        result = data_service.delete_asset_by_symbol(symbol.upper())

        if not result["deleted"]:
            raise HTTPException(status_code=404,detail="Asset not found")

        return result

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(status_code=500,detail=str(exc))
    finally:
        data_service.close()
        
@router.get("/{symbol}")
def get_asset(symbol: str):
    data_service = DataService()
    
    try:
        asset = data_service.get_asset_by_symbol(symbol.upper())

        if asset is None:
            raise HTTPException(status_code=404, detail="Asset not found")

        return dict(asset)
    finally:
        data_service.close()