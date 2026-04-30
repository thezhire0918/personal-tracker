# backend/app/main.py

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.auth import get_current_user
from app.database import Base, engine
from app.routes import transactions, users

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(transactions.router)


@app.get("/")
def read_root():
    return {"message": "Personal Tracker API is running"}


@app.get("/protected")
def protected_route(user_id: int = Depends(get_current_user)):
    return {
        "message": "You are authenticated",
        "user_id": user_id,
    }