import inspect
from typing_extensions import get_type_hints
from docstring_parser import parse
from typing import Callable, Literal, NotRequired, Optional
from dataclasses import dataclass
from tono.lib.base import TonoToolFormatter


@dataclass
class StructuredParam:
    arg_name: str
    type_name: str
    required: bool
    description: Optional[str] = None
    enum: Optional[list] = None


@dataclass
class StructuredDocstring:
    name: str
    short_description: str
    long_description: str
    params: list
    required: list


def analyze_kwargs_from_func(func):
    # Get the function signature and type hints
    sig = inspect.signature(func)
    type_hints = get_type_hints(func)

    # Extract the type of **kwargs
    for param in sig.parameters.values():
        if (
            param.kind == param.VAR_KEYWORD
        ):  # Check for **kwargs (variadic keyword arguments)
            # Get the type hint for kwargs, assuming it's a TypedDict
            typed_dict_type = type_hints.get(param.name)
            if typed_dict_type and hasattr(typed_dict_type, "__annotations__"):
                return analyze_typed_dict(typed_dict_type)

    return []


def is_enum(type_hint):
    if hasattr(type_hint, "__origin__") and type_hint.__origin__ is Literal:
        return True
    return False


# TODO: Add better support for nested Objects and AnyOf
def get_json_type(type_hint):
    if type_hint is str:
        return "string"
    elif type_hint is int:
        return "integer"
    elif type_hint is float:
        return "number"
    elif type_hint is bool:
        return "boolean"
    elif type_hint is list:
        return "array"
    elif type_hint is dict:
        return "object"
    elif type_hint is None:
        return "null"
    else:
        return "object"


def analyze_typed_dict(typed_dict):
    params = []

    # Iterate through annotations and check for NotRequired
    for key, value in typed_dict.__annotations__.items():
        param = {
            "arg_name": key,
            "required": True,
        }
        param["type_name"] = get_json_type(value)

        if is_enum(value):
            param["type_name"] = list(
                set([get_json_type(type(item)) for item in value.__args__])
            )
            param["enum"] = [item for item in value.__args__]

        if hasattr(value, "__origin__") and value.__origin__ is NotRequired:
            param["required"] = False

        params.append(param)

    return params


def parse_docstring(func: Callable, formatter: TonoToolFormatter):
    doc = parse(str(func.__doc__))
    params = analyze_kwargs_from_func(func)

    # update params with descriptions from docstring if available
    for doc_param in doc.params:
        for param in params:
            if doc_param.arg_name == param["arg_name"]:
                param["description"] = doc_param.description

    structured_docstring = StructuredDocstring(
        name=func.__name__,
        short_description=doc.short_description or "",
        long_description=doc.long_description or "",
        params=[StructuredParam(**param) for param in params],
        required=[param["arg_name"] for param in params if param["required"]],
    )

    formatted_doc = formatter.format(structured_docstring)
    return formatted_doc
