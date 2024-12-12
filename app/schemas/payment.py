from pydantic import BaseModel
from typing import Optional

# Base schema
class PaymentBase(BaseModel):
    amount: float
    subscription_id: int

# Schema for creating a payment
class PaymentCreate(PaymentBase):
    pass

# Schema for reading payment details (including the associated subscription)
class PaymentSchema(PaymentBase):
    id: int
    subscription: Optional[str]  # Optional field for subscription detail

    class Config:
        orm_mode = True
