from typing import Callable
import logging.config


logger_config = {
    "version": 1,
    "formatters": {},
    "handlers": {},
    "loggers": {},
    "disable_existing_loggers": False,
}


def setup_config(*args: list[Callable], config: dict) -> None:
    for logger in args:
        logger()
    logging.config.dictConfig(config)
