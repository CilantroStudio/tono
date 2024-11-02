import typer
from tono.lib._logging import console
from rich.panel import Panel


def get_input_panel(
    text: str, title: str = "Question?", response_text: str = "Response"
):
    console.print("\n")
    console.print(
        Panel(
            str(text),
            title=title,
            padding=(1, 1),
            highlight=True,
            border_style="color(49)",
        )
    )
    console.print("\n")
    return typer.prompt(response_text)


def print_in_panel(text: str, title: str = "Output"):
    console.print("\n")
    console.print(
        Panel(
            str(text),
            title=title,
            padding=(1, 1),
            highlight=True,
        )
    )
    console.print("\n")
