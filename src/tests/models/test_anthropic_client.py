import pytest
import json
from unittest.mock import Mock, patch
from anthropic import Anthropic
from tono.models.anthropic._client import CompletionClient
from tono.models.anthropic._formatter import ToolFormatter
from tono.lib.base import TonoCompletionClient, TonoToolFormatter


@pytest.fixture
def mock_anthropic_client():
    return Mock(spec=Anthropic)


@pytest.fixture
def completion_client(mock_anthropic_client):
    return CompletionClient(
        client=mock_anthropic_client, model="claude", temperature=0.3
    )


def test_subclassed():
    assert issubclass(CompletionClient, TonoCompletionClient)
    assert issubclass(ToolFormatter, TonoToolFormatter)


def test_init_validates_client_type():
    with pytest.raises(
        TypeError, match="client must be an instance of anthropic.Anthropic"
    ):
        CompletionClient(client="not_a_client")


def test_tool_formatter_property(completion_client):
    assert isinstance(completion_client.tool_formatter, ToolFormatter)


def test_format_message(completion_client):
    message = "test message"
    formatted = completion_client.format_message(message, role="user")
    assert formatted == {"role": "user", "content": "test message"}
    formatted = completion_client.format_message(message, role="assistant")
    assert formatted == {"role": "assistant", "content": "test message"}

    with pytest.raises(ValueError, match="role must be either 'user' or 'assistant'"):
        completion_client.format_message(message, role="invalid")


def test_get_response_text(completion_client):
    mock_response = json.dumps({"content": [{"type": "text", "text": "test response"}]})
    assert completion_client.get_response_text(mock_response) == "test response"


def test_get_tool_calls_no_tools(completion_client):
    mock_response = json.dumps({"content": [{"type": "text", "text": "test"}]})
    assert completion_client.get_tool_calls(mock_response) == []


def test_get_tool_calls_with_tools(completion_client):
    mock_response = json.dumps(
        {
            "role": "assistant",
            "content": [
                {
                    "type": "text",
                    "text": "<thinking>To answer this question, I will: 1. Use the get_weather tool to get the current weather in San Francisco. 2. Use the get_time tool to get the current time in the America/Los_Angeles timezone, which covers San Francisco, CA.</thinking>",
                },
                {
                    "type": "tool_use",
                    "id": "toolu_01A09q90qw90lq917835lq9",
                    "name": "get_weather",
                    "input": {"location": "San Francisco, CA"},
                },
            ],
        }
    )
    assert completion_client.get_tool_calls(mock_response) == [
        {
            "type": "tool_use",
            "id": "toolu_01A09q90qw90lq917835lq9",
            "name": "get_weather",
            "input": {"location": "San Francisco, CA"},
        }
    ]


def test_get_tool_details(completion_client):
    mock_tool = {"name": "test_func", "input": {"arg": "value"}}
    name, kwargs = completion_client.get_tool_details(mock_tool)
    assert name == "test_func"
    assert kwargs == {"arg": "value"}


@patch("tono.models.anthropic._client.print_in_panel")
def test_log_completion(mock_print, completion_client):
    mock_response = json.dumps(
        {
            "role": "assistant",
            "content": [
                {
                    "type": "text",
                    "text": "test response",
                },
                {
                    "type": "tool_use",
                    "id": "toolu_01A09q90qw90lq917835lq9",
                    "name": "get_weather",
                    "input": {"location": "San Francisco, CA"},
                },
            ],
        }
    )

    completion_client.log_completion(mock_response)

    mock_print.assert_any_call("test response", title="Agent Message")
    mock_print.assert_any_call(
        "get_weather({'location': 'San Francisco, CA'})", title="Tool Call Requested"
    )
