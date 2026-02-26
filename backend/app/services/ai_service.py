from anthropic import Anthropic
from openai import OpenAI
from ..core.config import settings
from typing import List, Optional

class AIService:
    def __init__(self):
        self.claude_client = None
        if settings.CLAUDE_API_KEY:
            self.claude_client = Anthropic(api_key=settings.CLAUDE_API_KEY)
        
        self.openai_client = None
        if settings.OPENAI_API_KEY:
            self.openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def generate_description(self, item_name: str, industry: Optional[str] = None) -> str:
        prompt = f"Generate a short, professional, one-sentence description for a line item named '{item_name}' on an invoice."
        if industry:
            prompt += f" The business industry is {industry}."
        
        # Try Claude first
        if self.claude_client:
            try:
                message = self.claude_client.messages.create(
                    model="claude-3-5-sonnet-20240620",
                    max_tokens=100,
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
                return message.content[0].text.strip()
            except Exception as e:
                print(f"Claude Error: {e}")

        # Fallback to OpenAI
        if self.openai_client:
            try:
                response = self.openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=100
                )
                return response.choices[0].message.content.strip()
            except Exception as e:
                print(f"OpenAI Error: {e}")

        # Basic fallback
        return f"Professional consultation and services for {item_name}."

ai_service = AIService()
