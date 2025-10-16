from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..core.security import get_current_user
from ..table_models.transaction_model import TransactionTable
from ..table_models.budget_model import BudgetTable
from ..table_models.user_model import UserTable
from ..validation_schemas.transactions import Transaction, TransactionCreate

# Creates a mini API
router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"]
)

# POST method at /transaction endpoint for user to create and add new transactions they made
@router.post("/", response_model=Transaction)
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db), current_user: UserTable = Depends(get_current_user)):
    db_transaction = TransactionTable(**transaction.dict(), user_id=current_user.id)
    db.add(db_transaction)

    budget = db.query(BudgetTable).filter(BudgetTable.user_id == current_user.id, BudgetTable.category == db_transaction.category).first()
    if budget:
        budget.spent += db_transaction.amount
    
    db.commit()
    db.refresh(db_transaction)
    if budget:
        db.refresh(budget)
    return db_transaction

# GET method at /transaction endpoint for user to be able to see all transactions made by them
@router.get("/", response_model=list[Transaction])
def get_transactions(db: Session = Depends(get_db), current_user: UserTable = Depends(get_current_user)):
    return db.query(TransactionTable).all()

# GET method at /transaction endpoint for user to be able to see specific transactions made by them
@router.get("/{transaction_id}", response_model=Transaction)
def get_transaction(transaction_id: int, db: Session = Depends(get_db), current_user: UserTable = Depends(get_current_user)):
    transaction = db.query(TransactionTable).filter(TransactionTable.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction

# PUT method at /transaction endpoint for user to be able to update transactions details
@router.put("/{transaction_id}", response_model=Transaction)
def update_transaction(transaction_id: int, updated_data: TransactionCreate, db: Session = Depends(get_db), current_user: UserTable = Depends(get_current_user)):
    transaction = db.query(TransactionTable).filter(TransactionTable.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    for key, value in updated_data.dict().items():
        setattr(transaction, key, value)

    db.commit()
    db.refresh(transaction)
    return transaction

# DELETE method at /transaction endpoint for user to be able to remove/delete specific transactions
@router.delete("/{transaction_id}")
def delete_transaction(transaction_id: int, db: Session = Depends(get_db), current_user: UserTable = Depends(get_current_user)):
    transaction = db.query(TransactionTable).filter(TransactionTable.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    budget = db.query(BudgetTable).filter(BudgetTable.user_id == current_user.id, BudgetTable.category == transaction.category).first()
    if budget:
        budget.spent -= transaction.amount
        if budget.spent < 0:
            budget.spent = 0

    db.delete(transaction)
    db.commit()
    return {"message": "Transaction deleted successfully"}
