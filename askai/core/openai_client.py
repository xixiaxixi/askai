from typing import Optional, Generator
import openai
from openai import OpenAI
import sys

from ..config import Config


class OpenAIClient:
    def __init__(self, config: Config):
        self.config = config
        self._setup_client()

    def _setup_client(self):
        self.client = OpenAI(
            api_key=self.config.api_key,
            base_url=self.config.base_url
        )

    def ask_stream(self, question: str, system_prompt: Optional[str] = None) -> Generator[str, None, str]:
        """流式获取响应"""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": question})

        try:
            response = self.client.chat.completions.create(
                model=self.config.model,
                messages=messages,
                stream=True
            )

            full_response = ""
            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    content = chunk.choices[0].delta.content
                    full_response += content
                    yield content

            return full_response

        except Exception as e:
            raise Exception(f"Failed to get response from OpenAI: {str(e)}")

    def ask(self, question: str, system_prompt: Optional[str] = None) -> str:
        """获取完整响应"""
        full_response = ""
        for content in self.ask_stream(question, system_prompt):
            print(content, end="", flush=True)
            full_response += content
        print()  # 最后打印换行
        return full_response