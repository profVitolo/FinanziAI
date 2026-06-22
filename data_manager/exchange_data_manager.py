import sqlite3
from data_manager.base_data_manager import BaseDataManager

class ExchangeDataManager(BaseDataManager):
    def __init__(self, database):
        self.database = database

    def _connect(self):
        return self.database.connect()

    def save_rate(self, from_currency, to_currency, rate, rate_date):
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT OR REPLACE INTO exchange_rates (
                from_currency,
                to_currency,
                rate_date,
                rate
            )
            VALUES (?, ?, ?, ?)
            """,
            (from_currency.upper(), to_currency.upper(), rate_date, rate)
        )

    def get_rate(self, from_currency, to_currency, rate_date):
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                from_currency,
                to_currency,
                rate_date,
                rate
            FROM exchange_rates
            WHERE from_currency = ?
              AND to_currency = ?
              AND rate_date = ?
            """,
            (from_currency, to_currency, rate_date)
        )

        result = cursor.fetchone()
        return dict(result) if result else None
        
    def get_latest_rate_before(self, from_currency, to_currency, rate_date=None):
        conn = self._connect()
        cursor = conn.cursor()

        if rate_date is None:
            cursor.execute(
                """
                SELECT
                    from_currency,
                    to_currency,
                    rate_date,
                    rate
                FROM exchange_rates
                WHERE from_currency = ?
                  AND to_currency = ?
                ORDER BY rate_date DESC
                LIMIT 1
                """,
                (from_currency, to_currency)
            )
        else:
            cursor.execute(
                """
                SELECT
                    from_currency,
                    to_currency,
                    rate_date,
                    rate
                FROM exchange_rates
                WHERE from_currency = ?
                  AND to_currency = ?
                  AND rate_date <= ?
                ORDER BY rate_date DESC
                LIMIT 1
                """,
                (from_currency, to_currency, rate_date)
            )

        result = cursor.fetchone()

        return dict(result) if result else None

    def get_latest_rate(self, from_currency, to_currency):
        return self.get_latest_rate_before(from_currency, to_currency)

    def get_all_rates(self):
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                from_currency,
                to_currency,
                rate_date,
                rate
            FROM exchange_rates
            ORDER BY
                from_currency,
                to_currency,
                rate_date DESC
            """
        )

        return [dict(row) for row in cursor.fetchall()]
		
    def get_rates(self, from_currency=None, to_currency=None, start_date=None, end_date=None):
        conn = self._connect()
        cursor = conn.cursor()

        query = """
            SELECT
                from_currency,
                to_currency,
                rate_date,
                rate
            FROM exchange_rates
            WHERE 1 = 1
        """

        params = []

        if from_currency:
            query += " AND from_currency = ?"
            params.append(from_currency.upper())

        if to_currency:
            query += " AND to_currency = ?"
            params.append(to_currency.upper())

        if start_date:
            query += " AND rate_date >= ?"
            params.append(start_date)

        if end_date:
            query += " AND rate_date <= ?"
            params.append(end_date)

        query += """
            ORDER BY
                from_currency,
                to_currency,
                rate_date DESC
        """

        cursor.execute(query, params)

        return [dict(row) for row in cursor.fetchall()]
		
    def get_from_currencies(self):
        conn = self._connect()
        cursor = conn.cursor()
        
        query = """
            SELECT DISTINCT from_currency
            FROM exchange_rates
            ORDER BY from_currency
        """
        
        cursor.execute(query)
        
        return [
            row["from_currency"]
            for row in cursor.fetchall()
        ]
