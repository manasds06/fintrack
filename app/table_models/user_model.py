from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..core.database import Base

# UserTable class that tells sqlalchemy what type of table to create
class UserTable(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    transactions = relationship("TransactionTable", back_populates="user", cascade="all, delete-orphan")
    
    budgets = relationship("BudgetTable", back_populates="user", cascade="all, delete-orphan")
