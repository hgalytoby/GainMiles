from ..context import CreateApiContext


def render(ctx: CreateApiContext) -> str:
    return f"""from enum import StrEnum

from pydantic import Field

from .base import ApiPageQuery, ApiQuery, BaseModel, IdCreatedAtUpdatedAtMixin


class Base{ctx.entity_class}(BaseModel): ...


class {ctx.entity_class}Create(Base{ctx.entity_class}): ...


class {ctx.entity_class}Update(Base{ctx.entity_class}): ...


class {ctx.entity_class}Read(IdCreatedAtUpdatedAtMixin, Base{ctx.entity_class}): ...


class {ctx.entity_class}WebRead({ctx.entity_class}Read): ...


class {ctx.entity_class}OrderByEnum(StrEnum):
    ID = "id"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"


class {ctx.entity_class}ApiQuery(ApiQuery): ...


class {ctx.entity_class}ApiPageQuery({ctx.entity_class}ApiQuery, ApiPageQuery):
    order_by: {ctx.entity_class}OrderByEnum | None = Field(default=None, description="排序")
"""
