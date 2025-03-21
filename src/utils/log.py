__all__ = ["init_logger", "ColorFormatter"]

import logging

from tqdm.contrib.logging import logging_redirect_tqdm

grey = "\x1b[38;20m"
yellow = "\x1b[33;20m"
red = "\x1b[31;20m"
bold_red = "\x1b[31;1m"
reset = "\x1b[0m"

format = "%(asctime)s [%(levelname)s] [%(name)s] %(filename)s:%(lineno)d: %(message)s"

FORMATS = {
    logging.DEBUG: grey + format + reset,
    logging.INFO: grey + format + reset,
    logging.WARNING: yellow + format + reset,
    logging.ERROR: red + format + reset,
    logging.CRITICAL: bold_red + format + reset,
}

uvicorn_access = logging.getLogger("uvicorn.access")
# uvicorn_access.disabled = True

dotenv_logger = logging.getLogger("dotenv.main")
dotenv_logger.disabled = True


class ColorFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_fmt = FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def init_logger(log_level: int = logging.INFO) -> None:
    """
    Initialize the root logger. All future loggers will inherit this logger.
    This function should be called once in your program.
    """
    if not hasattr(init_logger, "initialized"):
        init_logger.initialized = True  # type: ignore
    else:
        return
    # Create a logger
    logger = logging.getLogger()

    # Set the logging level
    logger.setLevel(log_level)

    # Create a console handler and set the formatter
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(ColorFormatter())

    # Add the console handler to the logger
    logger.addHandler(console_handler)

    init_logger.obj = logging_redirect_tqdm()  # type: ignore
    init_logger.obj.__enter__()  # type: ignore
