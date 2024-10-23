import json
import openai
from typing import Any, Literal
from tono.base import ToolFormatter, CompletionClient
from tono.lib import print_in_panel


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
        temperature: float = 0.3,
        model: str = "gpt-4o",
        **kwargs,
    ):
        self.client = client
        self.temperature = temperature
        self.model = model
        self.kwargs = kwargs

    @property
    def tool_formatter(self) -> ToolFormatter:
        # TODO: Think about if this should be written differently
        # TODO: Should this just be a function?
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
        self.log_completion(response.to_json())
        message = self.get_response_text(response)
        tool_calls = self.get_tool_calls(response)
        if tool_calls is None:
            tool_calls = []
        return response, message, tool_calls

    def get_tool_calls(self, response: Any) -> list:
        return response.choices[0].message.tool_calls

    def get_response_text(self, response: Any) -> str:
        return response.choices[0].message.content

    def format_message(self, message: str, role=Literal["user", "assistant"]) -> dict:
        return {"role": role, "content": str(message)}

    def log_completion(self, response: str):
        # try to get ai message content
        try:
            content = json.loads(response)["choices"][0]["message"]["content"]
        except KeyError:
            content = None

        # try to get tool function calls
        try:
            tool_calls = json.loads(response)["choices"][0]["message"]["tool_calls"]
        except KeyError:
            tool_calls = None

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
