from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from ..core.database import Base

# TransactionTable class that tells sqlalchemy what type of table to create
class TransactionTable(Base):
    __tablename__ = "Transactions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    amount = Column(Float)
    category = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
