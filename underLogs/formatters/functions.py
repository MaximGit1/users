from underLogs.formatters import DefaultFormatters, JsonFormatters


def add_formatter(
    logger_config, name: str, format_string: str | DefaultFormatters
) -> str:
    logger_config["formatters"][name] = {
        "format": format_string
        if type(format_string) is str
        else format_string.value,
        "style": "{",
    }
    return name


def add_json_formatter(
    logger_config, name: str, formatter: JsonFormatters
) -> str:
    logger_config["formatters"][name] = {
        "()": f"{formatter.value.__module__}.{formatter.value.__name__}"  # Квалифицированное имя класса
    }
    return name
