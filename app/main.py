from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from .core.database import check_db_connection, engine
from .exceptions import AppException
from .exceptions.handlers import (
    app_exception_handler,
    integrity_error_handler,
    sqlalchemy_error_handler,
)
from .routers import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await check_db_connection(engine_=engine)

    yield

    await engine.dispose()


app = FastAPI(lifespan=lifespan)

app.include_router(router)


app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(IntegrityError, integrity_error_handler)
app.add_exception_handler(SQLAlchemyError, sqlalchemy_error_handler)
