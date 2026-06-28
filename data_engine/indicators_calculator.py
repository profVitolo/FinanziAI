import math

from data_engine.data_engine_models import RsiMethod


class IndicatorsCalculator:
    def sma(self, prices: list[float], period: int) -> float | None:
        if len(prices) < period:
            return None

        return sum(prices[-period:]) / period

    def rsi(self, prices: list[float], period: int = 14, method: RsiMethod = RsiMethod.WILDER) -> float | None:
        if len(prices) < period + 1:
            return None

        gains = []
        losses = []

        for previous, current in zip(prices, prices[1:]):
            delta = current - previous
            gains.append(max(delta, 0))
            losses.append(max(-delta, 0))

        if method is RsiMethod.SIMPLE:
            avg_gain = sum(gains[-period:]) / period
            avg_loss = sum(losses[-period:]) / period
        elif method is RsiMethod.WILDER:
            avg_gain = sum(gains[:period]) / period
            avg_loss = sum(losses[:period]) / period

            for gain, loss in zip(gains[period:], losses[period:]):
                avg_gain = ((avg_gain * (period - 1)) + gain) / period
                avg_loss = ((avg_loss * (period - 1)) + loss) / period
        else:
            raise ValueError(f"Unsupported RSI method: {method}")

        if avg_loss == 0:
            return 100.0

        rs = avg_gain / avg_loss
        return 100 - (100 / (1 + rs))

    def daily_volatility(self, prices: list[float]) -> float | None:
        if len(prices) < 2:
            return None

        returns = [
            (current - previous) / previous
            for previous, current in zip(prices, prices[1:])
            if previous != 0
        ]

        if len(returns) < 2:
            return None

        mean = sum(returns) / len(returns)

        variance = sum(
            (r - mean) ** 2
            for r in returns
        ) / (len(returns) - 1)

        return math.sqrt(variance)

    def annualized_volatility(self, daily_volatility: float | None) -> float | None:
        if daily_volatility is None:
            return None
        return daily_volatility * math.sqrt(252)

    def period_range(self, prices: list[float]) -> float | None:
        if not prices:
            return None

        minimum = min(prices)

        if minimum == 0:
            return None

        maximum = max(prices)

        return ((maximum - minimum) / minimum) * 100