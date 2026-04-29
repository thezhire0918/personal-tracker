# backend/app/routes/transactions.py

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import SessionLocal
from app.models import Transaction

router = APIRouter()


class TransactionCreate(BaseModel):
    type: str
    amount: float
    category: str | None = None
    description: str | None = None


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/transactions")
def create_transaction(
    transaction: TransactionCreate,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if transaction.type not in ["income", "expense"]:
        raise HTTPException(
            status_code=400,
            detail="Transaction type must be income or expense",
        )

    if transaction.amount <= 0:
        raise HTTPException(
            status_code=400,
            detail="Amount must be greater than 0",
        )

    new_transaction = Transaction(
        user_id=user_id,
        type=transaction.type,
        amount=transaction.amount,
        category=transaction.category,
        description=transaction.description,
    )

    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)

    return {
        "message": "Transaction added successfully",
        "transaction_id": new_transaction.id,
        "type": new_transaction.type,
        "amount": new_transaction.amount,
    }