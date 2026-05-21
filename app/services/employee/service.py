from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from ...factories.employee import EmployeeFactory
from ...models.employee import EmployeeModel
from ...repositories.employee import EmployeeRepository
from ...schemas.base import PaginatorResponse
from ...schemas.employee import (
    EmployeeApiPageQuery,
    EmployeeCreate,
    EmployeeUpdate,
    EmployeeWebCreated,
    EmployeeWebRead,
)
from ...services.employee.validator import EmployeeValidator


class EmployeeService:
    @classmethod
    async def paginated(cls, query: EmployeeApiPageQuery, db: AsyncSession):
        items, total = await EmployeeRepository(db=db).get_paginated(
            page=query.page,
            size=query.size,
        )
        web_read_items = EmployeeFactory.build_web_read_items(items=items)
        return PaginatorResponse.build(
            items=web_read_items,
            total=total,
            query=query,
        )

    @classmethod
    async def get_by_id(cls, employee_id: str, db: AsyncSession) -> EmployeeWebRead:
        obj = await EmployeeRepository(db=db).get_by_employee_id(employee_id=employee_id)

        EmployeeValidator.get_by_employee_id(obj=obj)

        web_read = EmployeeFactory.build_web_read(obj=obj)
        return web_read

    @classmethod
    async def create(
        cls,
        create_item: EmployeeCreate,
        db: AsyncSession,
    ) -> EmployeeWebCreated:
        EmployeeValidator.create(create_item=create_item)

        db_item = EmployeeModel(
            **create_item.model_dump()
            | {"join_date": datetime.strptime(create_item.join_date, "%Y-%m-%d").date()}
        )
        obj = await EmployeeRepository(db=db).create(obj=db_item, refresh=True)

        web_read = EmployeeFactory.build_web_read(obj=obj)
        return web_read

    @classmethod
    async def update_by_id(
        cls,
        employee_id: str,
        db: AsyncSession,
        update_item: EmployeeUpdate,
    ):
        repository = EmployeeRepository(db=db)

        obj = await repository.get_by_employee_id(employee_id=employee_id)

        EmployeeValidator.update(obj=obj, update_item=update_item)

        data = update_item.model_dump(exclude_unset=True)
        obj = await repository.update_by_instance(obj=obj, update_item=data)

        web_read = EmployeeFactory.build_web_read(obj=obj)
        return web_read

    @classmethod
    async def delete_by_id(cls, employee_id: str, db: AsyncSession):
        repository = EmployeeRepository(db=db)

        obj = await repository.get_by_employee_id(employee_id=employee_id)

        EmployeeValidator.delete(obj=obj)

        await repository.delete(obj=obj)
