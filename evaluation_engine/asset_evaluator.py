from evaluation_engine.base_evaluator import BaseEvaluator
from evaluation_engine.evaluation_models import AssetEvaluationResult, Severity


class AssetEvaluator(BaseEvaluator):

    @classmethod
    def evaluate(cls, asset_analysis):
        return cls.build_result(
            AssetEvaluationResult,
            symbol=asset_analysis["asset"]["symbol"],
            messages=cls.collect_messages(
                cls.check_rsi(asset_analysis),
                cls.check_volatility(asset_analysis),
                cls.check_trend(asset_analysis),
                cls.check_beta(asset_analysis),
            )
        )
    
    @classmethod
    def check_rsi(cls, asset_analysis):
        rsi = asset_analysis["indicators"].get("rsi")

        if rsi is None:
            return None

        if rsi > 70:
            return cls.message(
                code="ASSET_RSI_OVERBOUGHT",
                type="rsi",
                severity=Severity.MEDIUM,
                message=f"RSI a {rsi:.1f}: possibile ipercomprato."
            )

        elif rsi < 30:
            return cls.message(
                code="ASSET_RSI_OVERSOLD",
                type="rsi",
                severity=Severity.MEDIUM,
                message=f"RSI a {rsi:.1f}: possibile ipervenduto."
            )

        return None

    @classmethod
    def check_volatility(cls, asset_analysis):
        level = asset_analysis["analysis"].get("volatility_level")

        if level == "high":
            return cls.message(
                code="ASSET_HIGH_VOLATILITY",
                type="volatility",
                severity=Severity.MEDIUM,
                message="L'asset presenta volatilità elevata."
            )

        return None

    @classmethod
    def check_trend(cls, asset_analysis):
        trend = asset_analysis["analysis"].get("trend")

        if trend == "bullish":
            return cls.message(
                code="ASSET_BULLISH_TREND",
                type="trend",
                severity=Severity.LOW,
                message="Trend positivo."
            )

        elif trend == "bearish":
            return cls.message(
                code="ASSET_BEARISH_TREND",
                type="trend",
                severity=Severity.MEDIUM,
                message="Trend negativo."
            )

        return None

    @classmethod
    def check_beta(cls, asset_analysis):
        beta = asset_analysis["asset"].get("beta")

        if beta is None:
            return None

        if beta > 1.5:
            return cls.message(
                code="ASSET_HIGH_BETA",
                type="beta",
                severity=Severity.MEDIUM,
                message=f"Beta elevato ({beta:.2f})."
            )

        elif beta < 0.7:
            return cls.message(
                code="ASSET_LOW_BETA",
                type="beta",
                severity=Severity.LOW,
                message=f"Beta contenuto ({beta:.2f})."
            )

        return None