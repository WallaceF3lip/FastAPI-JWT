from typing import List, Optional, Any

from fastapi import APIRouter, HTTPException, status, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm 
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from models.user_models import UserModel
from schemas.user_schema import UserSchemaBase, UserSchemaCreate, UserSchemaArticle, UserSchemaUpdate
from core.deps import get_current_user, get_session
from core.security import verify_password, generate_hashed_password
from core.auth import authenticate, create_access_token

router = APIRouter()

# GET Logado
@router.get("/logado", response_model=UserSchemaBase)
def get_logged_user(user_login: UserModel = Depends(get_current_user)):
    return user_login

# POST Login
@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=UserSchemaBase)
async def create_user(user: UserSchemaCreate, db: AsyncSession = Depends(get_session)):
    new_user: UserModel = UserModel(
        nome=user.nome,
        sobrenome=user.sobrenome,
        email=user.email,
        senha=generate_hashed_password(user.senha),
        eh_admin=user.eh_admin
    )
    async with db as session:
        try:
            session.add(new_user)
            await session.commit()

            return new_user
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="Já existe um usuário com esse e-mail cadastrado."
            )

# GET Usuários
@router.get("/", response_model=List[UserSchemaBase], status_code=status.HTTP_200_OK)
async def get_users(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UserModel)
        result = await session.execute(query)
        users: List[UserSchemaBase] = result.scalars().unique().all()

        return users
    
# GET Usuário por ID
@router.get("/{user_id}", response_model=UserSchemaArticle, status_code=status.HTTP_200_OK)
async def get_user_by_id(user_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UserModel).filter(UserModel.id == user_id)
        result = await session.execute(query)
        user: UserModel = result.scalars().unique().one_or_none()

        if user:
            return user
        
        else:
            raise HTTPException(detail="Usuário não encontrado", 
                                status_code=status.HTTP_404_NOT_FOUND)
        
# PUT Usuário
@router.put("/{user_id}", response_model=UserSchemaBase, status_code=status.HTTP_202_ACCEPTED)
async def put_user(user_id: int, user: UserSchemaUpdate, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UserModel).filter(UserModel.id == user_id)
        result = await session.execute(query)
        user_to_update: UserSchemaBase = result.scalars().unique().one_or_none()

        if user_to_update:
            if user.nome:
                user_to_update.nome = user.nome
            if user.sobrenome:
                user_to_update.sobrenome = user.sobrenome
            if user.email:
                user_to_update.email = user.email
            if user.eh_admin is not None:
                user_to_update.eh_admin = user.eh_admin
            if user.senha:
                user_to_update.senha = generate_hashed_password(user.senha)

            await session.commit()

            return user_to_update
        
        else:
            raise HTTPException(detail="Usuário não encontrado", 
                                status_code=status.HTTP_404_NOT_FOUND)
        
# DELETE Usuário
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_session)):    
    async with db as session:
        query = select(UserModel).filter(UserModel.id == user_id)
        result = await session.execute(query)
        user_to_delete: UserSchemaArticle = result.scalars().unique().one_or_none()

        if user_to_delete:
            await session.delete(user_to_delete)
            await session.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail="Usuário não encontrado", 
                                status_code=status.HTTP_404_NOT_FOUND)
        
# POST Login - Token
@router.post("/login", status_code=status.HTTP_200_OK)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    user = await authenticate(email=form_data.username, password=form_data.password, db=db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Dados de login incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return JSONResponse(
        content={
            "access_token": create_access_token(sub=user.id),
            "token_type": "bearer",
        },
        status_code=status.HTTP_200_OK
    )