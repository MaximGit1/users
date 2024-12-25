from pydantic import BaseModel, Field


class PaginationParams(BaseModel):
    offset: int = Field(1, ge=1, description="Offset for the query")
    limit: int = Field(10, ge=1, le=60, description="Limit for the query")
