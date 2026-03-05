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


class LoggingCallback(BaseCallbackHandler):
    def on_llm_start(self, serialized: dict, prompts: list, **kwargs: Any) -> None:
        """Fired when the LLM receives input.

        Args:
            serialized: Serialized LLM config.
            prompts: List of input prompts.
        """
        _logger.info("LLM start: %d prompt(s)", len(prompts))

    def on_llm_end(self, response: Any, **kwargs: Any) -> None:
        """Fired when the LLM finishes generating.

        Args:
            response: The LLM response object.
        """
        _logger.info("LLM end")

    def on_tool_start(self, serialized: dict, input_str: str, **kwargs: Any) -> None:
        """Fired when a tool is invoked.

        Args:
            serialized: Serialized tool config.
            input_str: Input passed to the tool.
        """
        _logger.info("Tool start: %s", serialized.get("name", "?"))

    def on_tool_end(self, output: str, **kwargs: Any) -> None:
        """Fired when a tool returns successfully.

        Args:
            output: The tool output string.
        """
        _logger.info("Tool end")

    def on_tool_error(self, error: BaseException, **kwargs: Any) -> None:
        """Fired when a tool raises an exception.

        Args:
            error: The raised exception.
        """
        _logger.error("Tool error: %s", error)
