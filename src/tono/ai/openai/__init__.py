import openai
from tono.base import ToolFormatter, CompletionClient


class OpenAICompletionClient(CompletionClient):
    def __init__(
        self, api_key: str, model: str = "gpt-4o", temperature: float = 0.2, **kwargs
    ):
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.kwargs = kwargs  # Store any additional kwargs for client use
        # Create an OpenAI client
        client = openai.Client(api_key=api_key)
        self.client = client

    def generate_completion(self, **kwargs):
        # Merge any method-specific kwargs with the class-level kwargs
        merged_kwargs = {**self.kwargs, **kwargs}

        # Pass the merged kwargs to the OpenAI client
        response = self.client.Completion.create(
            engine=self.model,
            temperature=self.temperature,
            **merged_kwargs,  # Pass down any additional arguments
        )

        return response


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
