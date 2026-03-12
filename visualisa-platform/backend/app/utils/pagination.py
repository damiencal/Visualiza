from __future__ import annotations

from typing import TypeVar, Generic, Sequence
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class PaginatedResponse(BaseModel, Generic[T]):
    """Standard paginated envelope returned by all list endpoints."""

    items: Sequence[T]
    total: int
    page: int
    page_size: int
    pages: int

    @classmethod
    def build(
        cls,
        items: Sequence[T],
        total: int,
        page: int,
        page_size: int,
    ) -> "PaginatedResponse[T]":
        pages = max(1, -(-total // page_size))  # ceiling division
        return cls(items=items, total=total, page=page, page_size=page_size, pages=pages)


def paginate_query(query, page: int, page_size: int):
    """Apply OFFSET/LIMIT to a SQLAlchemy select statement."""
    offset = (page - 1) * page_size
    return query.offset(offset).limit(page_size)
