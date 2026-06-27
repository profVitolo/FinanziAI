from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from api_test_utils import *
from evaluation_engine.evaluation_engine import EvaluationEngine
from data_engine.data_engine import DataEngine
from database.database_manager import DatabaseManager

def call_evaluation(asset_analysis=None, portfolio=None):
    if asset_analysis is not None:
        if not isinstance(asset_analysis, (list, tuple)):
            asset_analysis = [asset_analysis]
        for single_asset_analysis in asset_analysis:
            asset_result = EvaluationEngine.evaluate_asset(single_asset_analysis)
            print_result("ASSET EVALUATION", asset_result)

    if portfolio is not None:
        portfolio_result = EvaluationEngine.evaluate_portfolio(portfolio)
        print_result("PORTFOLIO EVALUATION", portfolio_result)

print_title("=== TEST EVALUATION ENGINE ===")

asset_analysis = {
    "asset": {
        "id": 1,
        "symbol": "NVDA",
        "name": "NVIDIA Corporation",
        "type": "EQUITY",
        "currency": "USD",
        "exchange": "NMS",
        "sector": "Technology",
        "industry": "Semiconductors",
        "country": "United States",
        "market_cap": 3_500_000_000_000,
        "beta": 1.82,
        "website": "https://www.nvidia.com"
    },
    "period": {
        "start": "2025-01-01",
        "end": "2026-01-01"
    },
    "market_data": {
        "records": 252,
        "last_close": 145.25
    },
    "indicators": {
        "sma20": 140.3,
        "sma50": 132.8,
        "rsi": 76.4,
        "daily_volatility": 0.031,
        "annualized_volatility": 0.49,
        "period_range": 112.7
    },
    "analysis": {
        "trend": "bullish",
        "volatility_level": "high"
    }
}

portfolio = {
    "base_currency": "EUR",
    "portfolio_value": 100000,
    "positions": [
        {
            "asset_id": 1,
            "symbol": "NVDA",
            "name": "NVIDIA Corporation",
            "type": "EQUITY",
            "sector": "Technology",
            "industry": "Semiconductors",
            "country": "United States",
            "market_cap": 3_500_000_000_000,
            "beta": 1.82,

            "quantity": 388.0,
            "currency": "USD",
            "avg_price": 120.00,
            "market_price": 145.10,
            "market_value": 56300.0,
            "market_value_base": 56300.0,

            "performance": {
                "cost_basis": 46560.0,
                "market_value": 56300.0,
                "pnl": 9740.0,
                "pnl_percent": 20.92,
                "cost_basis_base": 46560.0,
                "pnl_base": 9740.0
            }
        },
        {
            "asset_id": 2,
            "symbol": "AMD",
            "name": "Advanced Micro Devices",
            "type": "EQUITY",
            "sector": "Technology",
            "industry": "Semiconductors",
            "country": "United States",
            "market_cap": 250_000_000_000,
            "beta": 1.65,

            "quantity": 180.0,
            "currency": "USD",
            "avg_price": 120.00,
            "market_price": 131.67,
            "market_value": 23700.0,
            "market_value_base": 23700.0,

            "performance": {
                "cost_basis": 21600.0,
                "market_value": 23700.0,
                "pnl": 2100.0,
                "pnl_percent": 9.72,
                "cost_basis_base": 21600.0,
                "pnl_base": 2100.0
            }
        },
        {
            "asset_id": 3,
            "symbol": "STM",
            "name": "STMicroelectronics",
            "type": "EQUITY",
            "sector": "Technology",
            "industry": "Semiconductors",
            "country": "France",
            "market_cap": 28_000_000_000,
            "beta": 1.15,

            "quantity": 500.0,
            "currency": "EUR",
            "avg_price": 36.00,
            "market_price": 40.00,
            "market_value": 20000.0,
            "market_value_base": 20000.0,

            "performance": {
                "cost_basis": 18000.0,
                "market_value": 20000.0,
                "pnl": 2000.0,
                "pnl_percent": 11.11,
                "cost_basis_base": 18000.0,
                "pnl_base": 2000.0
            }
        }
    ],
    "exposure": {
        "NVDA": 56.3,
        "AMD": 23.7,
        "STM": 20.0
    },
    "risk": {
        "largest_position_weight": 56.3,
        "concentration_level": "high"
    }
}

print_title("=== CASE 1: HIGH RISK ===")
call_evaluation(asset_analysis, portfolio)


safe_asset = {
    "asset": {
        "symbol": "KO",
        "beta": 0.75
    },
    "indicators": {
        "rsi": 52
    },
    "analysis": {
        "trend": "neutral",
        "volatility_level": "low"
    }
}

