import os

import woodchips

from github_archive.constants import LOGGER_NAME


def setup_logger(github_archive):
    """Sets up a logger to log to console and a file.

    - Logging can be called with the `logger` property
    - Files will automatically roll over
    """
    logger = woodchips.Logger(
        name=LOGGER_NAME,
        level=github_archive.log_level,
    )
    logger.log_to_console()
    logger.log_to_file(location=os.path.join(github_archive.location, "logs"))


def log_and_raise_value_error(logger, message):
    """Logs an error message, then raises it."""
    logger.critical(message)
    raise ValueError(message)
