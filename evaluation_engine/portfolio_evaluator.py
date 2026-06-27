from collections import defaultdict
from evaluation_engine.base_evaluator import BaseEvaluator
from evaluation_engine.evaluation_models import PortfolioEvaluationResult, Severity


class PortfolioEvaluator(BaseEvaluator):

    @classmethod
    def evaluate(cls, portfolio):
        return cls.build_result(
            PortfolioEvaluationResult,
            messages=cls.collect_messages(
                cls.check_concentration(portfolio),
                cls.check_diversification(portfolio),
                cls.check_sector_exposure(portfolio),
                cls.check_country_exposure(portfolio),
                cls.check_currency_exposure(portfolio),
                cls.check_market_cap_exposure(portfolio),
                cls.check_portfolio_beta(portfolio),
            )
        )
    
    @classmethod
    def check_concentration(cls, portfolio):
        risk = portfolio.get("risk", {})
        largest_weight = risk.get("largest_position_weight", 0)

        if largest_weight > 50:
            return cls.message(
                code="PORTFOLIO_HIGH_CONCENTRATION",
                type="concentration",
                severity=Severity.HIGH,
                message=(
                    f"La posizione principale pesa "
                    f"{largest_weight:.2f}% del portafoglio."
                )
            )

        if largest_weight > 25:
            return cls.message(
                code="PORTFOLIO_MEDIUM_CONCENTRATION",
                type="concentration",
                severity=Severity.MEDIUM,
                message=(
                    f"La posizione principale pesa "
                    f"{largest_weight:.2f}% del portafoglio."
                )
            )

        return None
    
    @classmethod
    def check_diversification(cls, portfolio):
        positions = portfolio.get("positions", [])

        if len(positions) < 3:
            return cls.message(
                code="PORTFOLIO_LOW_DIVERSIFICATION",
                type="diversification",
                severity=Severity.MEDIUM,
                message=f"Il portafoglio contiene solo {len(positions)} asset."
            )

        return None
    
    @classmethod
    def check_sector_exposure(cls, portfolio):
        exposures = cls._aggregate_by_field(portfolio, "sector")

        if not exposures:
            return None

        sector, weight = max(exposures.items(), key=lambda item: item[1])

        if sector is None:
            return None

        if weight > 70:
            return cls.message(
                code="PORTFOLIO_HIGH_SECTOR_EXPOSURE",
                type="sector_exposure",
                severity=Severity.HIGH,
                message=(
                    f"Il settore '{sector}' rappresenta "
                    f"{weight:.2f}% del portafoglio."
                )
            )

        if weight > 50:
            return cls.message(
                code="PORTFOLIO_MEDIUM_SECTOR_EXPOSURE",
                type="sector_exposure",
                severity=Severity.MEDIUM,
                message=(
                    f"Il settore '{sector}' rappresenta "
                    f"{weight:.2f}% del portafoglio."
                )
            )

        return None
        
    @classmethod
    def check_country_exposure(cls, portfolio):
        exposures = cls._aggregate_by_field(portfolio, "country")

        if not exposures:
            return None

        country, weight = max(exposures.items(), key=lambda item: item[1])

        if country and weight > 80:
            return cls.message(
                code="PORTFOLIO_COUNTRY_EXPOSURE",
                type="country_exposure",
                severity=Severity.MEDIUM,
                message=(
                    f"Il paese '{country}' rappresenta "
                    f"{weight:.2f}% del portafoglio."
                )
            )

        return None
    
    @classmethod
    def check_currency_exposure(cls, portfolio):
        exposures = cls._aggregate_by_field(portfolio, "currency")

        if not exposures:
            return None

        currency, weight = max(exposures.items(), key=lambda item: item[1])

        if currency and weight > 80:
            return cls.message(
                code="PORTFOLIO_CURRENCY_EXPOSURE",
                type="currency_exposure",
                severity=Severity.MEDIUM,
                message=(
                    f"La valuta '{currency}' rappresenta "
                    f"{weight:.2f}% del portafoglio."
                )
            )

        return None
    
    @classmethod
    def check_market_cap_exposure(cls, portfolio):
        portfolio_value = portfolio.get("portfolio_value", 0)

        if portfolio_value <= 0:
            return None

        small_cap_value = 0

        for position in portfolio.get("positions", []):
            market_cap = position.get("market_cap")

            if market_cap and market_cap < 2_000_000_000:
                value = position.get("market_value_base") or 0
                small_cap_value += value

        weight = small_cap_value / portfolio_value * 100

        if weight > 50:
            return cls.message(
                code="PORTFOLIO_SMALL_CAP_EXPOSURE",
                type="small_cap_exposure",
                severity=Severity.MEDIUM,
                message=(
                    f"Le small cap rappresentano "
                    f"{weight:.2f}% del portafoglio."
                )
            )

        return None
    
    @classmethod
    def check_portfolio_beta(cls, portfolio):
        total_value = portfolio.get("portfolio_value", 0)

        if total_value <= 0:
            return None

        weighted_beta = 0

        for position in portfolio.get("positions", []):
            beta = position.get("beta")

            if beta is None:
                continue

            weight = (position.get("market_value_base") or 0) / total_value
            weighted_beta += beta * weight

        if weighted_beta > 1.5:
            return cls.message(
                code="PORTFOLIO_HIGH_BETA",
                type="portfolio_beta",
                severity=Severity.HIGH,
                message=(
                    f"Beta medio del portafoglio elevato "
                    f"({weighted_beta:.2f})."
                )
            )

        return None
    
    @staticmethod
    def _aggregate_by_field(portfolio, field):
        positions = portfolio.get("positions", [])
        portfolio_value = portfolio.get("portfolio_value") or 0

        result = defaultdict(float)

        if portfolio_value <= 0:
            return result

        for position in positions:
            value = position.get("market_value_base") or 0
            key = position.get(field)

            if key is None:
                continue

            result[key] += (value / portfolio_value) * 100

        return dict(result)