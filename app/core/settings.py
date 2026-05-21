from enum import StrEnum
import os

from pydantic import Field
from pydantic_settings import BaseSettings


class AppEnvPath(StrEnum):
    """
    PROD = 正式環境
    DEV = 開發環境
    TEST = 測試環境
    """

    PROD = ".env"
    DEV = ".env.dev"
    TEST = ".env.test"


class AppEnv(StrEnum):
    """
    PROD = 正式環境
    DEV = 開發環境
    TEST = 測試環境
    """

    PROD = "PROD"
    DEV = "DEV"
    TEST = "TEST"


MODE = os.getenv("MODE", default=AppEnv.DEV)


class Settings(BaseSettings):
    SQL_URL: str = Field(description="DB URL")

    class Config:
        env_file = AppEnvPath[MODE]


settings = Settings()
