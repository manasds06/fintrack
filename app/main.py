from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from . import models, transactions
from .database import engine, SessionLocal

# Creates table for data
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root_point():
  return {"message": "API still working?"}

# POST method at /transaction endpoint for user to create and add new transactions they made
@app.post("/transactions/", response_model=schemas.Transaction)
def create_transaction(transaction: schemas.TransactionCreate, db: Session = Depends(get_db)):
    db_transaction = models.TransactionTable(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

# GET method at /transaction endpoint for user to be able to see all transactions made by them
@app.get("/transactions/", response_model=list[schemas.Transaction])
def get_transactions(db: Session = Depends(get_db)):
    return db.query(models.TransactionTable).all()