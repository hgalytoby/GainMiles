from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.database import get_db
from ..schemas.base import PaginatorResponse
from ..schemas.employee import (
    EmployeeApiPageQuery,
    EmployeeCreate,
    EmployeeUpdate,
    EmployeeWebCreated,
    EmployeeWebRead,
)
from ..services.employee import EmployeeService

router = APIRouter(prefix="/employees", tags=["Employee"])


@router.get("", status_code=status.HTTP_200_OK, response_model=PaginatorResponse[EmployeeWebRead])
async def paginated(
    query: EmployeeApiPageQuery = Depends(),
    db: AsyncSession = Depends(get_db),
):
    return await EmployeeService.paginated(query=query, db=db)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=EmployeeWebCreated)
async def create(
    create_item: EmployeeCreate,
    db: AsyncSession = Depends(get_db),
):
    return await EmployeeService.create(create_item=create_item, db=db)


@router.get("/{employee_id}", status_code=status.HTTP_200_OK, response_model=EmployeeWebRead)
async def get_by_id(
    employee_id: str,
    db: AsyncSession = Depends(get_db),
):
    return await EmployeeService.get_by_id(employee_id=employee_id, db=db)


@router.patch("/{employee_id}", status_code=status.HTTP_200_OK, response_model=EmployeeWebRead)
async def update_by_id(
    employee_id: str,
    update_item: EmployeeUpdate,
    db: AsyncSession = Depends(get_db),
):
    return await EmployeeService.update_by_id(
        employee_id=employee_id, db=db, update_item=update_item
    )


@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_by_id(employee_id: str, db: AsyncSession = Depends(get_db)):
    await EmployeeService.delete_by_id(employee_id=employee_id, db=db)
