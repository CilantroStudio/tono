import anthropic
from tono.base import CompletionClient


class AnthropicCompletionClient(CompletionClient):
    def __init__(
        self,
        api_key: str,
        model: str = "claude-3-5-sonnet-20241022",
        temperature: float = 0.2,
        **kwargs,
    ):
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.kwargs = kwargs  # Store any additional kwargs for client use
        # Create an OpenAI client
        client = anthropic.Anthropic(api_key=api_key)
        self.client = client

    def generate_completion(self, **kwargs):
        # Merge any method-specific kwargs with the class-level kwargs
        merged_kwargs = {**self.kwargs, **kwargs}

        # Pass the merged kwargs to the OpenAI client
        response = self.client.messages.create(
            model=self.model,
            temperature=self.temperature,
            **merged_kwargs,  # Pass down any additional arguments
        )

        return response

    def get_tool_calls(self, response: str) -> list:
        return response.choices[0].message.tool_calls

    def get_response_text(self, response: str) -> str:
        return response.choices[0].message.content

    def format_message(self, message: str, role: str) -> dict:
        return {"role": role, "content": message}
