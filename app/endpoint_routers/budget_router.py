from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..core.security import get_current_user
from ..table_models.budget_model import BudgetTable
from ..table_models.user_model import UserTable
from ..validation_schemas.budgets import Budget, BudgetCreate

# Creates a mini API
router = APIRouter(
    prefix="/budget",
    tags=["Budgets"]
)

# POST method at /budget endpoint for user to create and add new budgets
@router.post("/", response_model=Budget)
def create_budget(budget: BudgetCreate, db: Session = Depends(get_db), current_user: UserTable = Depends(get_current_user)):
    # Check if the user already has a budget for that category
    existing = db.query(BudgetTable).filter(
        BudgetTable.user_id == current_user.id,
        BudgetTable.category == budget.category
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Budget for this category already exists.")

    db_budget = BudgetTable(**budget.dict(), user_id=current_user.id)
    db.add(db_budget)
    db.commit()
    db.refresh(db_budget)
    return db_budget

# GET method at /transaction endpoint for user to be able to see all transactions made by them
def get_budgets(db: Session = Depends(get_db), current_user: UserTable = Depends(get_current_user)):
    return db.query(BudgetTable).filter(BudgetTable.user_id == current_user.id).all()


# GET method at /transaction endpoint for user to be able to see specific transactions made by them
@router.get("/{budget_id}", response_model=Budget)
def get_budget(budget_id: int, db: Session = Depends(get_db), current_user: UserTable = Depends(get_current_user)):
    budget = db.query(BudgetTable).filter(
        BudgetTable.id == budget_id,
        BudgetTable.user_id == current_user.id
    ).first()
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    return budget

# PUT method at /transaction endpoint for user to be able to update transactions details
def update_budget(budget_id: int, updated_budget: BudgetCreate, db: Session = Depends(get_db), current_user: UserTable = Depends(get_current_user)):
    budget = db.query(BudgetTable).filter(
        BudgetTable.id == budget_id,
        BudgetTable.user_id == current_user.id
    ).first()

    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")

    for key, value in updated_budget.dict().items():
        setattr(budget, key, value)

    db.commit()
    db.refresh(budget)
    return budget


# DELETE method at /transaction endpoint for user to be able to remove/delete specific transactions
@router.delete("/{budget_id}")
def delete_budget(budget_id: int, db: Session = Depends(get_db), current_user: UserTable = Depends(get_current_user)):
    budget = db.query(BudgetTable).filter(
        BudgetTable.id == budget_id,
        BudgetTable.user_id == current_user.id
    ).first()

    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")

    db.delete(budget)
    db.commit()
    return {"message": "Budget deleted successfully"}