from ...context import CreateApiContext


def render(ctx: CreateApiContext) -> str:
    return f"""from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ...factories.{ctx.entity_module} import {ctx.entity_class}Factory
from ...models.{ctx.entity_module} import {ctx.entity_class}Model
from ...repositories.{ctx.entity_module} import {ctx.entity_class}Repository
from ...schemas.base import PaginatorResponse
from ...schemas.{ctx.entity_module} import (
    {ctx.entity_class}ApiPageQuery,
    {ctx.entity_class}Create,
    {ctx.entity_class}Update,
    {ctx.entity_class}WebRead,
)
from ...services.{ctx.entity_module}.validator import {ctx.entity_class}Validator


class {ctx.entity_class}Service:
    @classmethod
    async def paginated(cls, query: {ctx.entity_class}ApiPageQuery, db: AsyncSession):
        items, total = await {ctx.entity_class}Repository(db=db).get_paginated(
            page=query.page,
            size=query.size,
        )
        web_read_items = {ctx.entity_class}Factory.build_web_read_items(items=items)
        return PaginatorResponse.build(
            items=web_read_items,
            total=total,
            query=query,
        )

    @classmethod
    async def get_by_id(cls, db_id: UUID4, db: AsyncSession) -> {ctx.entity_class}WebRead:
        obj = await {ctx.entity_class}Repository(db=db).get_by_id(db_id=db_id)

        {ctx.entity_class}Validator.get_by_id(obj=obj)

        web_read = {ctx.entity_class}Factory.build_web_read(obj=obj)
        return web_read

    @classmethod
    async def create(
        cls,
        create_item: {ctx.entity_class}Create,
        db: AsyncSession,
    ) -> {ctx.entity_class}WebRead:
        {ctx.entity_class}Validator.create(create_item=create_item)

        db_item = {ctx.entity_class}Model(**create_item.model_dump())
        obj = await {ctx.entity_class}Repository(db=db).create(obj=db_item, refresh=True)

        web_read = {ctx.entity_class}Factory.build_web_read(obj=obj)
        return web_read

    @classmethod
    async def update_by_id(
        cls,
        db_id: UUID4,
        db: AsyncSession,
        update_item: {ctx.entity_class}Update,
    ):
        obj = await {ctx.entity_class}Repository(db=db).get_by_id(db_id=db_id)

        {ctx.entity_class}Validator.update(obj=obj, update_item=update_item)

        data = update_item.model_dump(exclude_unset=True)
        obj = await {ctx.entity_class}Repository(db=db).update_by_instance(obj=obj, update_item=data)

        web_read = {ctx.entity_class}Factory.build_web_read(obj=obj)
        return web_read

    @classmethod
    async def delete_by_id(cls, db_id: UUID4, db: AsyncSession):
        repository = {ctx.entity_class}Repository(db=db)

        obj = await {ctx.entity_class}Repository(db=db).get_by_id(db_id=db_id)

        {ctx.entity_class}Validator.delete(obj=obj)

        await repository.delete(obj=obj)
"""
