from ..context import CreateApiContext


def render(ctx: CreateApiContext) -> str:
    return f"""from ..models.{ctx.entity_module} import {ctx.entity_class}Model
from .base import BaseRepository


class {ctx.entity_class}Repository(BaseRepository[{ctx.entity_class}Model]):
    @classmethod
    def get_model(cls) -> type[{ctx.entity_class}Model]:
        return {ctx.entity_class}Model
"""
