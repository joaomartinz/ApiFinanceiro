from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, database

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

@app.get("/relatorio/saldo_mensal")
def saldo_mensal(db: Session = Depends(get_db)):
    return crud.relatorio_saldo_mensal(db=db)

@app.get("/relatorio/receitas_categoria")
def receitas_categoria(db: Session = Depends(get_db)):
    return crud.relatorio_categoria(db=db, tipo="receita")

@app.get("/relatorio/despesas_categoria")
def despesas_categoria(db: Session = Depends(get_db)):
    return crud.relatorio_categoria(db=db, tipo="despesa")

@app.put("/receitas/", response_model=schemas.Receita)
def atualizar_receita(receita_id: int, receita: schemas.ReceitaUpdate, db: Session = Depends(get_db)):
    db_receita = crud.update_receita(db, receita_id, receita)
    if not db_receita:
        raise HTTPException(status_code=404, detail= "Receita não encontrada")
    return db_receita

@app.delete("/receitas/{receita_id}", response_model=schemas.Receita)
def deletar_receita(receita_id: int, db: Session = Depends(get_db)):
    db_receita = crud.delete_receita(db, receita_id)
    if not db_receita:
         raise HTTPException(status_code=404, detail= "Receita não encontrada")
    return db_receita

@app.put("/despesas/", response_model= schemas.Despesa)
def atualizar_despesa(despesa_id: int, despesa: schemas.DespesaUpdate, db: Session = Depends(get_db)):
    db_despesa = crud.update_despesa(db, despesa_id, despesa)
    if not db_despesa:
        raise HTTPException(status_code=404, detail= "Despesa não encontrada")
    return db_despesa

@app.delete("/despesa/{despesa_id}", response_model= schemas.Despesa)
def deletar_despesa(despesa_id: int, db: Session = Depends(get_db)):
    db_despesa = crud.delete_despesa(db, despesa_id)
    if not db_despesa:
        raise HTTPException(status_code=404, detail= "Receita não encontrada")
    return db_despesa


