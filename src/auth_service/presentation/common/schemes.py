from pydantic import BaseModel, Field

from auth_service.application.common.request_response_models import (
    PaginationParams as ApplicationPaginationParams,
)


class PaginationParams(BaseModel):
    offset: int = Field(0, ge=0, description="Offset for the query")
    limit: int = Field(10, ge=1, le=60, description="Limit for the query")

    def to_model(self) -> ApplicationPaginationParams:
        return ApplicationPaginationParams(
            offset=self.offset,
            limit=self.limit,
        )
