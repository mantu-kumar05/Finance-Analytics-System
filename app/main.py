from fastapi import FastAPI, Depends
from typing import List

from app.models import Transaction, TransactionCreate

from app.crud import (
    get_all_transactions,
    add_transaction,
    remove_transaction
)

from app.analytics_service import get_financial_report

from app.users import router as user_router

from app.dependencies import get_current_user

from app.init_db import init_db



app = FastAPI(
    title="Finance Analytics API",
    version="1.0"
)


# Create database tables if they do not exist
init_db()


# Authentication routes
app.include_router(user_router)



@app.get("/")
def home():

    return {
        "message": "Finance Analytics API Running"
    }



# GET transactions (Protected)
@app.get(
    "/transactions",
    response_model=List[Transaction]
)
def get_transactions(
    current_user = Depends(get_current_user)
):

    user_id = current_user["user_id"]

    return get_all_transactions(user_id)



# POST transaction (Protected)
@app.post("/transactions")
def create_transaction(
    transaction: TransactionCreate,
    current_user = Depends(get_current_user)
):

    user_id = current_user["user_id"]

    add_transaction(
        transaction,
        user_id
    )

    return {
        "message": "Transaction added successfully"
    }



# DELETE transaction (Protected)
@app.delete("/transactions/{transaction_id}")
def delete_transaction(
    transaction_id: int,
    current_user = Depends(get_current_user)
):

    user_id = current_user["user_id"]

    remove_transaction(
        transaction_id,
        user_id
    )

    return {
        "message": "Transaction deleted successfully"
    }



# Analytics (Protected)
@app.get("/analytics")
def get_analytics(
    current_user = Depends(get_current_user)
):

    user_id = current_user["user_id"]

    return get_financial_report(user_id)