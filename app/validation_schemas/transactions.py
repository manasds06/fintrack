from pydantic import BaseModel
from datetime import datetime

class TransactionBase(BaseModel):
    amount: float
    title: str
    category: str

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True
