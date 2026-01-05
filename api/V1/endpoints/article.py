from typing import List

from fastapi import APIRouter, HTTPException, status, Depends, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.article_models import ArticleModel
from models.user_models import UserModel
from schemas.article_schema import ArticleSchema, ArticleSchemaCreateUpdate
from core.deps import get_current_user, get_session

router = APIRouter()

# POST Artigo
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ArticleSchema,)
async def post_article(article: ArticleSchemaCreateUpdate, user_login: UserModel = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    new_article: ArticleModel = ArticleModel(
        titulo=article.titulo,
        url_fonte=article.url_fonte,
        descricao=article.descricao,
        usuario_id=int(user_login.id)
    )

    db.add(new_article)
    await db.commit()

    return new_article

# GET Artigos
@router.get("/", response_model=List[ArticleSchema])
async def get_articles(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ArticleModel)
        result = await session.execute(query)
        articles: List[ArticleModel] = result.scalars().unique().all()

        return articles


# GET Artigo por ID
@router.get("/{article_id}", response_model=ArticleSchema, status_code=status.HTTP_200_OK)
async def get_article(article_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ArticleModel).filter(ArticleModel.id == article_id)
        result = await session.execute(query)
        article: ArticleModel = result.scalars().unique().one_or_none()

        if article:
            return article
        
        else:
            raise HTTPException(detail="Artigo não encontrado", 
                                status_code=status.HTTP_404_NOT_FOUND)

# PUT Artigo
@router.put("/{article_id}", response_model=ArticleSchema, status_code=status.HTTP_202_ACCEPTED)
async def put_article(article_id: int, article: ArticleSchemaCreateUpdate, db: AsyncSession = Depends(get_session), user_login: UserModel = Depends(get_current_user)):
    async with db as session:
        query = select(ArticleModel).filter(ArticleModel.id == article_id)
        result = await session.execute(query)
        article_to_update: ArticleModel = result.scalars().unique().one_or_none()

        if article_to_update:
            if article.titulo:
                article_to_update.titulo = article.titulo
            if article.url_fonte:
                article_to_update.url_fonte = article.url_fonte
            if article.descricao:
                article_to_update.descricao = article.descricao
            if user_login.id != article_to_update.usuario_id:
                article_to_update.usuario_id = user_login.id

            await session.commit()
            return article_to_update
        else:
            raise HTTPException(detail="Artigo não encontrado", 
                                status_code=status.HTTP_404_NOT_FOUND)
        
# DELETE Artigo
@router.delete("/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_article(article_id: int, db: AsyncSession = Depends(get_session), user_login: UserModel = Depends(get_current_user)):
    async with db as session:
        query = select(ArticleModel).filter(ArticleModel.id == article_id).filter(ArticleModel.usuario_id == user_login.id)
        result = await session.execute(query)
        article_to_delete: ArticleModel = result.scalars().unique().one_or_none()

        if article_to_delete:
            await session.delete(article_to_delete)
            await session.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail="Artigo não encontrado", 
                                status_code=status.HTTP_404_NOT_FOUND)