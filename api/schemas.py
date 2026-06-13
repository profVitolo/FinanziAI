from datetime import date
from pydantic import BaseModel, Field

class TransactionCreate(BaseModel):
    asset_id: int
    operation_type: str = Field(pattern="^(?i)(buy|sell)$")
    quantity: float = Field(gt=0)
    price: float = Field(gt=0)
    fees: float = Field(default=0, ge=0)
    transaction_date: date | None = None

class AssetSync(BaseModel):
    start_date: date 
    end_date: date | None = None

class TransactionsFilter(BaseModel):
    start_date: date | None = None
    end_date: date | None = None