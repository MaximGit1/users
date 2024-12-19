import json
import logging
import traceback
from datetime import datetime


class BaseJsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_record = {
            "level": record.levelname,
            "time": self.format_time(record),
            "name": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "funcName": record.funcName,
            "lineno": record.lineno,
        }

        if record.exc_info:
            log_record["exc_info"] = "".join(
                traceback.format_exception(*record.exc_info)
            )

        return json.dumps(log_record, ensure_ascii=False)

    @staticmethod
    def format_time(record: logging.LogRecord) -> datetime.fromtimestamp:
        return datetime.fromtimestamp(record.created).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
