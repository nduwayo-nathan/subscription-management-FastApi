from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.plan import Plan, PlanCreate, PlanUpdate  # Define Pydantic schemas
from typing import List
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base, Session

# Database setup for PostgreSQL
DATABASE_URL = "postgresql://postgres:ABC123%%%@localhost/fastApi_subscription"  # Adjust to your PostgreSQL credentials

# Create SQLAlchemy engine and sessionmaker
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Define the Plan model for the database
class PlanDB(Base):
    __tablename__ = "plans"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    price = Column(Integer)  # Price in cents (e.g., 1999 for $19.99)
    description = Column(String, nullable=True)

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

# Endpoint to create a plan
@router.post("/plans/", response_model=Plan)
def create_plan(plan: PlanCreate, db: Session = Depends(get_db)):
    # Create a new plan instance
    db_plan = PlanDB(name=plan.name, price=plan.price, description=plan.description)
    
    # Add the plan to the database
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)
    
    return db_plan

# Endpoint to get a single plan by ID
@router.get("/plans/{plan_id}", response_model=Plan)
def get_plan(plan_id: int, db: Session = Depends(get_db)):
    db_plan = db.query(PlanDB).filter(PlanDB.id == plan_id).first()
    if db_plan is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plan not found")
    return db_plan

# Endpoint to update a plan by ID
@router.put("/plans/{plan_id}", response_model=Plan)
def update_plan(plan_id: int, plan: PlanUpdate, db: Session = Depends(get_db)):
    db_plan = db.query(PlanDB).filter(PlanDB.id == plan_id).first()
    if db_plan is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plan not found")
    
    if plan.name is not None:
        db_plan.name = plan.name
    if plan.price is not None:
        db_plan.price = plan.price
    if plan.description is not None:
        db_plan.description = plan.description
    
    db.commit()
    db.refresh(db_plan)
    
    return db_plan

# Endpoint to get all plans from the database
@router.get("/plans/", response_model=List[Plan])
def get_all_plans(db: Session = Depends(get_db)):
    plans = db.query(PlanDB).all()
    return plans

# Endpoint to delete a plan by ID
@router.delete("/plans/{plan_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_plan(plan_id: int, db: Session = Depends(get_db)):
    db_plan = db.query(PlanDB).filter(PlanDB.id == plan_id).first()
    if db_plan is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plan not found")
    
    db.delete(db_plan)
    db.commit()
    return {"message": f"Plan with ID {plan_id} deleted successfully"}
