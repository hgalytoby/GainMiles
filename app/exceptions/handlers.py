from fastapi import FastAPI, Request, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from starlette.responses import JSONResponse

from . import CommonErrorCodeEnum
from .base import AppException


async def app_exception_handler(
    request: Request,
    exc: AppException,
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": {
                "error_code": str(exc.error_code),
                "message": exc.msg,
            },
        },
    )


async def integrity_error_handler(
    request: Request,
    exc: IntegrityError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "detail": {
                "error_code": CommonErrorCodeEnum.DB_INTEGRITY_ERROR,
                "message": "database integrity error",
            }
        },
    )


async def sqlalchemy_error_handler(
    request: Request,
    exc: SQLAlchemyError,
) -> JSONResponse:
    print(exc)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": {
                "error_code": CommonErrorCodeEnum.DB_ERROR,
                "message": "database error",
            },
        },
    )
