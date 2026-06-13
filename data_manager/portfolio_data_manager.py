import sqlite3
from datetime import datetime
from pathlib import Path
ROOT_DIR = Path(__file__).resolve().parent.parent
from config import DB_PATH

class PortfolioDataManager:

    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path

    def _connect(self):
        return sqlite3.connect(self.db_path)

    # ======================
    # TRANSACTIONS
    # ======================

    def add_transaction(self, asset_id, date, operation_type, quantity, price, fees=0):
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO transactions
            (asset_id, date, type, quantity, price, fees)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                asset_id,
                date,
                operation_type,
                quantity,
                price,
                fees
            )
        )

        conn.commit()
        transaction_id = cursor.lastrowid
        conn.close()

        return transaction_id

    def get_transaction(self, transaction_id):
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                id,
                asset_id,
                date,
                type,
                quantity,
                price,
                fees
            FROM transactions
            WHERE id = ?
            """,
            (transaction_id,)
        )

        result = cursor.fetchone()
        conn.close()

        return result

    def get_transactions(self, start_date=None, end_date=None):
        conn = self._connect()
        cursor = conn.cursor()

        query = """
            SELECT
                id,
                asset_id,
                date,
                type,
                quantity,
                price,
                fees
            FROM transactions
            WHERE 1 = 1
        """

        params = []

        if start_date:
            query += " AND date >= ?"
            params.append(start_date)

        if end_date:
            query += " AND date <= ?"
            params.append(end_date)

        query += " ORDER BY date"

        cursor.execute(query, params)

        results = cursor.fetchall()
        conn.close()

        return results

    def get_transactions_by_asset(self, asset_id):
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                id,
                asset_id,
                date,
                type,
                quantity,
                price,
                fees
            FROM transactions
            WHERE asset_id = ?
            ORDER BY date
            """,
            (asset_id,)
        )

        results = cursor.fetchall()
        conn.close()

        return results

    # ======================
    # PORTFOLIO
    # ======================

    def update_portfolio_position(self, asset_id, quantity, avg_price, last_update=None):
        if last_update is None:
            last_update = datetime.now().strftime("%Y-%m-%d")
        
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id
            FROM portfolio
            WHERE asset_id = ?
            """,
            (asset_id,)
        )

        existing = cursor.fetchone()

        if existing:
            cursor.execute(
                """
                UPDATE portfolio
                SET quantity = ?,
                    avg_price = ?,
                    last_update = ?
                WHERE asset_id = ?
                """,
                (
                    quantity,
                    avg_price,
                    last_update,
                    asset_id
                )
            )
        else:
            cursor.execute(
                """
                INSERT INTO portfolio
                (asset_id, quantity, avg_price, last_update)
                VALUES (?, ?, ?, ?)
                """,
                (
                    asset_id,
                    quantity,
                    avg_price,
                    last_update
                )
            )

        conn.commit()
        conn.close()

    def get_position(self, asset_id):
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                id,
                asset_id,
                quantity,
                avg_price,
                last_update
            FROM portfolio
            WHERE asset_id = ?
            """,
            (asset_id,)
        )

        result = cursor.fetchone()
        conn.close()

        return result

    def get_all_positions(self):
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                id,
                asset_id,
                quantity,
                avg_price,
                last_update
            FROM portfolio
            ORDER BY asset_id
            """
        )

        results = cursor.fetchall()
        conn.close()

        return results
    
    def delete_portfolio_position(self, asset_id):
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute(
            """
            DELETE FROM portfolio
            WHERE asset_id = ?
            """,
            (asset_id,)
        )

        conn.commit()
        conn.close()
        
    # ======================
    # WATCHLIST
    # ======================

    def add_to_watchlist(self, asset_id):
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT OR IGNORE INTO watchlist (asset_id)
            VALUES (?)
            """,
            (asset_id,)
        )

        conn.commit()
        conn.close()

    def remove_from_watchlist(self, asset_id):
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute(
            """
            DELETE FROM watchlist
            WHERE asset_id = ?
            """,
            (asset_id,)
        )

        conn.commit()
        conn.close()

    def get_watchlist(self):
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                id,
                asset_id
            FROM watchlist
            ORDER BY asset_id
            """
        )

        results = cursor.fetchall()
        conn.close()

        return results