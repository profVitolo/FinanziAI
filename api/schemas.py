from datetime import date
from pydantic import BaseModel, Field
from fastapi import Query
from advisor_engine.advisor_models import InvestorProfile


class TransactionCreate(BaseModel):
    asset_id: int
    operation_type: str = Field(pattern="^(?i)(buy|sell)$")
    quantity: float = Field(gt=0)
    price: float = Field(gt=0)
    fees: float = Field(default=0, ge=0)
    transaction_date: date | None = None
    
class TransactionUpdate(TransactionCreate):
    pass
    
class AssetUpdate(BaseModel):
    initial_days: int = 365

class AssetSync(BaseModel):
    start_date: date
    end_date: date | None = None

class TransactionsFilter(BaseModel):
    start_date: date | None = None
    end_date: date | None = None
    asset_id: int | None = None


class ExchangeRateSync(BaseModel):
    from_currency: str
    to_currency: str
    rate_date: str | None = None

class ExchangeRatesSync(BaseModel):
    from_currency: str
    to_currency: str
    start_date: str
    end_date: str | None = None
    
class ExchangeConvert(BaseModel):
    amount: float
    from_currency: str
    to_currency: str
    rate_date: str | None = None
    

class ExchangeRatesFilter:
    def __init__(
        self,
        from_currency: str | None = Query(None),
        to_currency: str | None = Query(None),
        start_date: str | None = Query(None),
        end_date: str | None = Query(None)
    ):
        self.from_currency = from_currency
        self.to_currency = to_currency
        self.start_date = start_date
        self.end_date = end_date

class MissingDatesFilter:
    def __init__(self, from_currency: str, to_currency: str, start_date: str, end_date: str | None = None):
        self.from_currency = from_currency
        self.to_currency = to_currency
        self.start_date = start_date
        self.end_date = end_date


class DatabaseRequest(BaseModel):
    db_name: str
   
class AdviseBody(BaseModel):
    prompt: str
    investor_profile: InvestorProfile = InvestorProfile.BALANCED
