from data_engine.data_engine_models import AssetItem, PortfolioItem, PositionItem


class PortfolioItemBuilder:
    @classmethod
    def build_portfolio(cls, positions: list[PositionItem], assets: dict[int, AssetItem], prices: dict[int, float]) -> list[PortfolioItem]:
        return [
            item
            for position in positions
            if (item := cls._build_portfolio_item(position, assets, prices)   ) is not None
        ]

    @staticmethod
    def _build_portfolio_item(position: PositionItem, assets: dict[int, AssetItem], prices: dict[int, float]) -> PortfolioItem | None:
        asset = assets.get(position.asset_id)
        market_price = prices.get(position.asset_id)

        if asset is None or market_price is None:
            return None

        return PortfolioItem(position=position, asset=asset, market_price=market_price)