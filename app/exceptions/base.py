from enum import StrEnum
from http import HTTPStatus


class AppException(Exception):
    def __init__(
        self,
        *,
        error_code: StrEnum,
        msg: str = "",
        status_code: int = HTTPStatus.BAD_REQUEST,
    ):
        super().__init__(msg)
        self.error_code = error_code
        self.status_code = status_code
        self.msg = msg
