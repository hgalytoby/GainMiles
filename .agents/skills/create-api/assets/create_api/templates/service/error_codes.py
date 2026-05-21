from ...context import CreateApiContext


def render(ctx: CreateApiContext) -> str:
    entity_upper = ctx.entity_name.upper()
    return f"""from enum import StrEnum, auto


class {ctx.entity_class}ErrorCode(StrEnum):
    {entity_upper}_NOT_FOUND = auto()
    # Add one specific error code for each validator failure.
"""
