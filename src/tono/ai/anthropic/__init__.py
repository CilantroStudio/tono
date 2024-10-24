import json
import anthropic
from typing import Any, Literal
from tono.base import ToolFormatter, CompletionClient
from tono.lib import print_in_panel, logger


class AnthropicToolFormatter(ToolFormatter):
    def format(self, parsed_doc):
        tool = {
            "name": parsed_doc.name,
            "description": f"{parsed_doc.short_description} {parsed_doc.long_description}",
        }

        if parsed_doc.params:
            tool["input_schema"] = {
                "type": "object",
                "properties": {
                    param.arg_name: {
                        "type": param.type_name,
                        "description": param.description,
                    }
                    for param in parsed_doc.params
                },
                "required": parsed_doc.required,
            }

            for param in parsed_doc.params:
                if param.enum:
                    tool["input_schema"]["properties"][param.arg_name]["enum"] = (
                        param.enum
                    )

        return tool


class AnthropicCompletionClient(CompletionClient):
    def __init__(
        self,
        client: anthropic.Anthropic,
        model: str = "claude-3-5-sonnet-20241022",
        max_tokens=1024,
        temperature: float = 0.3,
        **kwargs,
    ):
        self.client = client
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.kwargs = kwargs

    @property
    def tool_formatter(self) -> ToolFormatter:
        return AnthropicToolFormatter()

    def generate_completion(
        self,
        messages: list,
        tools: list = [],
        **kwargs,
    ):
        # Pass the merged kwargs to the client
        merged_kwargs = {**kwargs, **self.kwargs}
        response = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            tools=tools,
            messages=messages,
            temperature=self.temperature,
            **merged_kwargs,
        )

        res_json = response.to_json()
        message = self.get_response_text(res_json)
        tool_calls = self.get_tool_calls(res_json)

        self.log_completion(res_json)

        return response, message, tool_calls

    def get_tool_calls(self, response: str) -> list:
        try:
            items = json.loads(response)["content"]
            tool_calls = [item for item in items if item["type"] == "tool_use"]
            return tool_calls
        except Exception as e:
            logger.error(f"Error getting tool calls: {e}")
            return []

    def get_tool_details(self, tool: Any) -> tuple:
        name = tool["name"]
        kwargs = tool["input"]
        return name, kwargs

    def get_response_text(self, response: str) -> str:
        text_responses = [
            item["text"]
            for item in json.loads(response)["content"]
            if item["type"] == "text"
        ]
        return " ".join(text_responses)

    def format_message(self, message: str, role=Literal["user", "assistant"]) -> dict:
        return {"role": role, "content": str(message)}

    def log_completion(self, response: str):
        content = self.get_response_text(response)
        tool_calls = self.get_tool_calls(response)

        # log info in a panel
        if content:
            print_in_panel(str(content), title="Agent Message")
        if tool_calls:
            # loop through tool calls and format them as python function calls
            for tool_call in tool_calls:
                name = tool_call["name"]
                kwargs = tool_call["input"]
                # truncate any long arguments
                for key, value in kwargs.items():
                    if len(str(value)) > 50:
                        kwargs[key] = f"{str(value)[:50]}..."

                print_in_panel(f"{name}({kwargs})", title="Tool Call Requested")
