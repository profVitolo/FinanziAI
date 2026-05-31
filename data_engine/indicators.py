import math


class Indicators:

    @staticmethod
    def calculate_sma(prices, period):
        """
        Simple Moving Average (SMA).
        """

        if len(prices) < period:
            return None

        return sum(prices[-period:]) / period

    @staticmethod
    def calculate_rsi(prices, period=14, method="wilder"):
        """
        Relative Strength Index (RSI).

        Supported methods:
            - wilder (default)
            - simple
        """

        if len(prices) < period + 1:
            return None

        gains = []
        losses = []

        for i in range(1, len(prices)):
            delta = prices[i] - prices[i - 1]

            gains.append(max(delta, 0))
            losses.append(max(-delta, 0))

        if method == "simple":

            avg_gain = sum(gains[-period:]) / period
            avg_loss = sum(losses[-period:]) / period

        elif method == "wilder":

            avg_gain = sum(gains[:period]) / period
            avg_loss = sum(losses[:period]) / period

            for i in range(period, len(gains)):
                avg_gain = ((avg_gain * (period - 1)) + gains[i]) / period
                avg_loss = ((avg_loss * (period - 1)) + losses[i]) / period

        else:
            raise ValueError(f"Unsupported RSI method: {method}")

        if avg_loss == 0:
            return 100.0

        rs = avg_gain / avg_loss

        return 100 - (100 / (1 + rs))

    @staticmethod
    def calculate_daily_volatility(prices):
        """
        Standard deviation of daily returns.
        """

        if len(prices) < 2:
            return None

        returns = []

        for i in range(1, len(prices)):
            previous = prices[i - 1]
            current = prices[i]

            if previous == 0:
                continue

            returns.append((current - previous) / previous)

        if len(returns) < 2:
            return None

        mean_return = sum(returns) / len(returns)

        variance = sum(
            (r - mean_return) ** 2
            for r in returns
        ) / (len(returns) - 1)

        return math.sqrt(variance)

    @staticmethod
    def calculate_annualized_volatility(prices):
        """
        Annualized volatility.
        Assumes 252 trading days.
        """

        daily_volatility = Indicators.calculate_daily_volatility(prices)

        if daily_volatility is None:
            return None

        return daily_volatility * math.sqrt(252)

    @staticmethod
    def calculate_period_range(prices):
        """
        Percentage range over the entire period.

        (max_price - min_price) / min_price * 100
        """

        if not prices:
            return None

        min_price = min(prices)
        max_price = max(prices)

        if min_price == 0:
            return None

        return ((max_price - min_price) / min_price) * 100