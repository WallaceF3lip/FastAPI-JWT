from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from core.configs import settings

class ArticleModel(settings.DBBaseModel):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(256), nullable=False)
    url_fonte = Column(String(256), nullable=False)
    descricao = Column(String(256), nullable=False)
    usuario_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    criador = relationship(
        "UserModel", back_populates="articles", lazy="joined")