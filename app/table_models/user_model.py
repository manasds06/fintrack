from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..core.database import Base

# UserTable class that tells sqlalchemy what type of table to create
class UserTable(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    transactions = relationship("TransactionTable", back_populates="users")
    
    budgets = relationship("BudgetTable", back_populates="users")
