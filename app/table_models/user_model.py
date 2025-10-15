from sqlalchemy import Column, Integer, String
from ..core.database import Base

# UserTable class that tells sqlalchemy what type of table to create
class UserTable(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)