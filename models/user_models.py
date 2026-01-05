from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from core.configs import settings

class UserModel(settings.DBBaseModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(128))
    sobrenome = Column(String(128))
    email = Column(String(256), unique=True, index=True)
    senha = Column(String(256))
    eh_admin = Column(Boolean, default=False)
    articles = relationship(
        "ArticleModel", cascade="all, delete", back_populates="criador", uselist=True, lazy="joined")