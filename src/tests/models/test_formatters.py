import tono
import pytest

import tono.models
import tono.models.anthropic
import tono.models.anthropic._formatter
import tono.models.openai
import tono.models.openai._formatter


class MockParam:
    def __init__(self, arg_name, type_name, description, enum=None):
        self.arg_name = arg_name
        self.type_name = type_name
        self.description = description
        self.enum = enum


class MockParsedDoc:
    def __init__(
        self, name, short_description, long_description, params=None, required=None
    ):
        self.name = name
        self.short_description = short_description
        self.long_description = long_description
        self.params = params or []
        self.required = required or []


@pytest.mark.parametrize(
    "formatter,expected",
    [
        (
            tono.models.openai._formatter.ToolFormatter(),
            {
                "type": "function",
                "function": {
                    "name": "test_tool",
                    "description": "A test tool This tool is used for testing.",
                },
            },
        ),
        (
            tono.models.anthropic._formatter.ToolFormatter(),
            {
                "name": "test_tool",
                "description": "A test tool This tool is used for testing.",
            },
        ),
    ],
)
def test_tool_formatter_no_params(formatter, expected):
    parsed_doc = MockParsedDoc(
        name="test_tool",
        short_description="A test tool",
        long_description="This tool is used for testing.",
    )
    tool = formatter.format(parsed_doc)
    assert tool == expected


@pytest.mark.parametrize(
    "formatter,expected",
    [
        (
            tono.models.openai._formatter.ToolFormatter(),
            {
                "type": "function",
                "function": {
                    "name": "test_tool",
                    "description": "A test tool This tool is used for testing.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "param1": {
                                "type": "string",
                                "description": "The first parameter",
                            },
                            "param2": {
                                "type": "integer",
                                "description": "The second parameter",
                            },
                        },
                        "required": ["param1", "param2"],
                        "additionalProperties": False,
                    },
                },
            },
        ),
        (
            tono.models.anthropic._formatter.ToolFormatter(),
            {
                "name": "test_tool",
                "description": "A test tool This tool is used for testing.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "param1": {
                            "type": "string",
                            "description": "The first parameter",
                        },
                        "param2": {
                            "type": "integer",
                            "description": "The second parameter",
                        },
                    },
                    "required": ["param1", "param2"],
                },
            },
        ),
    ],
)
def test_tool_formatter_with_params(formatter, expected):
    params = [
        MockParam(
            arg_name="param1", type_name="string", description="The first parameter"
        ),
        MockParam(
            arg_name="param2", type_name="integer", description="The second parameter"
        ),
    ]
    parsed_doc = MockParsedDoc(
        name="test_tool",
        short_description="A test tool",
        long_description="This tool is used for testing.",
        params=params,
        required=["param1", "param2"],
    )
    tool = formatter.format(parsed_doc)
    assert tool == expected


@pytest.mark.parametrize(
    "formatter,expected",
    [
        (
            tono.models.openai._formatter.ToolFormatter(),
            {
                "type": "function",
                "function": {
                    "name": "test_tool",
                    "description": "A test tool This tool is used for testing.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "param1": {
                                "type": "string",
                                "description": "The first parameter",
                                "enum": ["option1", "option2"],
                            }
                        },
                        "required": ["param1"],
                        "additionalProperties": False,
                    },
                },
            },
        ),
        (
            tono.models.anthropic._formatter.ToolFormatter(),
            {
                "name": "test_tool",
                "description": "A test tool This tool is used for testing.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "param1": {
                            "type": "string",
                            "description": "The first parameter",
                            "enum": ["option1", "option2"],
                        }
                    },
                    "required": ["param1"],
                },
            },
        ),
    ],
)
def test_tool_formatter_with_enum(formatter, expected):
    params = [
        MockParam(
            arg_name="param1",
            type_name="string",
            description="The first parameter",
            enum=["option1", "option2"],
        )
    ]
    parsed_doc = MockParsedDoc(
        name="test_tool",
        short_description="A test tool",
        long_description="This tool is used for testing.",
        params=params,
        required=["param1"],
    )
    tool = formatter.format(parsed_doc)
    assert tool == expected
