import typer
from rich import print

# from tono.cli.commands import init, start
from tono import __version__

app = typer.Typer(name="tono", rich_markup_mode="markdown")
# app.command(short_help="Scaffold new project.")(init.init)
# app.command(short_help="Start the agent.")(start.start)


def version_callback(value: bool):
    if value:
        print(f"Tono CLI Version:  [dark_orange]{__version__}[/dark_orange]")
        raise typer.Exit()


@app.callback()
def common(
    ctx: typer.Context,
    version: bool = typer.Option(None, "--version", callback=version_callback),
):
    pass


if __name__ == "__main__":
    app()
