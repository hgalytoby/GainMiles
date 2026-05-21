from datetime import datetime
from enum import StrEnum

from pydantic import UUID4, BaseModel, Field


class BaseModel(BaseModel):
    model_config = {"from_attributes": True}


class IdMixin:
    id: UUID4 = Field(description="DB ID")


class CreatedAtMixin:
    created_at: datetime = Field(description="創建時間")


class UpdatedAtMixin:
    updated_at: datetime = Field(description="更新時間")


class IdCreatedAtMixin(IdMixin, CreatedAtMixin): ...


class IdUpdatedAtMixin(IdMixin, UpdatedAtMixin): ...


class CreatedAtUpdatedAtMixin(CreatedAtMixin, UpdatedAtMixin): ...


class IdCreatedAtUpdatedAtMixin(IdMixin, CreatedAtMixin, UpdatedAtMixin): ...


class PaginatorResponse[T: BaseModel](BaseModel):
    items: list[T] = Field(description="資料")
    prev: bool = Field(description="上一頁")
    next: bool = Field(description="下一頁")
    total: int = Field(description="總數")
    size: int = Field(description="每頁數量")

    @classmethod
    def build(
        cls,
        items: list[T],
        total: int,
        query: "ApiPageQuery",
    ) -> "PaginatorResponse[T]":
        return cls(
            items=items,
            prev=query.page > 1,
            next=query.page * query.size < total,
            total=total,
            size=query.size,
        )


class SortOrder(StrEnum):
    """
    ASC = 升序
    DESC = 降序
    """

    ASC = "asc"
    DESC = "desc"


class ApiQuery(BaseModel):
    order_by: StrEnum | None = Field(default=None)
    order: SortOrder | None = Field(default=None, description=SortOrder.__doc__)


class ApiPageQuery(BaseModel):
    page: int = Field(default=1, gt=0, description="頁碼")
    size: int = Field(default=20, gt=0, description="每頁數量")
