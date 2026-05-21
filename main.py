from services.data_service import DataService

if __name__ == "__main__":
    ds = DataService("finanziai.db")

    result = ds.update_asset("AAPL")

    print(result)