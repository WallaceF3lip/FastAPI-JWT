from typing import List

from pydantic import BaseSettings
from sqlalchemy.ext.declarative import declarative_base

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    DB_URL: str = "sqlite:///./test.db"
    DBBaseModel = declarative_base()

    JWT_SECRET: str = "eIgUH-7K5ps-5XiTOeX9MCrE0hi9B1l-Acd9fLnBCH0"
    """
    Chave secreta para codificação e decodificação do JWT
    -----------------------------------------------------
    import secrets

    token: str = secrets.token_urlsafe(32)
    -> eIgUH-7K5ps-5XiTOeX9MCrE0hi9B1l-Acd9fLnBCH0
    -------------------------------------
    """
    JWT_ALGORITHM: str = "HS256"
    # 60 MIN. * 24 HRS. * 7 DIAS = 1 SEMANA
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    class Config:
        case_sensitive = True

settings: Settings = Settings()