from sqlalchemy.orm import Session
from . import models, schemas

def get_receitas(db: Session):
    return db.query(models.Receita).all()

def create_receita(db: Session, receita: schemas.ReceitaCreate):
    db_receita = models.Receita(**receita.model_dump())
    db.add(db_receita)
    db.commit()
    db.refresh(db_receita)
    return db_receita

def get_despesas(db: Session):
    return db.query(models.Despesa).all()

def create_despesa(db: Session, despesa: schemas.DespesaCreate):
    db_despesa = models.Despesa(**despesa.model_dump())
    db.add(db_despesa)
    db.commit()
    db.refresh(db_despesa)
    return db_despesa