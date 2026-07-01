from collections import defaultdict

from evaluation_engine.base_evaluator import BaseEvaluator
from evaluation_engine.evaluation_models import PortfolioEvaluationResult, Severity, EvaluationType, EvaluationCode


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
            ),
        )

    @classmethod
    def check_concentration(cls, portfolio):
        largest_weight = portfolio.risk.largest_position_weight

        if largest_weight > 50:
            return cls.message(
                code=EvaluationCode.PORTFOLIO_HIGH_CONCENTRATION,
                type=EvaluationType.CONCENTRATION,
                severity=Severity.HIGH,
                message=(
                    f"La posizione principale pesa "
                    f"{largest_weight:.2f}% del portafoglio."
                ),
            )

        if largest_weight > 25:
            return cls.message(
                code=EvaluationCode.PORTFOLIO_MEDIUM_CONCENTRATION,
                type=EvaluationType.CONCENTRATION,
                severity=Severity.MEDIUM,
                message=(
                    f"La posizione principale pesa "
                    f"{largest_weight:.2f}% del portafoglio."
                ),
            )

        return None

    @classmethod
    def check_diversification(cls, portfolio):
        count = len(portfolio.positions)

        if count < 3:
            return cls.message(
                code=EvaluationCode.PORTFOLIO_LOW_DIVERSIFICATION,
                type=EvaluationType.DIVERSIFICATION,
                severity=Severity.MEDIUM,
                message=f"Il portafoglio contiene solo {count} asset.",
            )

        return None

    @classmethod
    def check_sector_exposure(cls, portfolio):
        exposures = cls._aggregate_by_field(portfolio, lambda p: p.asset.sector,)

        if not exposures:
            return None

        sector, weight = max(exposures.items(), key=lambda x: x[1])

        if weight > 70:
            return cls.message(
                code=EvaluationCode.PORTFOLIO_HIGH_SECTOR_EXPOSURE,
                type=EvaluationType.SECTOR_EXPOSURE,
                severity=Severity.HIGH,
                message=f"Il settore '{sector}' rappresenta {weight:.2f}% del portafoglio.",
            )

        if weight > 50:
            return cls.message(
                code=EvaluationCode.PORTFOLIO_MEDIUM_SECTOR_EXPOSURE,
                type=EvaluationType.SECTOR_EXPOSURE,
                severity=Severity.MEDIUM,
                message=f"Il settore '{sector}' rappresenta {weight:.2f}% del portafoglio.",
            )

        return None

    @classmethod
    def check_country_exposure(cls, portfolio):
        exposures = cls._aggregate_by_field(portfolio, lambda p: p.asset.country)

        if not exposures:
            return None

        country, weight = max(exposures.items(), key=lambda x: x[1])

        if weight > 80:
            return cls.message(
                code=EvaluationCode.PORTFOLIO_COUNTRY_EXPOSURE,
                type=EvaluationType.COUNTRY_EXPOSURE,
                severity=Severity.MEDIUM,
                message=f"Il paese '{country}' rappresenta {weight:.2f}% del portafoglio.",
            )

        return None

    @classmethod
    def check_currency_exposure(cls, portfolio):
        exposures = cls._aggregate_by_field(portfolio, lambda p: p.currency)

        if not exposures:
            return None

        currency, weight = max(exposures.items(), key=lambda x: x[1])

        if weight > 80:
            return cls.message(
                code=EvaluationCode.PORTFOLIO_CURRENCY_EXPOSURE,
                type=EvaluationType.CURRENCY_EXPOSURE,
                severity=Severity.MEDIUM,
                message=f"La valuta '{currency}' rappresenta {weight:.2f}% del portafoglio.",
            )

        return None

    @classmethod
    def check_market_cap_exposure(cls, portfolio):
        portfolio_value = portfolio.portfolio_value

        if portfolio_value <= 0:
            return None

        small_cap_value = sum(
            position.market_value_base or 0
            for position in portfolio.positions
            if (position.asset.market_cap is not None and position.asset.market_cap < 2_000_000_000)
        )

        weight = small_cap_value / portfolio_value * 100

        if weight > 50:
            return cls.message(
                code=EvaluationCode.PORTFOLIO_SMALL_CAP_EXPOSURE,
                type=EvaluationType.SMALL_CAP_EXPOSURE,
                severity=Severity.MEDIUM,
                message=f"Le small cap rappresentano {weight:.2f}% del portafoglio.",
            )

        return None

    @classmethod
    def check_portfolio_beta(cls, portfolio):
        total_value = portfolio.portfolio_value

        if total_value <= 0:
            return None

        weighted_beta = 0.0

        for position in portfolio.positions:
            beta = position.asset.beta

            if beta is None:
                continue

            weight = (position.market_value_base or 0) / total_value
            weighted_beta += beta * weight

        if weighted_beta > 1.5:
            return cls.message(
                code=EvaluationCode.PORTFOLIO_HIGH_BETA,
                type=EvaluationType.PORTFOLIO_BETA,
                severity=Severity.HIGH,
                message=f"Beta medio del portafoglio elevato ({weighted_beta:.2f}).",
            )

        return None

    @staticmethod
    def _aggregate_by_field(portfolio, key_fn):
        if portfolio.portfolio_value <= 0:
            return {}

        result = defaultdict(float)

        for position in portfolio.positions:
            key = key_fn(position)

            if key is None:
                continue

            result[key] += ((position.market_value_base or 0) / portfolio.portfolio_value * 100)

        return dict(result)

