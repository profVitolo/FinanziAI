from fastapi import APIRouter, HTTPException, Depends

from services.portfolio_service import PortfolioService
from services.transaction_service import TransactionService

from api.schemas import (TransactionCreate, TransactionUpdate, TransactionsFilter)

router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"]
)



@router.get("/")
def get_transactions(filters: TransactionsFilter = Depends()):
    transaction_service = TransactionService()

    return transaction_service.get_transactions(
        asset_id=filters.asset_id,
        start_date=filters.start_date,
        end_date=filters.end_date
    )


@router.get("/{transaction_id}")
def get_transaction(transaction_id: int):
    transaction_service = TransactionService()
    
    transaction = transaction_service.get_transaction(transaction_id)

    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")

    return transaction


@router.post("/")
def create_transaction(payload: TransactionCreate):
    portfolio_service = PortfolioService()
    
    try:
        transaction_id = portfolio_service.register_transaction(
            asset_id=payload.asset_id,
            operation_type=payload.operation_type,
            quantity=payload.quantity,
            price=payload.price,
            fees=payload.fees,
            transaction_date=payload.transaction_date
        )

        return {"status": "success", "transaction_id": transaction_id}

    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.put("/{transaction_id}")
def update_transaction(transaction_id: int, payload: TransactionUpdate):
    portfolio_service = PortfolioService()
    
    try:
        portfolio_service.update_transaction(
            transaction_id=transaction_id,
            asset_id=payload.asset_id,
            transaction_date=payload.transaction_date,
            operation_type=payload.operation_type,
            quantity=payload.quantity,
            price=payload.price,
            fees=payload.fees
        )

        return {"status": "success", "transaction_id": transaction_id}

    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.delete("/{transaction_id}")
def delete_transaction(transaction_id: int):
    portfolio_service = PortfolioService()
    
    try:
        portfolio_service.delete_transaction(transaction_id)

        return {"status": "success", "transaction_id": transaction_id}

    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
        