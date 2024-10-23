import uuid
from typing import Callable
from tono.base import CompletionClient


class Agent:
    group_chat = []

    def __init__(
        self,
        client: CompletionClient,
        tools: list[Callable],
        name: str = "",
    ):
        self.client = client
        self.tools = tools
        self.busy = False
        if name == "":
            self.name = str(uuid.uuid4())
        else:
            self.name = name

    def stop(self):
        self.busy = False

    def start(self, directive: str):
        self.busy = True
        while self.busy:
            print("Agent received directive:", directive)
            print(f"Agent {self.name} is running in a loop")
            # add the directive to the group chat
            self.add_to_context(directive)
            self.busy = False

    def add_to_context(cls, message):
        # TODO: convert message into the correct format for the completion client
        cls.group_chat.append(message)
