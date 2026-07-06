from fastapi import APIRouter, HTTPException

from data_engine.data_engine import DataEngine
from evaluation_engine.evaluation_engine import EvaluationEngine

router = APIRouter(
    prefix="/evaluation",
    tags=["Evaluation"]
)

@router.get("/portfolio")
def evaluate_portfolio():
    data_engine = DataEngine()

    try:
        portfolio = data_engine.analyze_portfolio()

        if portfolio is None:
            raise HTTPException(status_code=404, detail="Portfolio is empty")

        return EvaluationEngine.evaluate_portfolio(portfolio)
    finally:
        data_engine.close()
		

@router.get("/full")
def evaluate_portfolio_full():
    data_engine = DataEngine()
    
    try:
        analysis = data_engine.analyze_portfolio_full()

        if analysis is None:
            raise HTTPException(status_code=404, detail="Portfolio is empty")

        return {
            "portfolio": EvaluationEngine.evaluate_portfolio(
                analysis.portfolio
            ),
            "assets": [
                EvaluationEngine.evaluate_asset(asset)
                for asset in analysis.assets
            ]
        }
    finally:
        data_engine.close()

@router.get("/assets/{symbol}")
def evaluate_asset(symbol: str, start_date: str | None = None, end_date: str | None = None):
    data_engine = DataEngine()

    try:
        asset = data_engine.analyze_asset(
            symbol.upper(),
            start_date=start_date,
            end_date=end_date,
        )

        if asset is None:
            raise HTTPException(status_code=404, detail="Asset not found")

        return EvaluationEngine.evaluate_asset(asset)
    finally:
        data_engine.close()