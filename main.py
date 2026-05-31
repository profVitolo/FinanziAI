from services.data_service import DataService
from data_manager.asset_data_manager import AssetDataManager
from data_engine.data_engine import DataEngine


if __name__ == "__main__":
    db_path = "vault.db"

    ds = DataService(db_path)

    print(ds.update_asset("AAPL", initial_days=365))
    print(ds.update_asset("^GSPC", initial_days=365))

    adm = AssetDataManager(db_path)

    # Test 1: recupero asset
    asset = adm.get_asset_by_symbol("AAPL")
    print("Asset:", asset)

    if asset:
        asset_id = asset[0]

        print("\n=== LAST DATE ===")
        print(adm.get_last_price_date(asset_id))

        prices = adm.get_prices(asset_id)

        print("\n=== PRICE COUNT ===")
        print(len(prices))

        print("\n=== FIRST 5 ===")
        for row in prices[:5]:
            print(row)

        print("\n=== LAST 5 ===")
        for row in prices[-5:]:
            print(row)

    # =====================================
    # Test DataEngine
    # =====================================
    engine = DataEngine(db_path)

    print("\n=== AAPL ANALYSIS ===")
    print(engine.analyze_asset("AAPL"))

    print("\n=== S&P500 ANALYSIS ===")
    print(engine.analyze_asset("^GSPC"))