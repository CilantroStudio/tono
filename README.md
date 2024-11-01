# Tono

[![image](https://img.shields.io/pypi/v/tono-ai.svg)](https://pypi.python.org/pypi/tono-ai)
![GitHub License](https://img.shields.io/github/license/CilantroStudio/tono)
[![Build](https://github.com/CilantroStudio/tono/actions/workflows/build.yaml/badge.svg)](https://github.com/CilantroStudio/tono/actions/workflows/build.yaml)
[![Discord](https://img.shields.io/badge/Discord-%235865F2.svg?logo=discord&logoColor=white)](https://discord.gg/954vZeZ4)


Tono is a framework for building autonomous AI agents. 

## Features

- 🔋 Batteries included - Tono provides a basic set of tools for building autonomous AI agents
- 🚀 Automatic tool definition inference from function definition and reStructuredText docstrings
- ✨ Support for OpenAI models
- ✨ Support for Anthropic models

## Installation

You can install Tono using pip:

```bash
pip install tono-ai[all]
``` 

If you only want to use the OpenAI models, run:

```bash
pip install tono-ai[openai]
```

Alternatively, if you would only like to use the Anthropic models, run:

```bash
pip install tono-ai[anthropic]
```

## Quickstart

Here is a simple example of how to use Tono to build an autonomous AI agent:

```python
import openai
from tono import Agent
from tono.models.openai import CompletionClient
from tono.tools import http_request, write_to_file


openai_client = openai.OpenAI(api_key="your-api-key")
client = CompletionClient(client=openai_client)

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