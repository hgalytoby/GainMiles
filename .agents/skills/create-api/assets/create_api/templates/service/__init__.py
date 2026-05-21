from ...context import CreateApiContext


def render(ctx: CreateApiContext) -> str:
    return f"""from .error_codes import {ctx.entity_class}ErrorCode
from .service import {ctx.entity_class}Service
from .validator import {ctx.entity_class}Validator


__all__ = [
    "{ctx.entity_class}ErrorCode",
    "{ctx.entity_class}Service",
    "{ctx.entity_class}Validator",
]
"""
