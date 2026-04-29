# backend/app/main.py

from fastapi import FastAPI

from app.database import Base, engine
from app.routes import users

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)


@app.get("/")
def read_root():
    return {"message": "Personal Tracker API is running"}