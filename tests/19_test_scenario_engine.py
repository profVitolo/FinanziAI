from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from test_utils import *
from data_engine_test_utils import *

from scenario_engine.scenario_builder import ScenarioBuilder

print_title("=== TEST SCENARIO BUILDER ===")


asset = make_asset(id=1, symbol="AAPL",name="Apple Inc.")


print_result(
    "ADD ASSET",
    ScenarioBuilder.add_asset(
        asset=asset,
        quantity=10,
        avg_price=180,
    ),
)

print_result(
    "REMOVE ASSET",
    ScenarioBuilder.remove_asset(
        asset=asset,
    ),
)

asset2 = make_asset(
    id=2,
    symbol="MSFT",
    name="Microsoft Corporation",
)
print_result("Asset2", asset2)

print_result(
    "REBALANCE",
    ScenarioBuilder.rebalance(
        target_weights={
            asset: 40,
            asset2: 60,
        }
    ),
)