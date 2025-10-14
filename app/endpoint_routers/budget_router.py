from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..table_models.budget_model import BudgetTable
from ..validation_schemas.budgets import Budget, BudgetCreate

# Creates a mini API
router = APIRouter(
    prefix="/budget",
    tags=["Budgets"]
)

# POST method at /budget endpoint for user to create and add new budgets
@router.post("/", response_model=Budget)
def create_budget(budget: BudgetCreate, db: Session = Depends(get_db)):
    db_budget = BudgetTable(**budget.dict())
    db.add(db_budget)
    db.commit()
    db.refresh(db_budget)
    return db_budget

# GET method at /transaction endpoint for user to be able to see all transactions made by them
@router.get("/", response_model=list[Budget])
def get_budgets(db: Session = Depends(get_db)):
    return db.query(BudgetTable).all()

# GET method at /transaction endpoint for user to be able to see specific transactions made by them
@router.get("/{budget_id}", response_model=Budget)
def get_budget(budget_id: int, db: Session = Depends(get_db)):
    budget = db.query(BudgetTable).filter(BudgetTable.id == budget_id).first()
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    return budget

# PUT method at /transaction endpoint for user to be able to update transactions details
@router.put("/{budget_id}", response_model=Budget)
def update_transaction(budget_id: int, updated_data: BudgetCreate, db: Session = Depends(get_db)):
    budget = db.query(BudgetTable).filter(BudgetTable.id == budget_id).first()
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")

    for key, value in updated_data.dict().items():
        setattr(budget, key, value)

    db.commit()
    db.refresh(budget)
    return budget

# DELETE method at /transaction endpoint for user to be able to remove/delete specific transactions
@router.delete("/{budget_id}")
def delete_budget(budget_id: int, db: Session = Depends(get_db)):
    budget = db.query(BudgetTable).filter(BudgetTable.id == budget_id).first()
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")

    db.delete(budget)
    db.commit()
    return {"message": "Budget deleted successfully"}
