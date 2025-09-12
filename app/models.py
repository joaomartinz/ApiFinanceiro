from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Receita(Base):
    __tablename__ = "receitas"
    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String, index=True)
    valor = Column(Float, nullable=False)
    data = Column(Date, nullable=False)
    categoria = Column(String, nullable=True)

class Despesa(Base):
    __tablename__ = "despesas"
    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String, index=True)
    valor = Column(Float, nullable=False)
    data = Column(Date, nullable=False)
    categoria = Column(String, nullable=True)

