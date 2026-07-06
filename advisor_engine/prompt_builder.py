from pathlib import Path
from jinja2 import Template
from config import ROOT_DIR, TITLE

from advisor_engine.advisor_models import AdvisorContext, Prompt


class PromptBuilder:
    def __init__(self):
        prompt_dir = ROOT_DIR / "advisor_engine" / "prompts"
        self._system_template = Template((prompt_dir / "system_prompt.txt").read_text(encoding="utf-8"))
        self._user_template = Template((prompt_dir / "user_prompt.txt").read_text(encoding="utf-8"))

    def build(self, context: AdvisorContext, user_prompt: str) -> Prompt:
        return Prompt(
            system_prompt=self._system_template.render(title=TITLE),
            user_prompt=self._user_template.render(
                context=context,
                user_prompt=user_prompt,
            ),
        )