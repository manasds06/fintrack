from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Creating a database url in project folder
DATABASE_URL = "sqlite:///./fintrack.db"

# Connecting python to database
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}
)

# SessionLocal class to handle database sessions
SessionLocal = sessionmaker(bind=engine)

# Table models will inherit from this class
Base = declarative_base()