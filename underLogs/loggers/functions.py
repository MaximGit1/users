from underLogs.levels import Levels


def add_logger(
    logger_config,
    name: str,
    level: Levels,
    handlers: list[str],
    propagate: bool = False,
) -> None:
    logger_config["loggers"][name] = {
        "level": level.value,
        "handlers": handlers,
        "propagate": propagate,
    }
