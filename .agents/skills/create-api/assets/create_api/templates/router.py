from ..context import CreateApiContext


def render(ctx: CreateApiContext) -> str:
    return f"""from fastapi import APIRouter, Depends, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.database import get_db
from ...schemas.base import PaginatorResponse
from ...schemas.{ctx.entity_module} import (
    {ctx.entity_class}ApiPageQuery,
    {ctx.entity_class}Create,
    {ctx.entity_class}Update,
    {ctx.entity_class}WebRead,
)
from ...services.{ctx.entity_module} import {ctx.entity_class}Service

router = APIRouter(prefix="/{ctx.api_prefix}", tags=["{ctx.tag}"])


@router.get("", status_code=status.HTTP_200_OK, response_model=PaginatorResponse[{ctx.entity_class}WebRead])
async def paginated(
    query: {ctx.entity_class}ApiPageQuery = Depends(),
    db: AsyncSession = Depends(get_db),
):
    return await {ctx.entity_class}Service.paginated(query=query, db=db)


@router.post("", status_code=status.HTTP_201_CREATED, response_model={ctx.entity_class}WebRead)
async def create(
    create_item: {ctx.entity_class}Create,
    db: AsyncSession = Depends(get_db),
):
    return await {ctx.entity_class}Service.create(create_item=create_item, db=db)


@router.get("/{{db_id}}", status_code=status.HTTP_200_OK, response_model={ctx.entity_class}WebRead)
async def get_by_id(
    db_id: UUID4,
    db: AsyncSession = Depends(get_db),
):
    return await {ctx.entity_class}Service.get_by_id(db_id=db_id, db=db)


@router.patch("/{{db_id}}", status_code=status.HTTP_200_OK, response_model={ctx.entity_class}WebRead)
async def update_by_id(
    db_id: UUID4,
    update_item: {ctx.entity_class}Update,
    db: AsyncSession = Depends(get_db),
):
    return await {ctx.entity_class}Service.update_by_id(db_id=db_id, db=db, update_item=update_item)


@router.delete("/{{db_id}}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_by_id(db_id: UUID4, db: AsyncSession = Depends(get_db)):
    await {ctx.entity_class}Service.delete_by_id(db_id=db_id, db=db)
"""
