from sqlalchemy import Column, Integer, ForeignKey, DateTime
from app.database import Base
from datetime import datetime
from sqlalchemy.orm import relationship

class PaymentModel(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    subscription_id = Column(Integer, ForeignKey('subscriptions.id'))
    amount = Column(Integer)  # Amount paid in cents
    paid_at = Column(DateTime, default=datetime.utcnow)

    # Relationship back to Subscription
    subscription = relationship("SubscriptionModel", back_populates="payments")
