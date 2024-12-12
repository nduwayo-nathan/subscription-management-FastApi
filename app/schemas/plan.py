# app/schemas/plan.py
from pydantic import BaseModel

class PlanBase(BaseModel):
    name: str
    price: int  # Price in cents
    description: str | None = None

class PlanCreate(PlanBase):
    pass

class PlanUpdate(PlanBase):
    name: str | None = None  # Optional in case you want to update a single field

class Plan(PlanBase):
    id: int

    class Config:
        orm_mode = True  # Tells Pydantic to treat the SQLAlchemy model as a dict
