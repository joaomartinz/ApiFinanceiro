from pydantic import BaseModel
from datetime import date
from typing import Optional


class ReceitaBase(BaseModel):
    descricao: str
    valor: float
    data: Optional[date] = None
    categoria: Optional[str] = None

class ReceitaCreate(ReceitaBase):
    pass

class Receita(ReceitaBase):
    id: int 
    class Config:
        orm_mode = True

class DespesaBase(BaseModel):
    descricao: str
    valor: float
    data: Optional[date] = None
    categoria: Optional[str] = None

class DespesaCreate(DespesaBase):
    pass 

class Despesa(DespesaBase):
    id: int
    class Config:
        orm_mode = True

class ReceitaUpdate(BaseModel):
    descricao: Optional[str] = None
    valor: Optional[float] = None
    data: Optional[date] = None
    categoria: Optional[str] = None
    
class DespesaUpdate(BaseModel):
    descricao: Optional[str] = None
    valor: Optional[float] = None
    data: Optional[date] = None
    categoria: Optional[str] = None
    