from services.data_service import DataService
from data_manager.asset_data_manager import AssetDataManager
from data_engine.data_engine import DataEngine


if __name__ == "__main__":
    db_path = "vault.db"

    ds = DataService(db_path)

    result = ds.update_asset("AAPL")
    print(result)

    result = ds.update_asset("^GSPC")
    print(result)

    adm = AssetDataManager(db_path)

    # Test 1: recupero asset
    asset = adm.get_asset_by_symbol("AAPL")
    print("Asset:", asset)

    if asset:

        asset_id = asset[0]

        # Test 2: ultima data disponibile
        last_date = adm.get_last_price_date(asset_id)
        print("Ultima data:", last_date)

        # Test 3: storico prezzi
        prices = adm.get_prices(asset_id)

        print(f"Numero record: {len(prices)}")

        for row in prices[:5]:
            print(row)

        for row in prices[-5:]:
            print(row)

    # =====================================
    # Test DataEngine
    # =====================================
    engine = DataEngine(db_path)

    analysis = engine.analyze_asset("AAPL")

    print("\n=== DATA ENGINE ===")
    print(analysis)
    
    analysis = engine.analyze_asset("^GSPC")
    print("\n=== S&P500 ===")
    print(analysis)