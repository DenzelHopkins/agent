import logging
from typing import Any

from langchain_core.callbacks import BaseCallbackHandler

# General logging
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s")


def get_logger(name: str) -> logging.Logger:
    """Returns a named logger instance.

    Args:
        name: The logger name, typically __name__.
    """
    return logging.getLogger(name)


# LangChain logging
_logger = logging.getLogger(__name__)

# Max chars for variable log content to fit k9s log view
_MAX = 120


def _t(s: str) -> str:
    """Truncate string to _MAX chars."""
    s = str(s)
    return s if len(s) <= _MAX else s[:_MAX] + "..."


class LoggingCallback(BaseCallbackHandler):
    def on_llm_start(self, serialized: dict, prompts: list, **kwargs: Any) -> None:
        model = serialized.get("kwargs", {}).get("model", serialized.get("name", "?"))
        _logger.info("LLM start: model=%s prompts=%d", model, len(prompts))
        for i, p in enumerate(prompts):
            _logger.info("LLM prompt[%d]: %s", i, _t(p))

    def on_llm_end(self, response: Any, **kwargs: Any) -> None:
        generations = response.generations
        text = generations[0][0].text if generations else ""
        _logger.info("LLM end: %s", _t(text))

    def on_tool_start(self, serialized: dict, input_str: str, **kwargs: Any) -> None:
        name = serialized.get("name", "?")
        _logger.info("Tool start: %s input=%s", name, _t(input_str))

    def on_tool_end(self, output: str, **kwargs: Any) -> None:
        _logger.info("Tool end: %s", _t(output))

    def on_tool_error(self, error: BaseException, **kwargs: Any) -> None:
        _logger.error("Tool error: %s", _t(str(error)))