safe_portfolio = {
    "portfolio_value": 100000,
    "risk": {
        "largest_position_weight": 20
    },
    "positions": [
        {
            "sector": "Technology",
            "country": "USA",
            "currency": "USD",
            "market_cap": 3_000_000_000_000,
            "beta": 1.1,
            "market_value_base": 20000
        },
        {
            "sector": "Healthcare",
            "country": "Switzerland",
            "currency": "CHF",
            "market_cap": 400_000_000_000,
            "beta": 0.9,
            "market_value_base": 20000
        },
        {
            "sector": "Finance",
            "country": "Italy",
            "currency": "EUR",
            "market_cap": 80_000_000_000,
            "beta": 0.8,
            "market_value_base": 20000
        },
        {
            "sector": "Energy",
            "country": "UK",
            "currency": "GBP",
            "market_cap": 150_000_000_000,
            "beta": 1.0,
            "market_value_base": 20000
        },
        {
            "sector": "Consumer",
            "country": "Japan",
            "currency": "JPY",
            "market_cap": 100_000_000_000,
            "beta": 0.7,
            "market_value_base": 20000
        }
    ]
}

print_title("=== CASE 2: SAFE ===")
call_evaluation(safe_asset, safe_portfolio)

medium_asset = {
    "asset": {
        "id": 2,
        "symbol": "MSFT",
        "name": "Microsoft Corporation",
        "type": "EQUITY",
        "currency": "USD",
        "exchange": "NMS",
        "sector": "Technology",
        "industry": "Software - Infrastructure",
        "country": "United States",
        "market_cap": 3_600_000_000_000,
        "beta": 1.20,
        "website": "https://www.microsoft.com"
    },
    "period": {
        "start": "2025-01-01",
        "end": "2026-01-01"
    },
    "market_data": {
        "records": 252,
        "last_close": 400.00
    },
    "indicators": {
        "sma20": 398.0,
        "sma50": 396.5,
        "rsi": 71.0,
        "daily_volatility": 0.016,
        "annualized_volatility": 0.25,
        "period_range": 42.3
    },
    "analysis": {
        "trend": "neutral",
        "volatility_level": "low"
    }
}

medium_portfolio = {
    "base_currency": "EUR",
    "portfolio_value": 100000,
    "positions": [
        {
            "asset_id": 1,
            "symbol": "MSFT",
            "name": "Microsoft Corporation",
            "type": "EQUITY",
            "sector": "Technology",
            "industry": "Software - Infrastructure",
            "country": "United States",
            "market_cap": 3_600_000_000_000,
            "beta": 1.20,

            "quantity": 77.5,
            "currency": "USD",
            "avg_price": 360.00,
            "market_price": 400.00,
            "market_value": 31000.0,
            "market_value_base": 31000.0,

            "performance": {
                "cost_basis": 27900.0,
                "market_value": 31000.0,
                "pnl": 3100.0,
                "pnl_percent": 11.11,
                "cost_basis_base": 27900.0,
                "pnl_base": 3100.0
            }
        },
        {
            "asset_id": 2,
            "symbol": "GOOGL",
            "name": "Alphabet Inc.",
            "type": "EQUITY",
            "sector": "Technology",
            "industry": "Internet Content & Information",
            "country": "United States",
            "market_cap": 2_300_000_000_000,
            "beta": 1.15,

            "quantity": 160.0,
            "currency": "USD",
            "avg_price": 135.00,
            "market_price": 150.00,
            "market_value": 24000.0,
            "market_value_base": 24000.0,

            "performance": {
                "cost_basis": 21600.0,
                "market_value": 24000.0,
                "pnl": 2400.0,
                "pnl_percent": 11.11,
                "cost_basis_base": 21600.0,
                "pnl_base": 2400.0
            }
        },
        {
            "asset_id": 3,
            "symbol": "JNJ",
            "name": "Johnson & Johnson",
            "type": "EQUITY",
            "sector": "Healthcare",
            "industry": "Drug Manufacturers - General",
            "country": "United States",
            "market_cap": 370_000_000_000,
            "beta": 0.70,

            "quantity": 200.0,
            "currency": "USD",
            "avg_price": 117.00,
            "market_price": 130.00,
            "market_value": 26000.0,
            "market_value_base": 26000.0,

            "performance": {
                "cost_basis": 23400.0,
                "market_value": 26000.0,
                "pnl": 2600.0,
                "pnl_percent": 11.11,
                "cost_basis_base": 23400.0,
                "pnl_base": 2600.0
            }
        },
        {
            "asset_id": 4,
            "symbol": "NESN",
            "name": "Nestlé S.A.",
            "type": "EQUITY",
            "sector": "Consumer",
            "industry": "Packaged Foods",
            "country": "Switzerland",
            "market_cap": 280_000_000_000,
            "beta": 0.65,

            "quantity": 200.0,
            "currency": "CHF",
            "avg_price": 85.50,
            "market_price": 95.00,
            "market_value": 19000.0,
            "market_value_base": 19000.0,

            "performance": {
                "cost_basis": 17100.0,
                "market_value": 19000.0,
                "pnl": 1900.0,
                "pnl_percent": 11.11,
                "cost_basis_base": 17100.0,
                "pnl_base": 1900.0
            }
        }
    ],
    "exposure": {
        "MSFT": 31.0,
        "GOOGL": 24.0,
        "JNJ": 26.0,
        "NESN": 19.0
    },
    "risk": {
        "largest_position_weight": 31.0,
        "concentration_level": "medium"
    }
}

