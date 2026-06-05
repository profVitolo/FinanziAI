from datetime import date

from pydantic import BaseModel
from pydantic import Field


class TransactionCreate(BaseModel):
    asset_id: int

    transaction_type: str = Field(pattern="^(buy|sell)$")

    quantity: float = Field(gt=0)

    price: float = Field(gt=0)

    commission: float = Field(default=0, ge=0)

    transaction_date: date | None = None