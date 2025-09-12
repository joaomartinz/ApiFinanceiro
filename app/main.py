from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app import crud, schemas, database, models


app = FastAPI(title="Api - Controle Financeiro Pessoal")

def get_db():
    db = database.SessionLocal()
    try:
        yield db

    finally:
        db.close()

@app.post("/receitas/", response_model=schemas.Receita)
def criar_receita(receita: schemas.ReceitaCreate, db: Session = Depends(get_db)):
    return crud.create_receita(db=db, receita=receita)

@app.post("/despesas/", response_model=schemas.Despesa)
def criar_despesa(despesa: schemas.DespesaCreate, db: Session = Depends(get_db)):
    return crud.create_despesa(db=db, despesa=despesa)

@app.get("/receitas/", response_model=list[schemas.Receita])
def listar_receitas(db: Session = Depends(get_db)):
    return crud.get_receitas(db=db)

@app.get("/despesas/", response_model=list[schemas.Despesa])
def listar_despesas(db: Session = Depends(get_db)):
    return crud.get_despesas(db=db)