print_title("=== CASE 3: MEDIUM ===")
call_evaluation(medium_asset, medium_portfolio)

medium_portfolio = {
    "base_currency": "EUR",
    "portfolio_value": 100000,
    "positions": [
        {
            "asset_id": 1,
            "symbol": "MSFT",
            "name": "Microsoft Corporation",
            "type": "EQUITY",
            "sector": "Technology",
            "industry": "Software - Infrastructure",
            "country": "United States",
            "market_cap": 3_600_000_000_000,
            "beta": 1.20,

            "quantity": 77.5,
            "currency": "USD",
            "avg_price": 360.00,
            "market_price": 400.00,
            "market_value": 31000.0,
            "market_value_base": 31000.0,

            "performance": {
                "cost_basis": 27900.0,
                "market_value": 31000.0,
                "pnl": 3100.0,
                "pnl_percent": 11.11,
                "cost_basis_base": 27900.0,
                "pnl_base": 3100.0
            }
        },
        {
            "asset_id": 2,
            "symbol": "GOOGL",
            "name": "Alphabet Inc.",
            "type": "EQUITY",
            "sector": "Technology",
            "industry": "Internet Content & Information",
            "country": "United States",
            "market_cap": 2_300_000_000_000,
            "beta": 1.15,

            "quantity": 160.0,
            "currency": "USD",
            "avg_price": 135.00,
            "market_price": 150.00,
            "market_value": 24000.0,
            "market_value_base": 24000.0,

            "performance": {
                "cost_basis": 21600.0,
                "market_value": 24000.0,
                "pnl": 2400.0,
                "pnl_percent": 11.11,
                "cost_basis_base": 21600.0,
                "pnl_base": 2400.0
            }
        },
        {
            "asset_id": 3,
            "symbol": "JNJ",
            "name": "Johnson & Johnson",
            "type": "EQUITY",
            "sector": "Healthcare",
            "industry": "Drug Manufacturers - General",
            "country": "United States",
            "market_cap": 370_000_000_000,
            "beta": 0.70,

            "quantity": 200.0,
            "currency": "USD",
            "avg_price": 117.00,
            "market_price": 130.00,
            "market_value": 26000.0,
            "market_value_base": 26000.0,

            "performance": {
                "cost_basis": 23400.0,
                "market_value": 26000.0,
                "pnl": 2600.0,
                "pnl_percent": 11.11,
                "cost_basis_base": 23400.0,
                "pnl_base": 2600.0
            }
        },
        {
            "asset_id": 4,
            "symbol": "NESN",
            "name": "Nestlé S.A.",
            "type": "EQUITY",
            "sector": "Consumer",
            "industry": "Packaged Foods",
            "country": "Switzerland",
            "market_cap": 280_000_000_000,
            "beta": 0.65,

            "quantity": 200.0,
            "currency": "CHF",
            "avg_price": 85.50,
            "market_price": 95.00,
            "market_value": 19000.0,
            "market_value_base": 19000.0,

            "performance": {
                "cost_basis": 17100.0,
                "market_value": 19000.0,
                "pnl": 1900.0,
                "pnl_percent": 11.11,
                "cost_basis_base": 17100.0,
                "pnl_base": 1900.0
            }
        }
    ],
    "exposure": {
        "MSFT": 31.0,
        "GOOGL": 24.0,
        "JNJ": 26.0,
        "NESN": 19.0
    },
    "risk": {
        "largest_position_weight": 31.0,
        "concentration_level": "medium"
    }
}

print_title("=== CASE 4: STILL MEDIUM ===")
call_evaluation(medium_asset, medium_portfolio)


print_title("=== CASE 5: REAL PORTFOLIO ===")

database = DatabaseManager()
engine = DataEngine(database)
from pprint import pprint
try:
    analysis = engine.analyze_portfolio_full()
    pprint(analysis, sort_dicts=False)

    call_evaluation([ asset for asset in analysis["assets"] ], analysis["portfolio"])

finally:
    engine.close()