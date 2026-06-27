from services.exchange_service import ExchangeService


class CurrencyEnricher:
    def __init__(self, exchange_service: ExchangeService):
        self.exchange_service = exchange_service
        self.base_currency = self.exchange_service.base_currency
    
    def enrich_position(self, position):
        result = position.copy()

        currency = position["currency"]

        result["performance"] = self._enrich_performance(position["performance"],currency)
        result["market_value_base"] = self.convert(position["market_value"],currency)

        return result

    def enrich_positions(self, positions):
        return [self.enrich_position(position) for position in positions]

    def _enrich_performance(self, performance, currency):
        result = performance.copy()

        result["cost_basis_base"] = self.convert(performance["cost_basis"], currency)
        result["pnl_base"] = self.convert(performance["pnl"], currency)

        return result

    def convert(self, amount, from_currency):
        try:
            return self.exchange_service.convert(amount, from_currency)
        except ValueError:
            return None