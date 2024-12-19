from abc import abstractmethod
from typing import Protocol
import logging


class HandlerProtocol(Protocol):
    @abstractmethod
    def emit(self, record: logging.LogRecord) -> None: ...
