from typing import Optional
from fastapi import APIRouter, HTTPException

from config import DB_PATH
from data_engine.data_engine import DataEngine

router = APIRouter(prefix="/analysis", tags=["Analysis"])

data_engine = DataEngine(DB_PATH)


@router.get("/{symbol}")
def analyze_asset(symbol: str):
    result = data_engine.analyze_asset(symbol.upper())
    
    if result is None:

        raise HTTPException(status_code=404, detail="Asset not found or no price data available")

    return result
    
@router.get("/{symbol}")
def analyze_asset(symbol: str, start_date: Optional[str] = None, end_date: Optional[str] = None):
    result = data_engine.analyze_asset(symbol.upper(), start_date=start_date, end_date=end_date)

    if result is None:

        raise HTTPException(status_code=404, detail="Asset not found or no price data available")

    return result
    