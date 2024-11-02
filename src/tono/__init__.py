from tono.lib._agent import Agent  # noqa
import importlib.metadata as _importlib_metadata  # noqa


__app_name__ = "tono"
__version__ = _importlib_metadata.version("tono-ai")


__all__ = ["Agent"]
