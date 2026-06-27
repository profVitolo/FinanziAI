from dataclasses import dataclass

@dataclass(frozen=True)
class PortfolioResult:
    base_currency: str
    portfolio_value: float
    positions: list[dict]
    exposure: dict
    risk: dict

@dataclass(frozen=True)
class PortfolioItem:
    """
    DTO utilizzata dal PortfolioAnalyzer.

    Rappresenta tutti gli ingredienti necessari per costruire
    una posizione completa del portafoglio.
    """

    position: dict
    asset: dict
    market_price: float

    @property
    def asset_id(self):
        return self.asset["id"]

    @property
    def symbol(self):
        return self.asset["symbol"]

    @property
    def name(self):
        return self.asset["name"]

    @property
    def type(self):
        return self.asset["type"]

    @property
    def sector(self):
        return self.asset["sector"]

    @property
    def industry(self):
        return self.asset["industry"]

    @property
    def country(self):
        return self.asset["country"]

    @property
    def market_cap(self):
        return self.asset["market_cap"]

    @property
    def beta(self):
        return self.asset["beta"]

    @property
    def currency(self):
        return self.asset["currency"]

    @property
    def quantity(self):
        return self.position["quantity"]

    @property
    def avg_price(self):
        return self.position["avg_price"]