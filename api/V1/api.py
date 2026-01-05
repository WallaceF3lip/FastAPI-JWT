from fastapi import APIRouter

from api.V1.endpoints import user
from api.V1.endpoints import article

api_router = APIRouter()

api_router.include_router(user.router, prefix="/users", tags=["users"])
api_router.include_router(article.router, prefix="/articles", tags=["articles"])