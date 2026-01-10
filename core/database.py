from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession

from core.configs import settings
# Database engine -> UTILIZADO PARA PRODUÇÃO
# engine: AsyncEngine = create_async_engine(settings.DB_URL)

# Database engine -> UTILIZADO PARA TESTES/DESENVOLVIMENTO
engine: AsyncEngine = create_async_engine(
    settings.DB_URL, 
    connect_args={"check_same_thread": False}
)

Session: AsyncSession = sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession,
    bind=engine
)