from services.data_service import DataService

if __name__ == "__main__":
    ds = DataService("vault.db")

    result = ds.update_asset("AAPL")

    print(result)