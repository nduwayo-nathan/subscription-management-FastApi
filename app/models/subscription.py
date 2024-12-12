from sqlalchemy import Column, Integer, ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship

class SubscriptionModel(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    plan_id = Column(Integer, ForeignKey('plans.id'))
    user_id = Column(Integer, ForeignKey('users.id'))

    plan = relationship("Plan", back_populates="subscriptions")
    user = relationship("User", back_populates="subscriptions")

    # Add the payments relationship
    payments = relationship("PaymentModel", back_populates="subscription", cascade="all, delete-orphan")
