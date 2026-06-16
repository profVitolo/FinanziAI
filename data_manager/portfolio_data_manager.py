import sqlite3
from datetime import datetime
from pathlib import Path
ROOT_DIR = Path(__file__).resolve().parent.parent
from config import DB_PATH
from data_manager.base_data_manager import BaseDataManager

class PortfolioDataManager(BaseDataManager):

    def __init__(self, database):
        super().__init__(database)

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