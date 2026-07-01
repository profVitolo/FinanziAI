from evaluation_engine.base_evaluator import BaseEvaluator
from evaluation_engine.evaluation_models import AssetEvaluationResult, Severity, EvaluationType, EvaluationCode
from data_engine.data_engine_models import AssetResult, VolatilityLevel, Trend

class AssetEvaluator(BaseEvaluator):

    @classmethod
    def evaluate(cls, asset_analysis: AssetResult):
        return cls.build_result(
            AssetEvaluationResult,
            symbol=asset_analysis.asset.symbol,
            messages=cls.collect_messages(
                cls.check_rsi(asset_analysis),
                cls.check_volatility(asset_analysis),
                cls.check_trend(asset_analysis),
                cls.check_beta(asset_analysis),
            )
        )

    @classmethod
    def check_rsi(cls, asset_analysis: AssetResult):
        rsi = asset_analysis.indicators.rsi
        if rsi is None:
            return None

        if rsi > 70:
            return cls.message(
                code=EvaluationCode.ASSET_RSI_OVERBOUGHT,
                type=EvaluationType.RSI,
                severity=Severity.MEDIUM,
                message=f"RSI a {rsi:.1f}: possibile ipercomprato."
            )

        if rsi < 30:
            return cls.message(
                code=EvaluationCode.ASSET_RSI_OVERBOUGHT,
                type=EvaluationType.RSI,
                severity=Severity.MEDIUM,
                message=f"RSI a {rsi:.1f}: possibile ipervenduto."
            )

        return None

    @classmethod
    def check_volatility(cls, asset_analysis: AssetResult):
        if asset_analysis.analysis.volatility_level == VolatilityLevel.HIGH:
            return cls.message(
                code=EvaluationCode.ASSET_HIGH_VOLATILITY,
                type=EvaluationType.VOLATILITY,
                severity=Severity.MEDIUM,
                message="L'asset presenta volatilità elevata."
            )

        return None

    @classmethod
    def check_trend(cls, asset_analysis: AssetResult):
        trend = asset_analysis.analysis.trend

        if trend == Trend.BULLISH:
            return cls.message(
                code=EvaluationCode.ASSET_BULLISH_TREND,
                type=EvaluationType.TREND,
                severity=Severity.LOW,
                message="Trend positivo."
            )

        if trend == Trend.BEARISH:
            return cls.message(
                code=EvaluationCode.ASSET_BEARISH_TREND,
                type=EvaluationType.TREND,
                severity=Severity.MEDIUM,
                message="Trend negativo."
            )

        return None

    @classmethod
    def check_beta(cls, asset_analysis: AssetResult):
        beta = asset_analysis.asset.beta

        if beta is None:
            return None

        if beta > 1.5:
            return cls.message(
                code=EvaluationCode.ASSET_HIGH_BETA,
                type=EvaluationType.BETA,
                severity=Severity.MEDIUM,
                message=f"Beta elevato ({beta:.2f})."
            )

        if beta < 0.7:
            return cls.message(
                code=EvaluationCode.ASSET_LOW_BETA,
                type=EvaluationType.BETA,
                severity=Severity.LOW,
                message=f"Beta contenuto ({beta:.2f})."
            )

        return None