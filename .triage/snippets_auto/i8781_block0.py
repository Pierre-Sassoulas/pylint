"""A demonstration of a missing logging-fstring-interpolation warning."""
import logging

MSG = "we used an f-string in a logging statement"
logging.error(f"Something bad happened: {MSG}")

file_logger = logging.getLogger(__name__)
file_logger.error(f"Something bad happened: {MSG}")


def my_function(logger: logging.Logger) -> None:
    """A function that accepts a logger."""
    logging.error(f"Something bad happened: {MSG}")

    function_logger = logging.getLogger(my_function.__name__)
    function_logger.error(f"Something bad happened: {MSG}")

    logger.error(f"Something bad happened: {MSG}")  # no logging-fstring-interpolation warning


class MyClass:  # pylint: disable=too-few-public-methods
    """A class with a method that accepts a logger."""

    def __init__(self, logger: logging.Logger) -> None:
        logging.error(f"Something bad happened: {MSG}")

        class_logger = logging.getLogger(MyClass.__name__)
        class_logger.error(f"Something bad happened: {MSG}")

        logger.error(f"Something bad happened: {MSG}")  # no logging-fstring-interpolation warning

