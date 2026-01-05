from typing import Optional, List
from pydantic import BaseModel, EmailStr

from schemas.article_schema import ArticleSchema

class UserSchemaBase(BaseModel):
    id: Optional[int] = None
    nome: str
    sobrenome: str
    email: EmailStr
    eh_admin: bool = False

    class Config:
        from_attributes = True

class UserSchemaCreate(UserSchemaBase):
    senha: str

class UserSchemaArticle(UserSchemaBase):
    articles: Optional[List[ArticleSchema]]

class UserSchemaUpdate(UserSchemaBase):
    senha: Optional[str]
    sobrenome: Optional[str]
    email: Optional[EmailStr]
    senha: Optional[str]
    eh_admin: Optional[bool]