from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from app.models.payment import PaymentModel
from app.schemas.payment import PaymentSchema, PaymentCreate
from app.database import get_db

router = APIRouter()

# Endpoint to get all payments
@router.get("/payments/", response_model=List[PaymentSchema])
def get_payments(db: Session = Depends(get_db)):
    payments = db.query(PaymentModel).all()  # Query for all payments
    return payments

# Endpoint to create a new payment
@router.post("/payments/", response_model=PaymentSchema)
def create_payment(payment: PaymentCreate, db: Session = Depends(get_db)):
    db_payment = PaymentModel(
        amount=payment.amount,
        subscription_id=payment.subscription_id,
    )
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment

# Endpoint to get a specific payment by ID
@router.get("/payments/{payment_id}", response_model=PaymentSchema)
def get_payment(payment_id: int, db: Session = Depends(get_db)):
    payment = db.query(PaymentModel).filter(PaymentModel.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment

# Endpoint to delete a specific payment by ID
@router.delete("/payments/{payment_id}")
def delete_payment(payment_id: int, db: Session = Depends(get_db)):
    db_payment = db.query(PaymentModel).filter(PaymentModel.id == payment_id).first()
    if not db_payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    
    db.delete(db_payment)
    db.commit()
    return {"message": "Payment deleted"}
