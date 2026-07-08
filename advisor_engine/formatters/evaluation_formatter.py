from evaluation_engine.evaluation_models import AssetEvaluationResult, EvaluationMessage, PortfolioEvaluationResult
from advisor_engine.formatters.utils import join_lines


def format_portfolio_evaluation(evaluation: PortfolioEvaluationResult) -> str:
    lines = [f"Highest severity: {evaluation.summary.highest_severity.value}", ""]
    lines.extend(format_evaluation_message(message) for message in evaluation.messages)

    return join_lines(lines)

def format_asset_evaluations(evaluations: list[AssetEvaluationResult]) -> str:
    lines: list[str] = []

    for evaluation in evaluations:
        lines.append(evaluation.symbol)
        lines.extend(f"  {format_evaluation_message(message)}" for message in evaluation.messages)
        lines.append("")

    return join_lines(lines)

def format_evaluation_message(message: EvaluationMessage) -> str:
    return (f"- [{message.severity.value}] {message.message}")

def format_asset_evaluations(evaluations: list[AssetEvaluationResult]) -> str:
    lines: list[str] = []

    for evaluation in evaluations:
        lines.append(f"Asset: {evaluation.symbol}")

        if evaluation.messages:
            lines.extend(format_evaluation_message(message) for message in evaluation.messages)
        else:
            lines.append("- No evaluation messages")

        lines.append("")

    return join_lines(lines)