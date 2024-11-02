from tono.models.openai import CompletionClient as OpenAICompletionClient
from tono.lib.base import TonoCompletionClient


def test_openai_completion_client():
    assert issubclass(OpenAICompletionClient, TonoCompletionClient)
    assert hasattr(OpenAICompletionClient, "tool_formatter")
    assert hasattr(OpenAICompletionClient, "generate_completion")
    assert hasattr(OpenAICompletionClient, "get_tool_calls")
    assert hasattr(OpenAICompletionClient, "get_response_text")
    assert hasattr(OpenAICompletionClient, "get_tool_details")
    assert hasattr(OpenAICompletionClient, "format_message")
