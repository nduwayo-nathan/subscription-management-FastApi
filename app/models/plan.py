from sqlalchemy import Column, Integer, String
from app.database import Base
from sqlalchemy.orm import relationship

class Plan(Base):
    __tablename__ = "plans"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    price = Column(Integer)  # Price in cents (e.g., 1999 for $19.99)
    description = Column(String, nullable=True)
    
    # A plan can have multiple subscriptions
    #subscriptions = relationship("SubscriptionModel", back_populates="plan")
