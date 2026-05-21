from abc import ABCMeta, abstractmethod
from typing import Any

from pydantic import UUID4
from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.interfaces import ORMOption
from sqlalchemy.sql.elements import ColumnElement

from ..models.base import BaseSQL
from ..schemas.base import BaseModel

FiltersType = list[ColumnElement[bool]] | None
OptionsType = list[ORMOption] | None


class BaseRepository[ModelType: BaseSQL](metaclass=ABCMeta):
    def __init__(self, db: AsyncSession):
        self.db = db

    @classmethod
    @abstractmethod
    def get_model(cls) -> type[ModelType]:
        raise NotImplementedError

    @property
    def model(self) -> type[ModelType]:
        return self.get_model()

    def _build_query(
        self,
        filters: FiltersType = None,
        options: OptionsType = None,
    ) -> Select[tuple[ModelType]]:
        stmt = select(self.model)

        if filters:
            stmt = stmt.where(*filters)

        if options:
            stmt = stmt.options(*options)

        return stmt

    async def get_by_id(
        self,
        db_id: UUID4,
        options: OptionsType = None,
    ) -> ModelType | None:
        stmt = self._build_query(
            filters=[self.model.id == db_id],
            options=options,
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(
        self,
        filters: FiltersType = None,
        options: OptionsType = None,
    ) -> list[ModelType]:
        stmt = self._build_query(filters=filters, options=options)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_paginated(
        self,
        page: int,
        size: int,
        filters: FiltersType = None,
        options: OptionsType = None,
    ) -> tuple[list[ModelType], int]:
        stmt = self._build_query(filters=filters, options=options)

        offset = (page - 1) * size

        count_stmt = select(func.count()).select_from(stmt.order_by(None).subquery())

        total_result = await self.db.execute(count_stmt)
        total = total_result.scalar_one()
        result = await self.db.execute(stmt.offset(offset).limit(size))

        items = list(result.scalars().all())
        return items, total

    async def create(
        self,
        obj: ModelType,
        *,
        commit: bool = True,
        refresh: bool = False,
        flush: bool = False,
    ) -> ModelType:
        self.db.add(obj)

        if commit:
            await self.db.commit()
        elif flush:
            await self.db.flush()

        if refresh and (commit or flush):
            await self.db.refresh(obj)

        return obj

    async def update_by_instance(
        self,
        obj: ModelType,
        update_item: dict[str, Any] | BaseModel,
        *,
        commit: bool = True,
        refresh: bool = False,
        flush: bool = False,
    ) -> ModelType:
        if isinstance(update_item, BaseModel):
            update = update_item.model_dump(exclude_unset=True)
        else:
            update = update_item

        for key, value in update.items():
            if hasattr(obj, key):
                setattr(obj, key, value)

        if commit:
            await self.db.commit()
        elif flush:
            await self.db.flush()

        if refresh and (commit or flush):
            await self.db.refresh(obj)

        return obj

    async def delete(
        self,
        obj: ModelType,
        *,
        commit: bool = True,
        flush: bool = False,
    ) -> None:
        await self.db.delete(obj)

        if commit:
            await self.db.commit()
        elif flush:
            await self.db.flush()
