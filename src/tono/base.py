from abc import ABC, abstractmethod
from typing import Any


class ToolFormatter(ABC):
    @abstractmethod
    def format(self, parsed_doc) -> dict:
        pass


class CompletionClient(ABC):
    @property
    def tool_formatter(self) -> ToolFormatter:
        pass

    @abstractmethod
    def generate_completion(self, messages: list, tools: list, **kwargs) -> tuple:
        pass

    @abstractmethod
    def get_tool_calls(self, response: str) -> list:
        pass

    @abstractmethod
    def get_tool_details(self, tool: Any) -> tuple:
        pass

    @abstractmethod
    def get_response_text(self, response: str) -> str:
        pass

    @abstractmethod
    def format_message(self, message: str, role: str) -> dict:
        pass
