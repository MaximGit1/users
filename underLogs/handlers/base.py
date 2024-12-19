from enum import StrEnum

from underLogs.handlers.json_handler import JsonHandler


class HandlerClasses(StrEnum):
    ConsoleHandler = "logging.StreamHandler"
    FileHandler = "logging.FileHandler"
    JsonHandler = "underLogs.handlers.json_handler.JsonHandler"
