from pathlib import Path
from jinja2 import Template
from config import ROOT_DIR, TITLE

from advisor_engine.advisor_models import AdvisorContext, Prompt


class PromptBuilder:
    def __init__(self):
        prompt_dir = ROOT_DIR / "advisor_engine" / "prompts"

        self._system_template = Template(
            (prompt_dir / "system_prompt.txt").read_text(
                encoding="utf-8"
            )
        )

        self._user_template = Template(
            (prompt_dir / "user_prompt.txt").read_text(
                encoding="utf-8"
            )
        )

    def build(self, context: AdvisorContext, user_prompt: str,) -> Prompt:
        system_prompt = self._system_template.render(title=TITLE,)

        rendered_user_prompt = self._user_template.render(
            context=self._build_context(context),
            user_prompt=user_prompt,
        )

        return Prompt(system_prompt=system_prompt, user_prompt=rendered_user_prompt)

    def _build_context(self, context: AdvisorContext,) -> str:
        lines: list[str] = []

        lines.append("==============================")
        lines.append("DATA")
        lines.append("==============================")
        lines.append(str(context.current_date))
        lines.append("")

        lines.append("==============================")
        lines.append("PROFILO INVESTITORE")
        lines.append("==============================")
        lines.append(context.investor_profile.value)
        lines.append("")

        lines.append("==============================")
        lines.append("PORTAFOGLIO")
        lines.append("==============================")
        lines.append(
            f"Valore: {context.portfolio.portfolio_value:.2f} "
            f"{context.portfolio.base_currency}"
        )
        lines.append(
            f"Numero posizioni: {len(context.portfolio.positions)}"
        )
        lines.append("")

        lines.append("==============================")
        lines.append("VALUTAZIONE PORTAFOGLIO")
        lines.append("==============================")
        lines.append(str(context.portfolio_evaluation))
        lines.append("")

        if context.portfolio_asset_evaluations:
            lines.append("==============================")
            lines.append("ASSET DEL PORTAFOGLIO")
            lines.append("==============================")

            for evaluation in context.portfolio_asset_evaluations:
                lines.append(str(evaluation))

            lines.append("")

        if context.watchlist:
            lines.append("==============================")
            lines.append("WATCHLIST")
            lines.append("==============================")

            for asset in context.watchlist:
                lines.append(str(asset))

            lines.append("")

        if context.watchlist_evaluations:
            lines.append("==============================")
            lines.append("VALUTAZIONE WATCHLIST")
            lines.append("==============================")

            for evaluation in context.watchlist_evaluations:
                lines.append(str(evaluation))

        return "\n".join(lines)