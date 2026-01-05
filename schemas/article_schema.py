from typing import Optional
from pydantic import BaseModel, HttpUrl

class ArticleSchemaCreateUpdate(BaseModel):
    """Schema para CRIAR artigo (sem usuario_id no body)"""
    titulo: str
    descricao: str
    url_fonte: str 

class ArticleSchema(BaseModel):
    id: Optional[int] = None
    titulo: str
    descricao: str
    url_fonte: str
    usuario_id: Optional[int]

    class Config:
        from_attributes = True