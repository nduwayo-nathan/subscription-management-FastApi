# app/schemas/subscription.py
from pydantic import BaseModel
from datetime import date

class SubscriptionBase(BaseModel):
    user_id: int
    plan_id: int
    start_date: date
    end_date: date

class SubscriptionCreate(SubscriptionBase):
    pass

class SubscriptionUpdate(BaseModel):
    start_date: date | None = None  # Optional for update
    end_date: date | None = None    # Optional for update

class Subscription(SubscriptionBase):
    id: int

    class Config:
        orm_mode = True  # Tells Pydantic to treat the SQLAlchemy model as a dict
