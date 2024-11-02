from abc import ABC, abstractmethod
from typing import Any


class TonoToolFormatter(ABC):
    @abstractmethod
    def format(self, parsed_doc) -> dict:
        pass


class TonoCompletionClient(ABC):
    @abstractmethod
    def tool_formatter(self) -> TonoToolFormatter:
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
