from ..context import CreateApiContext


def render(ctx: CreateApiContext) -> str:
    return f"""from ..models.{ctx.entity_module} import {ctx.entity_class}Model
from ..schemas.{ctx.entity_module} import {ctx.entity_class}WebRead


class {ctx.entity_class}Factory:
    @classmethod
    def build_web_read(cls, obj: {ctx.entity_class}Model) -> {ctx.entity_class}WebRead:
        return {ctx.entity_class}WebRead.model_validate(obj)

    @classmethod
    def build_web_read_items(cls, items: list[{ctx.entity_class}Model]) -> list[{ctx.entity_class}WebRead]:
        return [cls.build_web_read(obj=item) for item in items]
"""
