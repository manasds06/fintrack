from pydantic import BaseModel

class BudgetBase(BaseModel):
    category: str
    limit: float
    spent: float = 0.0

class BudgetCreate(BudgetBase):
    pass

class Budget(BudgetBase):
    id: int

    class Config:
        orm_mode = True
