from datetime import date

from sqlalchemy import Date, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseSQL


class EmployeeModel(BaseSQL):
    __tablename__ = "employees"

    id = None  # type: ignore
    employee_id: Mapped[str] = mapped_column(String(50), primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    department: Mapped[str] = mapped_column(String(100), nullable=False)
    salary: Mapped[int] = mapped_column(Integer, nullable=False)
    join_date: Mapped[date] = mapped_column(Date, nullable=False)
