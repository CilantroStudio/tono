import json
import logging
import uuid
from typing import Callable, Literal
from tono.base import CompletionClient
from tono.lib import logger, get_input_panel, parse_docstring


class Agent:
    def __init__(
        self,
        client: CompletionClient,
        tools: list[Callable],
        context: list = [],
        name: str = "",
    ):
        self.busy = False
        self.client = client
        self.tools = tools
        self.context = context
        self.tool_definitions = []

        # derive tool definitions from the tools
        for func in tools:
            formatted_doc = parse_docstring(func, self.client.tool_formatter)
            self.tool_definitions.append(formatted_doc)

        if name == "":
            self.name = str(uuid.uuid4())
        else:
            self.name = name

    def add_to_context(self, message: str, role: Literal["user", "assistant"] = "user"):
        formatted = self.client.format_message(message, role)
        logger.debug(f"Adding message to context: {formatted}")
        if role and message:
            self.context.append(formatted)

    def start(self, objective: str):
        logger.info(f"Starting agent: [gold3]{self.name}[/gold3]")
        if logger.level > logging.DEBUG:
            logger.info(
                "Set the log level to [dark_sea_green4]DEBUG[/dark_sea_green4] for more detailed logs."
            )
        self.busy = True

        logger.debug(f"Tool Definitions: {json.dumps(self.tool_definitions, indent=2)}")
        self.add_to_context(message=f"Your objective is: {objective}", role="user")

        logger.info("Making initial completion request.")
        _, message, tool_calls = self.client.generate_completion(
            messages=self.context,
            tools=self.tool_definitions,
        )

        while self.busy:
            if tool_calls == []:
                logger.info("No obvious action to be taken.")
                # prompt the user for an additional prompt
                user_input = get_input_panel(
                    """Please enter an additional prompt if you would like to give the agent more context. If you have no additional prompt, you can type "exit" to stop the agent.""",
                    title="Additional Prompt",
                    response_text="Additional Prompt",
                )

                if user_input.lower() != "exit":
                    self.add_to_context(user_input, role="user")
                    _, message, tool_calls = self.client.generate_completion(
                        messages=self.context,
                        tools=self.tool_definitions,
                    )
                    self.add_to_context(message, role="assistant")
                else:
                    self.busy = False
                    break

            for tool_call in tool_calls:
                # TODO: Make sure this becomes model agnostic
                name = tool_call.function.name
                kwargs = json.loads(tool_call.function.arguments)

                # get the tool from the tools list by name
                selected_tool = next(
                    (tool for tool in self.tools if tool.__name__ == name), None
                )

                if selected_tool is None:
                    logger.error(
                        f"Could not find tool: {name}. Please make sure the tool is defined in the tools list."
                    )
                    self.busy = False
                    break

                logger.debug(f"Calling tool: {name} with arguments: {kwargs}")
                function_call_output = selected_tool(**kwargs)
                self.add_to_context(
                    f"Called tool: {name} with arguments: {kwargs}. The function call output was: {function_call_output}",
                    role="assistant",
                )

            logger.debug(json.dumps(self.context, indent=2))
            _, message, tool_calls = self.client.generate_completion(
                messages=self.context,
                tools=self.tool_definitions,
            )
            self.add_to_context(message, role="assistant")
