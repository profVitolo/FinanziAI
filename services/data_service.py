from data_manager.asset_data_manager import AssetDataManager
from data_collector.yahoo_collector import YahooCollector


class DataService:

    def __init__(self, db_path):
        self.asset_manager = AssetDataManager(db_path)
        self.collector = YahooCollector()

    def update_asset(self, symbol):
        """
        Aggiorna i dati di un asset:
        - crea asset se non esiste
        - scarica nuovi prezzi
        - salva nel database
        """

        # ======================
        # 1. Recupero / creazione asset
        # ======================
        asset = self.asset_manager.get_asset_by_symbol(symbol)

        if asset is None:
            asset_id = self.asset_manager.create_asset(symbol)
        else:
            asset_id = asset[0]  # id è primo campo

        # ======================
        # 2. Ultima data disponibile
        # ======================
        last_date = self.asset_manager.get_last_price_date(asset_id)

        # ======================
        # 3. Download dati
        # ======================
        prices = self.collector.fetch_prices(symbol, start_date=last_date)

        # ======================
        # 4. Controlli minimi (no paranoia)
        # ======================
        if not prices:
            # niente dati → inutile continuare
            return {
                "status": "warning",
                "message": "Nessun dato scaricato"
            }

        # controllo semplice: almeno qualche punto
        if len(prices) < 5:
            return {
                "status": "warning",
                "message": "Dati sospetti (troppo pochi)"
            }

        # ======================
        # 5. Salvataggio (batch)
        # ======================
        self.asset_manager.save_prices(asset_id, prices)

        # ======================
        # 6. Output
        # ======================
        return {
            "status": "ok",
            "message": f"{len(prices)} prezzi aggiornati",
            "asset_id": asset_id
        }