from underLogs.configuration import logger_config, setup_config
from underLogs.levels import Levels
from underLogs.formatters import JsonFormatters, add_json_formatter
from underLogs.handlers import HandlerClasses, add_handler
from underLogs.loggers import add_logger


def my_json(config=logger_config):
    formatter = add_json_formatter(
        name="my_json_formatter",
        logger_config=config,
        formatter=JsonFormatters.BaseJSONFORMATTER,
    )
    handler = add_handler(
        name="my_json_handler",
        level=Levels.WARNING,
        formatter=formatter,
        class_=HandlerClasses.JsonHandler,
        filename="C:/Users/user/PycharmProjects/AuthService/logs.json",
        logger_config=config,
    )
    add_logger(
        config, level=Levels.WARNING, handlers=[handler], name="my_json_logger"
    )


setup_config(my_json, config=logger_config)
