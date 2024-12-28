from dataclasses import dataclass
from enum import StrEnum, auto


@dataclass
class PaginationParams:
    offset: int
    limit: int


class SortOrder(StrEnum):
    ASC = auto()
    DESC = auto()


class SearchFilterTypes(StrEnum):
    ID = auto()
    USERNAME = auto()


@dataclass
class SearchFilters:
    order_by: SearchFilterTypes | None = None
    order: SortOrder | None = None
