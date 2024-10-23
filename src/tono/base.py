from abc import ABC, abstractmethod


class CompletionClient(ABC):
    @abstractmethod
    def generate_completion(self, prompt: str, **kwargs) -> str:
        pass


class ToolFormatter(ABC):
    @abstractmethod
    def format(self, parsed_doc) -> dict:
        pass
