import typer
from tono.lib import logger, print_in_question_panel
from typing import TypedDict, NotRequired
from pathlib import Path


class TWriteCodeToFile(TypedDict):
    code: str
    file_name: str
    language: NotRequired[str]


def write_code_to_file(**kwargs: TWriteCodeToFile):
    """Writes the generated code to a file in the current working directory. We are using the w+ mode to write the file.

    :param code: The generated code to be written to a file. Should be plain text and not include code fences.
    :type code: str
    :param file_name: The name of the file to write the code to. Including the file extension.
    :type file_name: str

    :return: A message indicating the status of the operation.
    """
    supported_languages = ["python"]
    code = kwargs.get("code", None)
    file_name = kwargs.get("file_name", "test_by_automators_agent.py")

    if not file_name.endswith(".py"):
        return f"Invalid language provided. Only the following languages are supported: {supported_languages}. Please rewrite the code in a supported language."

    if not code:
        return logger.error("code or file_name not provided to write code to file.")

    logger.info(f"Writing code to file {file_name}")
    with open(Path(file_name), "w+") as f:
        f.write(code)
        return f"Code written to {file_name}"


class TGetUserInput(TypedDict):
    question: str


def get_user_input(**kwargs: TGetUserInput) -> str:
    """Prompts the user for input. Use this tool to get input from the user when needed.

    :param str question: The question to ask the user for input.

    :return: The response from the user.
    :rtype: str
    """
    question = kwargs.get("question", None)

    if not question:
        return logger.error("No question provided to get user input for.")

    print_in_question_panel(question)
    response = typer.prompt("Response")

    return response
