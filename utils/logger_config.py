import logging
from logging.handlers import RotatingFileHandler

from config.settings import settings


def setup_logging() -> None:
    """
    Configures application-wide logging with both console and file handlers.
    Log files are rotated when they reach a specified size to manage disk usage.
    """

    logger = logging.getLogger()
    logger.setLevel(settings.log_level)

    log_format = logging.Formatter('%(asctime)s - %(name)s - %(message)s')

    file_handler = RotatingFileHandler(settings.log_file,
                                       maxBytes=5 * 1024 * 1024,backupCount=3)
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_format)
    logger.addHandler(console_handler)

    logger.info("Logging configured successfully")


setup_logging()