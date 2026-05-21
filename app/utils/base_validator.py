from ..exceptions.base import AppException
from ..exceptions.error_codes import CommonErrorCodeEnum
from ..models import BaseSQL


class BaseValidator:
    @classmethod
    def db_exist(cls, obj: BaseSQL | None):
        if not obj:
            raise AppException(
                status_code=404,
                error_code=CommonErrorCodeEnum.NOT_FOUND,
                msg="Not Found",
            )
