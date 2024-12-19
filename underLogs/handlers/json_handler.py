import logging


class JsonHandler(logging.Handler):
    def __init__(
        self,
        filename: str,
        level: int = logging.NOTSET,
        formatter: logging.Formatter = None,
    ):
        super().__init__(level)
        self.file_name = filename
        if formatter:
            self.setFormatter(formatter)

    def emit(self, record: logging.LogRecord) -> None:
        try:
            log_entry = self.format(record)
            with open(self.file_name, "a", encoding="utf-8") as f:
                f.write(log_entry + "\n")
        except Exception:
            self.handleError(record)
