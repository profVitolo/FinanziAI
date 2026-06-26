from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from api_test_utils import *
from advisor.advisor_engine import AdvisorEngine

def call_advisor(asset_analysis=None, portfolio=None):
    if asset_analysis is not None:
        asset_result = AdvisorEngine.evaluate_asset(asset_analysis)
        print_result("ASSET ADVISOR", asset_result)

    if portfolio is not None:
        portfolio_result = AdvisorEngine.evaluate_portfolio(portfolio)
        print_result("PORTFOLIO ADVISOR", portfolio_result)

print_title("=== TEST ADVISOR ENGINE ===")

asset_analysis = {
    "asset": {
        "symbol": "NVDA",
        "beta": 1.82
    },
    "indicators": {
        "rsi": 76.4
    },
    "analysis": {
        "trend": "bullish",
        "volatility_level": "high"
    }
}

portfolio = {
    "portfolio_value": 100000,
    "risk": {
        "largest_position_weight": 56.3
    },
    "positions": [
        {
            "symbol": "NVDA",
            "sector": "Technology",
            "country": "USA",
            "currency": "USD",
            "market_cap": 3_500_000_000_000,
            "beta": 1.82,
            "market_value_base": 56300
        },
        {
            "symbol": "AMD",
            "sector": "Technology",
            "country": "USA",
            "currency": "USD",
            "market_cap": 250_000_000_000,
            "beta": 1.65,
            "market_value_base": 23700
        },
        {
            "symbol": "STM",
            "sector": "Technology",
            "country": "France",
            "currency": "EUR",
            "market_cap": 28_000_000_000,
            "beta": 1.15,
            "market_value_base": 20000
        }
    ]
}

print_title("=== CASE 1: HIGH RISK ===")
call_advisor(asset_analysis, portfolio)


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
call_advisor(safe_asset, safe_portfolio)


medium_asset = {
    "asset": {
        "symbol": "MSFT",
        "beta": 1.20
    },
    "indicators": {
        "rsi": 71
    },
    "analysis": {
        "trend": "neutral",
        "volatility_level": "low"
    }
}

medium_portfolio = {
    "portfolio_value": 100000,
    "risk": {
        "largest_position_weight": 31
    },
    "positions": [
        {
            "symbol": "MSFT",
            "sector": "Technology",
            "country": "USA",
            "currency": "USD",
            "market_cap": 3_600_000_000_000,
            "beta": 1.20,
            "market_value_base": 55000
        },
        {
            "symbol": "GOOGL",
            "sector": "Technology",
            "country": "USA",
            "currency": "USD",
            "market_cap": 2_300_000_000_000,
            "beta": 1.15,
            "market_value_base": 26000
        },
        {
            "symbol": "NESN",
            "sector": "Consumer",
            "country": "Switzerland",
            "currency": "CHF",
            "market_cap": 280_000_000_000,
            "beta": 0.65,
            "market_value_base": 19000
        }
    ]
}

print_title("=== CASE 3: MEDIUM ===")
call_advisor(medium_asset, medium_portfolio)


medium_portfolio = {
    "portfolio_value": 100000,
    "risk": {
        "largest_position_weight": 31
    },
    "positions": [
        {
            "symbol": "MSFT",
            "sector": "Technology",
            "country": "USA",
            "currency": "USD",
            "market_cap": 3_600_000_000_000,
            "beta": 1.20,
            "market_value_base": 31000
        },
        {
            "symbol": "GOOGL",
            "sector": "Technology",
            "country": "USA",
            "currency": "USD",
            "market_cap": 2_300_000_000_000,
            "beta": 1.15,
            "market_value_base": 24000
        },
        {
            "symbol": "JNJ",
            "sector": "Healthcare",
            "country": "USA",
            "currency": "USD",
            "market_cap": 370_000_000_000,
            "beta": 0.70,
            "market_value_base": 26000
        },
        {
            "symbol": "NESN",
            "sector": "Consumer",
            "country": "Switzerland",
            "currency": "CHF",
            "market_cap": 280_000_000_000,
            "beta": 0.65,
            "market_value_base": 19000
        }
    ]
}

print_title("=== CASE 4: STILL MEDIUM ===")
call_advisor(medium_asset, medium_portfolio)