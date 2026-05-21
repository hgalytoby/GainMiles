from ...context import CreateApiContext


def render(ctx: CreateApiContext) -> str:
    return f"""from ...models.{ctx.entity_module} import {ctx.entity_class}Model
from ...schemas.{ctx.entity_module} import {ctx.entity_class}Create, {ctx.entity_class}Update
from ...utils.base_validator import BaseValidator
from .error_codes import {ctx.entity_class}ErrorCode


class {ctx.entity_class}Validator(BaseValidator):
    @classmethod
    def get_by_id(cls, obj: {ctx.entity_class}Model | None):
        cls.db_exist(obj=obj)

    @classmethod
    def create(cls, create_item: {ctx.entity_class}Create):
        # Add create validation here when the rule needs project-specific error codes,
        # database/service context, or reusable business validation.
        # Pydantic Field constraints and validators are allowed in schemas when appropriate.
        # When adding a validation failure here, also add a matching member to {ctx.entity_class}ErrorCode.
        ...

    @classmethod
    def update(cls, update_item: {ctx.entity_class}Update, obj: {ctx.entity_class}Model | None):
        cls.db_exist(obj=obj)
        # Add update validation here when the rule needs project-specific error codes,
        # database/service context, or reusable business validation.
        # Validate only fields that are not None / were provided by the caller.
        ...

    @classmethod
    def delete(cls, obj: {ctx.entity_class}Model | None):
        cls.db_exist(obj=obj)
"""
