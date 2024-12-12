from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Replace with your actual PostgreSQL connection string
DATABASE_URL = "postgresql://postgres:ABC123%%%@localhost:5432/fastApi_subscription"

# SQLAlchemy database engine
engine = create_engine(DATABASE_URL)

# SessionLocal factory for database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for model definitions
Base = declarative_base()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
