from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from ..core.database import Base

# TransactionTable class that tells sqlalchemy what type of table to create
class BudgetTable(Base):
    __tablename__ = "Budgets"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String)
    limit = Column(Float, nullable=False)
    spent = Column(Float, default=0.0)

    transactions = relationship("TransactionTable", back_populates="budget")