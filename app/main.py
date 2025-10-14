from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from .table_models import transaction_model
from .validation_schemas import transactions
from .core.database import engine, SessionLocal

# Creates table for data
transaction_model.Base.metadata.create_all(bind=engine)

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
@app.post("/transactions/", response_model=transaction_model.Transaction)
def create_transaction(transaction: transaction_model.TransactionCreate, db: Session = Depends(get_db)):
    db_transaction = transaction_model.TransactionTable(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

# GET method at /transaction endpoint for user to be able to see all transactions made by them
@app.get("/transactions/", response_model=list[transactions.Transaction])
def get_transactions(db: Session = Depends(get_db)):
    return db.query(transaction_model.TransactionTable).all()

# GET method at /transaction endpoint for user to be able to see specific transactions made by them
@app.get("/transactions/{transaction_id}", response_model=transactions.Transaction)
def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction = db.query(transaction_model.TransactionTable).filter(transaction_model.TransactionTable.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction

# PUT method at /transaction endpoint for user to be able to update transactions details
@app.put("/transactions/{transaction_id}", response_model=transactions.Transaction)
def update_transaction(transaction_id: int, updated_data: transactions.TransactionCreate, db: Session = Depends(get_db)):
    transaction = db.query(transaction_model.TransactionTable).filter(transaction_model.TransactionTable.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    for key, value in updated_data.dict().items():
        setattr(transaction, key, value)

    db.commit()
    db.refresh(transaction)
    return transaction

# DELETE method at /transaction endpoint for user to be able to remove/delete specific transactions
@app.delete("/transactions/{transaction_id}")
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction = db.query(transaction_model.TransactionTable).filter(transaction_model.TransactionTable.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    db.delete(transaction)
    db.commit()
    return {"message": "Transaction deleted successfully"}
