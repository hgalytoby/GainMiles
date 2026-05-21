from enum import StrEnum, auto


class EmployeeErrorCode(StrEnum):
    NOT_FOUND = auto()
    ID_REQUIRED = auto()
    ID_ALREADY_EXISTS = auto()
    NAME_REQUIRED = auto()
    NAME_INVALID_FORMAT = auto()
    EMAIL_REQUIRED = auto()
    EMAIL_INVALID_FORMAT = auto()
    DEPARTMENT_REQUIRED = auto()
    DEPARTMENT_INVALID_FORMAT = auto()
    SALARY_REQUIRED = auto()
    SALARY_MUST_BE_POSITIVE = auto()
    JOIN_DATE_REQUIRED = auto()
    JOIN_DATE_INVALID_FORMAT = auto()
