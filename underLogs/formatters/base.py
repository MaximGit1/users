from enum import StrEnum, Enum, EnumMeta
# from abc import ABC

from underLogs.formatters.json_formatter import BaseJsonFormatter


class AbstractFormatter:
    pass


class DefaultFormatters(StrEnum):
    TimeLevelNameMessage = "{asctime} [{levelname}] {name}: {message}'"
    LevelNameMessage = "{levelname} - {name} - '{message}'"
    TimeLevelNameModuleFunctionLineMessage = "{asctime} [{levelname}] {name} - {module}:[func {funcName}]:{lineno} - {message}'"


class JsonFormatters(Enum):
    BaseJSONFORMATTER = BaseJsonFormatter
