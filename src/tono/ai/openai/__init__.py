import json
import openai
from typing import Any, Literal
from tono.base import ToolFormatter, CompletionClient
from tono.lib import print_in_panel, logger


class OpenAIToolFormatter(ToolFormatter):
    def format(self, parsed_doc):
        tool = {
            "type": "function",
            "function": {
                "name": parsed_doc.name,
                "description": f"{parsed_doc.short_description} {parsed_doc.long_description}",
            },
        }

        if parsed_doc.params:
            tool["function"]["parameters"] = {
                "type": "object",
                "properties": {
                    param.arg_name: {
                        "type": param.type_name,
                        "description": param.description,
                    }
                    for param in parsed_doc.params
                },
                "required": parsed_doc.required,
                "additionalProperties": False,
            }

            for param in parsed_doc.params:
                if param.enum:
                    tool["function"]["parameters"]["properties"][param.arg_name][
                        "enum"
                    ] = param.enum

        return tool


class OpenAICompletionClient(CompletionClient):
    def __init__(
        self,
        client: openai.OpenAI,
        model: str = "gpt-4o",
        temperature: float = 0.3,
        **kwargs,
    ):
        self.client = client
        self.model = model
        self.temperature = temperature
        self.kwargs = kwargs

    @property
    def tool_formatter(self) -> ToolFormatter:
        return OpenAIToolFormatter()

    def generate_completion(
        self,
        messages: list,
        tools: list = [],
        **kwargs,
    ):
        # Pass the merged kwargs to the OpenAI client
        merged_kwargs = {**kwargs, **self.kwargs}
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=tools,
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
            tool_calls = json.loads(response)["choices"][0]["message"].get(
                "tool_calls", None
            )
            if tool_calls is None:
                return []
            return tool_calls
        except Exception as e:
            logger.debug(f"Error getting tool calls: {e}")
            return []

    def get_tool_details(self, tool: Any) -> tuple:
        name = tool["function"]["name"]
        kwargs = json.loads(tool["function"]["arguments"])
        return name, kwargs

    def get_response_text(self, response: str) -> str:
        return json.loads(response)["choices"][0]["message"]["content"]

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
                name = tool_call["function"]["name"]
                kwargs = json.loads(tool_call["function"]["arguments"])
                # truncate any long arguments
                for key, value in kwargs.items():
                    if len(str(value)) > 50:
                        kwargs[key] = f"{str(value)[:50]}..."

                print_in_panel(f"{name}({kwargs})", title="Tool Call Requested")
