import pytest
import json
from unittest.mock import Mock, patch
from openai import OpenAI
from tono.models.openai._client import CompletionClient
from tono.models.openai._formatter import ToolFormatter
from tono.lib.base import TonoCompletionClient, TonoToolFormatter


@pytest.fixture
def mock_openai_client():
    return Mock(spec=OpenAI)


@pytest.fixture
def completion_client(mock_openai_client):
    return CompletionClient(client=mock_openai_client, model="gpt-4", temperature=0.3)


def test_subclassed():
    assert issubclass(CompletionClient, TonoCompletionClient)
    assert issubclass(ToolFormatter, TonoToolFormatter)


def test_init_validates_client_type():
    with pytest.raises(TypeError, match="client must be an instance of openai.OpenAI"):
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
    mock_response = json.dumps({"choices": [{"message": {"content": "test response"}}]})
    assert completion_client.get_response_text(mock_response) == "test response"


def test_get_tool_calls_no_tools(completion_client):
    mock_response = json.dumps({"choices": [{"message": {"content": "test"}}]})
    assert completion_client.get_tool_calls(mock_response) == []


def test_get_tool_calls_with_tools(completion_client):
    mock_tool_calls = [{"function": {"name": "test_func", "arguments": "{}"}}]
    mock_response = json.dumps(
        {"choices": [{"message": {"tool_calls": mock_tool_calls}}]}
    )
    assert completion_client.get_tool_calls(mock_response) == mock_tool_calls


def test_get_tool_details(completion_client):
    mock_tool = {"function": {"name": "test_func", "arguments": '{"arg": "value"}'}}
    name, kwargs = completion_client.get_tool_details(mock_tool)
    assert name == "test_func"
    assert kwargs == {"arg": "value"}


@patch("tono.models.openai._client.print_in_panel")
def test_log_completion(mock_print, completion_client):
    mock_response = json.dumps(
        {
            "choices": [
                {
                    "message": {
                        "content": "test response",
                        "tool_calls": [
                            {
                                "function": {
                                    "name": "test_func",
                                    "arguments": '{"arg": "value"}',
                                }
                            }
                        ],
                    }
                }
            ]
        }
    )

    completion_client.log_completion(mock_response)

    mock_print.assert_any_call("test response", title="Agent Message")
    mock_print.assert_any_call(
        "test_func({'arg': 'value'})", title="Tool Call Requested"
    )
