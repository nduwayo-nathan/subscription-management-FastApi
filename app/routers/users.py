from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas import User, UserCreate, UserUpdate
from typing import List
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base, Session
import bcrypt

# Database setup for PostgreSQL
DATABASE_URL = "postgresql://postgres:ABC123%%%@localhost/fastApi_subscription"  # Adjust to your PostgreSQL credentials

# Create SQLAlchemy engine and sessionmaker
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Define the User model for the database
class UserDB(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)  # Store hashed password here

    def set_password(self, password: str):
        """Hash the password before saving."""
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password: str) -> bool:
        """Check if the provided password matches the hashed password."""
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

# Create the tables in the database (do this once)
Base.metadata.create_all(bind=engine)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter()

# Endpoint to create a user
@router.post("/users/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if the username or email already exists
    db_user = db.query(UserDB).filter(UserDB.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
    
    db_user = db.query(UserDB).filter(UserDB.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
    
    # Create a new user instance
    new_user = UserDB(username=user.username, email=user.email)
    
    # Set the hashed password
    new_user.set_password(user.password)
    
    # Add the user to the database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

# Endpoint to get a single user by ID
@router.get("/users/{user_id}", response_model=User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user

# Endpoint to update a user by ID
@router.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    # If the new username or email is provided, check for duplicates
    if user.username and user.username != db_user.username:
        existing_user = db.query(UserDB).filter(UserDB.username == user.username).first()
        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")

    if user.email and user.email != db_user.email:
        existing_user = db.query(UserDB).filter(UserDB.email == user.email).first()
        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
    
    # Update user fields
    db_user.username = user.username if user.username else db_user.username
    db_user.email = user.email if user.email else db_user.email
    
    # If password is provided, hash it and update it
    if user.password:
        db_user.set_password(user.password)
    
    db.commit()
    db.refresh(db_user)
    
    return db_user

# Endpoint to get all users from the database
@router.get("/users/", response_model=List[User])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(UserDB).all()
    return users

# Endpoint to delete a user by ID
@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    db.delete(db_user)
    db.commit()
    return {"message": f"User with ID {user_id} deleted successfully"}
