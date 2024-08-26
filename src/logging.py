import logging
import sys


def setup_logging() -> None:
    """
    Устанавливает настройки логгирования.
    """
    logging.basicConfig(
        format="[{levelname}] [{asctime}] [{pathname}] {message}",
        style="{",
        stream=sys.stdout,
    )
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)