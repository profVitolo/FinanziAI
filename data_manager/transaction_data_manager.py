import sqlite3
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

from config import DB_PATH
from data_manager.base_data_manager import BaseDataManager


class TransactionDataManager(BaseDataManager):
    
    def __init__(self, database=None):
        super().__init__(database)
    
    # ======================
    # COMMANDS
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
            (asset_id, date, operation_type, quantity, price, fees)
        )

        transaction_id = cursor.lastrowid

        """if not self.shared_connection:
            conn.commit()
            conn.close()
        """
        return transaction_id

    def update_transaction(self, transaction_id, asset_id, date, operation_type, quantity, price, fees=0):
        conn = self._connect()

        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE transactions
            SET
                asset_id = ?,
                date = ?,
                type = ?,
                quantity = ?,
                price = ?,
                fees = ?
            WHERE id = ?
            """,
            (asset_id, date, operation_type, quantity, price, fees, transaction_id)
        )

        affected_rows = cursor.rowcount
        """
        if not self.shared_connection:
            conn.commit()
            conn.close()
        """
        return affected_rows > 0

    def delete_transaction(self, transaction_id):
        conn = self._connect()

        cursor = conn.cursor()

        cursor.execute(
            """
            DELETE FROM transactions
            WHERE id = ?
            """,
            (transaction_id,)
        )

        affected_rows = cursor.rowcount
        """
        if not self.shared_connection:
            conn.commit()
            conn.close()
        """
        return affected_rows > 0


    # ======================
    # QUERIES
    # ======================

    def get_transaction(self, transaction_id):
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id, asset_id, date, type, quantity, price, fees 
            FROM transactions
            WHERE id = ?
            """,
            (transaction_id,)
        )

        result = cursor.fetchone()
        """
        if not self.shared_connection:
            conn.close()
        """
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

        query += """
            ORDER BY
                asset_id,
                date
        """

        cursor.execute(query, params)

        results = cursor.fetchall()
        """
        if not self.shared_connection:
            conn.close()
        """
        return results

    def get_transactions_by_asset(self, asset_id, start_date=None, end_date=None):
        conn = self._connect()
        cursor = conn.cursor()

        query = """
            SELECT id, asset_id, date, type, quantity, price, fees 
            FROM transactions
            WHERE asset_id = ?
        """

        params = [asset_id]

        if start_date:
            query += " AND date >= ?"
            params.append(start_date)

        if end_date:
            query += " AND date <= ?"
            params.append(end_date)

        query += " ORDER BY date"

        cursor.execute(query, params)

        results = cursor.fetchall()
        """
        if not self.shared_connection:
            conn.close()
        """
        return results
        
        