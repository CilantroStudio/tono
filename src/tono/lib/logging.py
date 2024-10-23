import logging
import os
from rich.logging import RichHandler
from rich.console import Console
from rich.theme import Theme

console = Console(
    theme=Theme(
        {
            "logging.level.info": "cornflower_blue",
            "logging.level.debug": "dark_sea_green4",
            "logging.level.warning": "gold3",
            "logging.level.error": "red1",
        }
    ),
)

FORMAT = "%(message)s"
LOG_LEVEL = os.environ.get("LOG_LEVEL", logging.INFO)

logging.basicConfig(
    format=FORMAT,
    datefmt="[%X]",
    handlers=[RichHandler(markup=True, console=console, rich_tracebacks=True)],
)

logger = logging.getLogger("tono")
logger.setLevel(LOG_LEVEL)
