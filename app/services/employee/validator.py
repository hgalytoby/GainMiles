from datetime import date, datetime
import re

from fastapi import status

from ...exceptions.base import AppException
from ...models.employee import EmployeeModel
from ...schemas.employee import EmployeeCreate, EmployeeUpdate
from ...utils.base_validator import BaseValidator
from .error_codes import EmployeeErrorCode


class EmployeeValidator(BaseValidator):
    @classmethod
    def get_by_employee_id(cls, obj: EmployeeModel | None):
        if not obj:
            raise AppException(
                status_code=status.HTTP_404_NOT_FOUND,
                error_code=EmployeeErrorCode.NOT_FOUND,
                msg="Employee not found.",
            )

    @classmethod
    def create(cls, create_item: EmployeeCreate):
        cls.validate_name(create_item.name)
        cls.validate_email(create_item.email)
        cls.validate_department(create_item.department)
        cls.validate_salary(create_item.salary)
        cls.validate_join_date(create_item.join_date)

    @classmethod
    def update(cls, update_item: EmployeeUpdate, obj: EmployeeModel | None):
        cls.db_exist(obj=obj)

        if update_item.name is not None:
            cls.validate_name(update_item.name)
        if update_item.email is not None:
            cls.validate_email(update_item.email)
        if update_item.department is not None:
            cls.validate_department(update_item.department)
        if update_item.salary is not None:
            cls.validate_salary(update_item.salary)
        if update_item.join_date is not None:
            cls.validate_join_date(update_item.join_date)

    @classmethod
    def delete(cls, obj: EmployeeModel | None):
        cls.db_exist(obj=obj)

    @classmethod
    def validate_name(cls, name: str):
        if not name.strip():
            raise AppException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                error_code=EmployeeErrorCode.NAME_REQUIRED,
                msg="name is required.",
            )

        if name.strip() != name:
            raise AppException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                error_code=EmployeeErrorCode.NAME_INVALID_FORMAT,
                msg="name invalid format.",
            )

        if len(name) < 1 or len(name) > 50:
            raise AppException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                error_code=EmployeeErrorCode.NAME_INVALID_FORMAT,
                msg="name length must be between 1 and 50 characters.",
            )

    @classmethod
    def validate_email(cls, email: str):
        if not email.strip() or email.strip() != email:
            raise AppException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                error_code=EmployeeErrorCode.EMAIL_REQUIRED,
                msg="email is required.",
            )

        if email.strip() != email:
            raise AppException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                error_code=EmployeeErrorCode.EMAIL_INVALID_FORMAT,
                msg="email must be a valid email address format.",
            )

        email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(email_regex, email):
            raise AppException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                error_code=EmployeeErrorCode.EMAIL_INVALID_FORMAT,
                msg="email must be a valid email address format.",
            )

    @classmethod
    def validate_department(cls, department: str):
        if not department.strip():
            raise AppException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                error_code=EmployeeErrorCode.DEPARTMENT_REQUIRED,
                msg="department is required.",
            )
        if department.strip() != department:
            raise AppException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                error_code=EmployeeErrorCode.DEPARTMENT_INVALID_FORMAT,
                msg="department invalid format.",
            )

    @classmethod
    def validate_salary(cls, salary: int):
        if salary <= 0:
            raise AppException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                error_code=EmployeeErrorCode.SALARY_MUST_BE_POSITIVE,
                msg="salary must be a positive integer (> 0).",
            )

    @classmethod
    def validate_join_date(cls, join_date_val: str):
        if not join_date_val.strip():
            raise AppException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                error_code=EmployeeErrorCode.JOIN_DATE_REQUIRED,
                msg="join_date is required.",
            )

        if join_date_val.strip() != join_date_val:
            raise AppException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                error_code=EmployeeErrorCode.JOIN_DATE_INVALID_FORMAT,
                msg="join_date must follow the format YYYY-MM-DD and be a valid calendar date.",
            )

        try:
            datetime.strptime(join_date_val, "%Y-%m-%d").date()
        except ValueError:
            raise AppException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                error_code=EmployeeErrorCode.JOIN_DATE_INVALID_FORMAT,
                msg="join_date must follow the format YYYY-MM-DD and be a valid calendar date.",
            )
