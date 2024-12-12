# app/routers/subscriptions.py
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from app.models.subscription import SubscriptionModel as SubscriptionModel
from app.schemas.subscription import SubscriptionCreate, SubscriptionUpdate, Subscription
from app.database import get_db  # Function to provide DB session

router = APIRouter()

# Endpoint to get all subscriptions
@router.get("/subscriptions/", response_model=List[Subscription])
def get_subscriptions(db: Session = Depends(get_db)):
    subscriptions = db.query(SubscriptionModel).all()  # Get all subscriptions from the database
    return subscriptions

# Endpoint to create a new subscription
@router.post("/subscriptions/", response_model=Subscription)
def create_subscription(subscription: SubscriptionCreate, db: Session = Depends(get_db)):
    db_subscription = SubscriptionModel(
        plan_id=subscription.plan_id, 
        user_id=subscription.user_id, 
        start_date=subscription.start_date, 
        end_date=subscription.end_date
    )
    db.add(db_subscription)
    db.commit()  # Save the subscription to the database
    db.refresh(db_subscription)  # Get the newly created subscription with generated ID
    return db_subscription

# Endpoint to get a specific subscription by ID
@router.get("/subscriptions/{subscription_id}", response_model=Subscription)
def get_subscription(subscription_id: int, db: Session = Depends(get_db)):
    subscription = db.query(SubscriptionModel).filter(SubscriptionModel.id == subscription_id).first()  # Find the subscription by ID
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return subscription

# Endpoint to update a specific subscription by ID
@router.put("/subscriptions/{subscription_id}", response_model=Subscription)
def update_subscription(subscription_id: int, subscription: SubscriptionUpdate, db: Session = Depends(get_db)):
    db_subscription = db.query(SubscriptionModel).filter(SubscriptionModel.id == subscription_id).first()
    if not db_subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    
    # Update subscription attributes
    db_subscription.plan_id = subscription.plan_id
    db_subscription.user_id = subscription.user_id
    db_subscription.start_date = subscription.start_date
    db_subscription.end_date = subscription.end_date
    db.commit()  # Save the changes to the database
    db.refresh(db_subscription)  # Refresh the object with updated data
    return db_subscription

# Endpoint to delete a specific subscription by ID
@router.delete("/subscriptions/{subscription_id}")
def delete_subscription(subscription_id: int, db: Session = Depends(get_db)):
    db_subscription = db.query(SubscriptionModel).filter(SubscriptionModel.id == subscription_id).first()
    if not db_subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    
    db.delete(db_subscription)  # Delete the subscription from the database
    db.commit()  # Commit the transaction to make changes permanent
    return {"message": "Subscription deleted"}
