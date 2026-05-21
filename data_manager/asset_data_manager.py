import sqlite3


class AssetDataManager:

    def __init__(self, db_path):
        self.db_path = db_path

    # ======================
    # INTERNAL
    # ======================

    def _connect(self):
        return sqlite3.connect(self.db_path)

    # ======================
    # ASSETS
    # ======================

    def get_asset_by_symbol(self, symbol):
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id, symbol, name, type, currency, exchange FROM assets WHERE symbol = ?",
            (symbol,)
        )

        result = cursor.fetchone()
        conn.close()
        return result

    def create_asset(self, symbol, name=None, type=None, currency=None, exchange=None):
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO assets (symbol, name, type, currency, exchange)
            VALUES (?, ?, ?, ?, ?)
            """,
            (symbol, name, type, currency, exchange)
        )

        conn.commit()
        asset_id = cursor.lastrowid
        conn.close()
        return asset_id

    # ======================
    # PRICES
    # ======================

    def get_last_price_date(self, asset_id):
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT MAX(date) FROM prices WHERE asset_id = ?",
            (asset_id,)
        )

        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None

    def price_exists(self, asset_id, date):
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT 1 FROM prices WHERE asset_id = ? AND date = ?",
            (asset_id, date)
        )

        exists = cursor.fetchone() is not None
        conn.close()
        return exists

    def save_price(self, asset_id, price):
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO prices (asset_id, date, open, high, low, close, volume)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                asset_id,
                price["date"],
                price["open"],
                price["high"],
                price["low"],
                price["close"],
                price["volume"]
            )
        )

        conn.commit()
        conn.close()

    def save_prices(self, asset_id, prices_list):
        conn = self._connect()
        cursor = conn.cursor()

        cursor.executemany(
            """
            INSERT OR IGNORE INTO prices (asset_id, date, open, high, low, close, volume)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    asset_id,
                    p["date"],
                    p["open"],
                    p["high"],
                    p["low"],
                    p["close"],
                    p["volume"]
                )
                for p in prices_list
            ]
        )

        conn.commit()
        conn.close()

    def get_prices(self, asset_id, start_date=None, end_date=None):
        conn = self._connect()
        cursor = conn.cursor()

        query = "SELECT date, open, high, low, close, volume FROM prices WHERE asset_id = ?"
        params = [asset_id]

        if start_date:
            query += " AND date >= ?"
            params.append(start_date)

        if end_date:
            query += " AND date <= ?"
            params.append(end_date)

        query += " ORDER BY date"

        cursor.execute(query, tuple(params))
        results = cursor.fetchall()

        conn.close()
        return results