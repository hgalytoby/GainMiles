from datetime import date
from enum import StrEnum

from pydantic import Field

from .base import ApiPageQuery, ApiQuery, BaseModel, CreatedAtUpdatedAtMixin


class BaseEmployee(BaseModel):
    employee_id: str = Field(..., description="員工 ID")
    name: str = Field(..., description="姓名")
    email: str = Field(..., description="電子郵件")
    department: str = Field(..., description="部門")
    salary: int = Field(..., description="薪資")
    join_date: date = Field(..., description="入職日期")


class EmployeeCreate(BaseEmployee):
    join_date: str = Field(..., description="入職日期")


class EmployeeUpdate(BaseModel):
    name: str | None = Field(default=None, description="姓名")
    email: str | None = Field(default=None, description="電子郵件")
    department: str | None = Field(default=None, description="部門")
    salary: int | None = Field(default=None, description="薪資")
    join_date: str | None = Field(default=None, description="入職日期")


class EmployeeRead(CreatedAtUpdatedAtMixin, BaseEmployee):
    pass


class EmployeeWebRead(EmployeeRead):
    pass


class EmployeeWebCreated(BaseModel):
    id: str = Field(validation_alias="employee_id")
    status: str = Field(default="created")


class EmployeeOrderByEnum(StrEnum):
    EMPLOYEE_ID = "employee_id"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"


class EmployeeApiQuery(ApiQuery):
    pass


class EmployeeApiPageQuery(EmployeeApiQuery, ApiPageQuery):
    order_by: EmployeeOrderByEnum | None = Field(default=None, description="排序")
