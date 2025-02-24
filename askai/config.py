from dataclasses import dataclass
from typing import Optional

@dataclass
class Config:
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    model: str = 'deepseek-chat'

    def __post_init__(self):
        if not self.api_key:
            self.api_key = self._get_api_key_from_env()
        if not self.base_url:
            self.base_url = "https://api.deepseek.com/v1"

    def _get_api_key_from_env(self):
        import os
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("API key not provided and not found in environment variables")
        return api_key