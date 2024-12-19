import logging
from .setup import logger_config


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name=name)
