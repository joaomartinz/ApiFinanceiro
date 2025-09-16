from sqlalchemy.orm import Session
from . import models, schemas
import pandas as pd
from datetime import datetime, date

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

def relatorio_saldo_mensal(db: Session):
    receitas = db.query(models.Receita).all()
    despesas = db.query(models.Despesa).all()

    df_receitas = pd.DataFrame([r.__dict__ for r in receitas])
    df_despesas = pd.DataFrame([d.__dict__ for d in despesas])

    if df_receitas.empty and df_despesas.empty:
        return {}

    if not df_receitas.empty:
        df_receitas['data'] = pd.to_datetime(df_receitas['data'])
        receita_mensal = df_receitas.groupby(df_receitas['data'].dt.to_period('M'))['valor'].sum()
    else:
        receita_mensal = pd.Series(dtype=float)

    if not df_despesas.empty:
        df_despesas['data'] = pd.to_datetime(df_despesas['data'])
        despesa_mensal = df_despesas.groupby(df_despesas['data'].dt.to_period('M'))['valor'].sum()
    else:
        despesa_mensal = pd.Series(dtype=float)

    saldo = pd.DataFrame({
        'Receitas': receita_mensal,
        'Despesas': despesa_mensal
    }).fillna(0)
    saldo['Saldo'] = saldo['Receitas'] - saldo['Despesas']

    saldo.index = saldo.index.astype(str)

    resultado = {str(idx): row.to_dict() for idx, row in saldo.iterrows()}

    return resultado


def relatorio_categoria(db: Session, tipo='receita'):
    if tipo == 'receita':
        dados = db.query(models.Receita).all()
    else:
        dados = db.query(models.Despesa).all()

    df = pd.DataFrame([d.__dict__ for d in dados])
    df['valor'] = df['valor'].astype(float)

    cat = df.groupby('categoria')['valor'].sum().to_dict()
    return cat

def update_receita(db: Session, receita_id: int, receita: schemas.ReceitaUpdate):
    db_receita = db.query(models.Receita).filter(models.Receita.id == receita_id).first()
    if not db_receita:
        return None
    
    dados = receita.model_dump(exclude_unset=True)

    for key, value in dados.items():
        if key == "data" and value is not None:
            if isinstance(value, datetime):
                value.date()
            elif isinstance(value, date):
                value = value
        setattr(db_receita, key, value)
    db.commit()
    db.refresh(db_receita)
    return db_receita

def delete_receita(db: Session, receita_id: int):
    db_receita = db.query(models.Receita).filter(models.Receita.id == receita_id).first()
    if not db_receita:
        return None
    db.delete(db_receita)
    db.commit()
    return db_receita

def update_despesa(db: Session, despesa_id: int, despesa: schemas.DespesaUpdate):
    db_despesa = db.query(models.Despesa).filter(models.Despesa.id == despesa_id).first()
    if not db_despesa:
        return None
    
    dados = despesa.model_dump(exclude_unset=True)

    for key, value in dados.items():
        if key == "data" and value is not None:
            if isinstance(value, datetime):
                value.date()
            elif isinstance(value, date):
                value = value
        setattr(db_despesa, key, value)
    db.commit()
    db.refresh(db_despesa)
    return db_despesa
  
def delete_despesa(db: Session, despesa_id: int):
    db_despesa = db.query(models.Despesa).filter(models.Despesa.id == despesa_id).first()
    if not db_despesa:
        return None
    db.delete(db_despesa)
    db.commit()
    return db_despesa


