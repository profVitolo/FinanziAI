class ExchangeDataManager:
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
		
		