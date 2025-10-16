from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from ..core.database import Base

# BudgetTable class that tells sqlalchemy what type of table to create
class BudgetTable(Base):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String)
    limit = Column(Float, nullable=False)
    spent = Column(Float, default=0.0)

    transactions = relationship("TransactionTable", back_populates="budgets")

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    users = relationship("UserTable", back_populates="budgets")