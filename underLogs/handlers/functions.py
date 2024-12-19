from underLogs.handlers import HandlerClasses
from underLogs.levels import Levels


def add_handler(
    logger_config,
    name: str,
    level: Levels,
    class_: HandlerClasses,
    formatter: str,
    filename: str | None = None,
) -> str:
    current_handler = logger_config["handlers"][name] = {
        "level": level.value,
        "class": class_.value,
        "formatter": formatter,
    }
    if (class_ is HandlerClasses.FileHandler) or (
        class_ is HandlerClasses.JsonHandler
    ):
        if filename is None:
            raise TypeError(f"{filename} - Invalid path")
        current_handler["filename"] = filename
    return name
