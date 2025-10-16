from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from ..core.database import Base

# TransactionTable class that tells sqlalchemy what type of table to create
class TransactionTable(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    amount = Column(Float)
    category = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

    budget_id = Column(Integer, ForeignKey("budgets.id"), nullable=True)
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    budgets = relationship("BudgetTable", back_populates="transactions")

    users = relationship("UserTable", back_populates="transactions")