from ..context import CreateApiContext


def render(ctx: CreateApiContext) -> str:
    return f"""from .base import BaseSQL


class {ctx.entity_class}Model(BaseSQL):
    __tablename__ = "{ctx.api_prefix}"
"""
