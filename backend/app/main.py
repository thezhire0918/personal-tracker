# backend/app/main.py

from fastapi import FastAPI, Depends
from app.database import Base, engine
from app.routes import users, transactions
from app.auth import get_current_user

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(transactions.router)


@app.get("/")
def read_root():
    return {"message": "Personal Tracker API is running"}


@app.get("/protected")
def protected_route(user_id: int = Depends(get_current_user)):
    return {
        "message": "You are authenticated",
        "user_id": user_id
    }