from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from test_utils import *
from data_engine_test_utils import *
from evaluation_engine.evaluation_engine import EvaluationEngine
from data_engine.data_engine import DataEngine
from data_engine.data_engine_models import PortfolioResult
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

asset_analysis = make_asset_result(
    asset=make_asset(
        id=1,
        symbol="NVDA",
        name="NVIDIA Corporation",
        type="EQUITY",
        exchange="NMS",
        industry="Semiconductors",
        country="United States",
        market_cap=3_500_000_000_000,
        beta=1.82,
        website="https://www.nvidia.com",
    )
)

portfolio = make_portfolio_result(
    positions=[
        make_portfolio_position(
            item=make_portfolio_item(
                asset=make_asset(
                    id=1,
                    symbol="NVDA",
                    name="NVIDIA Corporation",
                    type="EQUITY",
                    industry="Semiconductors",
                    country="United States",
                    market_cap=3_500_000_000_000,
                    beta=1.82,
                ),
                position=make_position(
                    asset_id=1,
                    quantity=388,
                    avg_price=120,
                ),
                market_price=145.10,
            ),
            market_value_base=56300,
        ),
        make_portfolio_position(
            item=make_portfolio_item(
                asset=make_asset(
                    id=2,
                    symbol="AMD",
                    name="Advanced Micro Devices",
                    type="EQUITY",
                    industry="Semiconductors",
                    country="United States",
                    market_cap=250_000_000_000,
                    beta=1.65,
                ),
                position=make_position(
                    asset_id=2,
                    quantity=180,
                    avg_price=120,
                ),
                market_price=131.67,
            ),
            market_value_base=23700,
        ),
        make_portfolio_position(
            item=make_portfolio_item(
                asset=make_asset(
                    id=3,
                    symbol="STM",
                    name="STMicroelectronics",
                    type="EQUITY",
                    currency="EUR",
                    industry="Semiconductors",
                    country="France",
                    market_cap=28_000_000_000,
                    beta=1.15,
                ),
                position=make_position(
                    asset_id=3,
                    quantity=500,
                    avg_price=36,
                ),
                market_price=40,
            ),
            market_value_base=20000,
        ),
    ]
)

print_title("=== CASE 1: HIGH RISK ===")
call_evaluation(asset_analysis, portfolio)

safe_asset = make_asset_result(
    asset=make_asset(
        symbol="KO",
        beta=0.75,
    ),
    rsi=52,
    trend=Trend.NEUTRAL,
    volatility_level=VolatilityLevel.LOW,
)

safe_portfolio = make_portfolio_result(
    positions=[
        make_portfolio_position(
            item=make_portfolio_item(
                asset=make_asset(
                    sector="Technology",
                    country="USA",
                    currency="USD",
                    market_cap=3_000_000_000_000,
                    beta=1.1,
                )
            ),
            market_value_base=20_000,
        ),
        make_portfolio_position(
            item=make_portfolio_item(
                asset=make_asset(
                    sector="Healthcare",
                    country="Switzerland",
                    currency="CHF",
                    market_cap=400_000_000_000,
                    beta=0.9,
                )
            ),
            market_value_base=20_000,
        ),
        make_portfolio_position(
            item=make_portfolio_item(
                asset=make_asset(
                    sector="Finance",
                    country="Italy",
                    currency="EUR",
                    market_cap=80_000_000_000,
                    beta=0.8,
                )
            ),
            market_value_base=20_000,
        ),
        make_portfolio_position(
            item=make_portfolio_item(
                asset=make_asset(
                    sector="Energy",
                    country="UK",
                    currency="GBP",
                    market_cap=150_000_000_000,
                    beta=1.0,
                )
            ),
            market_value_base=20_000,
        ),
        make_portfolio_position(
            item=make_portfolio_item(
                asset=make_asset(
                    sector="Consumer",
                    country="Japan",
                    currency="JPY",
                    market_cap=100_000_000_000,
                    beta=0.7,
                )
            ),
            market_value_base=20_000,
        ),
    ]
)

print_title("=== CASE 2: SAFE ===")
call_evaluation(safe_asset, safe_portfolio)

medium_asset = make_asset_result(
    asset=make_asset(
        id=2,
        symbol="MSFT",
        name="Microsoft Corporation",
        type="EQUITY",
        currency="USD",
        exchange="NMS",
        sector="Technology",
        industry="Software - Infrastructure",
        country="United States",
        market_cap=3_600_000_000_000,
        beta=1.20,
        website="https://www.microsoft.com",
    ),
    start=date(2025, 1, 1),
    end=date(2026, 1, 1),
    records=252,
    last_close=400.00,
    sma20=398.0,
    sma50=396.5,
    rsi=71.0,
    daily_volatility=0.016,
    annualized_volatility=0.25,
    period_range=42.3,
    trend=Trend.NEUTRAL,
    volatility_level=VolatilityLevel.LOW,
)

medium_portfolio = make_portfolio_result(
    positions=[
        make_portfolio_position(
            item=make_portfolio_item(
                asset=make_asset(
                    id=1,
                    symbol="MSFT",
                    name="Microsoft Corporation",
                    type="EQUITY",
                    sector="Technology",
                    industry="Software - Infrastructure",
                    country="United States",
                    market_cap=3_600_000_000_000,
                    beta=1.20,
                ),
                position=make_position(
                    asset_id=1,
                    quantity=77.5,
                    avg_price=360.00,
                ),
                market_price=400.00,
            ),
            market_value_base=31_000,
        ),
        make_portfolio_position(
            item=make_portfolio_item(
                asset=make_asset(
                    id=2,
                    symbol="GOOGL",
                    name="Alphabet Inc.",
                    type="EQUITY",
                    sector="Technology",
                    industry="Internet Content & Information",
                    country="United States",
                    market_cap=2_300_000_000_000,
                    beta=1.15,
                ),
                position=make_position(
                    asset_id=2,
                    quantity=160,
                    avg_price=135,
                ),
                market_price=150,
            ),
            market_value_base=24_000,
        ),
        make_portfolio_position(
            item=make_portfolio_item(
                asset=make_asset(
                    id=3,
                    symbol="JNJ",
                    name="Johnson & Johnson",
                    type="EQUITY",
                    sector="Healthcare",
                    industry="Drug Manufacturers - General",
                    country="United States",
                    market_cap=370_000_000_000,
                    beta=0.70,
                ),
                position=make_position(
                    asset_id=3,
                    quantity=200,
                    avg_price=117,
                ),
                market_price=130,
            ),
            market_value_base=26_000,
        ),
        make_portfolio_position(
            item=make_portfolio_item(
                asset=make_asset(
                    id=4,
                    symbol="NESN",
                    name="Nestlé S.A.",
                    type="EQUITY",
                    currency="CHF",
                    sector="Consumer",
                    industry="Packaged Foods",
                    country="Switzerland",
                    market_cap=280_000_000_000,
                    beta=0.65,
                ),
                position=make_position(
                    asset_id=4,
                    quantity=200,
                    avg_price=85.50,
                ),
                market_price=95,
            ),
            market_value_base=19_000,
        ),
    ]
)

print_title("=== CASE 3: MEDIUM ===")
call_evaluation(medium_asset, medium_portfolio)

print_title("=== CASE 4: REAL PORTFOLIO IN DB ===")

database = DatabaseManager()
engine = DataEngine(database)
from pprint import pprint
try:
    analysis = engine.analyze_portfolio_full()
    pprint(analysis, sort_dicts=False)

    call_evaluation([ asset for asset in analysis.assets ], analysis.portfolio)

finally:
    engine.close()