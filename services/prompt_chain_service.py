import re
from typing import Optional

from services.gpt_service import GPTService


class ChainPromptsService:

    def __init__(self, prompts_templates: str, gpt_service: GPTService):
        self.prompts_templates = prompts_templates
        self.gpt_service = gpt_service

    def generate(self, *, initial_text: str) -> Optional[str]:
        response = self._chain_prompts(self.prompts_templates, initial_text)
        return response

    def _extract_prompts_templates(self, prompts_templates_str):
        # Регулярное выражение теперь учитывает опциональность атрибута heat
        pattern = r'<prompt(?: heat="([^"]*)")?>(.*?)</prompt>'
        matches = re.findall(pattern, prompts_templates_str)
        return matches

    def _chain_prompts(self, prompts_templates: str, text: str) -> Optional[str]:
        extracted_prompts_templates = self._extract_prompts_templates(prompts_templates)
        response = text
        conversation_history = []
        for prompt_template in extracted_prompts_templates:
            temperature = float(prompt_template[0]) if prompt_template[0] else None
            prompt = prompt_template[1].format(response)
            msg = {"role": "user", "content": prompt}
            conversation_history.append(msg)
            kwargs = {"temperature": temperature} if temperature else {}
            response = self.gpt_service.query_chatgpt(
                messages=conversation_history, **kwargs
            )
        return response
