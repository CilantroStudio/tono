# Tono

Tono is a framework for building autonomous AI agents. 

## Features

- 🔋 Batteries included - Tono provides a basic set of tools for building autonomous AI agents
- 🚀 Automatic tool definition inference from function definition and reStructuredText docstrings
- ✨ Support for OpenAI models
- ✨ Support for Anthropic models

## Installation

You can install Tono using pip:

```bash
pip install tono-ai
```

## Quickstart

Here is a simple example of how to use Tono to build an autonomous AI agent:

```python
from tono import Agent, OpenAICompletionClient
from tono.tools import http_request, write_to_file



openai_client = openai.OpenAI(api_key="your-api-key")
client = OpenAICompletionClient(client=openai_client)


agent = Agent(
    name="gpt-agent",
    client=client,
    tools=[write_to_file, http_request],
    context=[
        {
            "role": "assistant",
            "content": "You are a helpful assistant that...",
        }
    ],
)

agent.start(objective="Use the supplied tools to...")
```


## Contributing

We are passionate about supporting contributors of all levels of experience and would love to see you get involved in the project. See the [contributing guide](/contributing.md) to get started.

## License 

Tono is licensed under the [MIT License](/LICENSE).