from typing import Generator, Optional

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel

from core.database import Session
from core.configs import settings
from core.auth import oauth2_schema
from models.users_model import UsersModel

class TokenData(BaseModel):
    userName: Optional[str] = None

async def get_session() -> Generator:
    session: AsyncSession = Session()

    try:
        yield session
    finally:
        await session.close()

async def get_current_user(
    db: Session = Depends(get_session), 
    token: str = Depends(oauth2_schema)
) -> UsersModel:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )
        user_name: str = payload.get("sub")

        if user_name is None:
            raise credentials_exception

        token_data = TokenData(userName=user_name)
    except JWTError:
        raise credentials_exception

    async with db as session:
        query = select(UsersModel).filter(UsersModel.id == int(token_data.userName))
        result = await session.execute(query)
        user: UsersModel = result.scalars().unique().one_or_none()

        if user is None:
            raise credentials_exception

        return user
   