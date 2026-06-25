from typing import Optional
from fastapi import APIRouter, HTTPException

from data_engine.data_engine import DataEngine

router = APIRouter(prefix="/analysis", tags=["Analysis"])

@router.get("/{symbol}")
def analyze_asset(symbol: str, start_date: Optional[str] = None, end_date: Optional[str] = None):
    data_engine = DataEngine()
    try:
        result = data_engine.analyze_asset(symbol.upper(), start_date=start_date, end_date=end_date)

        if result is None:
            raise HTTPException(status_code=404, detail="Asset not found or no price data available")

        return result
    finally:
        data_engine.close()