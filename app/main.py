# app/main.py
from fastapi import FastAPI
from app.routers import users,plans, subscriptions, payments
from app.models.user import User
from app.models.plan import Plan

app = FastAPI()
@app.get("/")
def read_root():
    return {"message": "Welcome to the FAST API Subscription System!"}


app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(plans.router, prefix="/plans", tags=["plans"])
app.include_router(subscriptions.router, prefix="/subscriptions", tags=["subscriptions"])
# app.include_router(payments.router, prefix="/payments", tags=["payments"])
