from fastapi import APIRouter, Depends, HTTPException

from api.schemas import (ExchangeRatesFilter, MissingDatesFilter, ExchangeRateSync, ExchangeRatesSync, ExchangeConvert)
from services.exchange_service import ExchangeService

router = APIRouter(prefix="/exchange", tags=["Exchange"])


@router.get("/rates")
def get_rates(filters: ExchangeRatesFilter = Depends()):
    exchange_service = ExchangeService()

    return exchange_service.get_rates(
        from_currency=filters.from_currency,
        to_currency=filters.to_currency,
        start_date=filters.start_date,
        end_date=filters.end_date
    )


@router.get("/latest")
def get_latest_rate(from_currency: str, to_currency: str):
    exchange_service = ExchangeService()

    rate = exchange_service.get_latest_rate(from_currency, to_currency)

    if rate is None:
        raise HTTPException(status_code=404, detail="Exchange rate not found")

    return rate


@router.get("/missing")
def get_missing_dates(filters: MissingDatesFilter = Depends()):
    exchange_service = ExchangeService()

    return {
        "from_currency": filters.from_currency,
        "to_currency": filters.to_currency,
        "missing_dates": exchange_service.get_missing_dates(
            filters.from_currency,
            filters.to_currency,
            filters.start_date,
            filters.end_date
        )
    }


@router.get("/convert")
def convert(params: ExchangeConvert = Depends()):
    exchange_service = ExchangeService()

    try:
        converted_amount = exchange_service.convert(
            amount=params.amount,
            from_currency=params.from_currency,
            to_currency=params.to_currency,
            rate_date=params.rate_date
        )

        return {
            "amount": params.amount,
            "from_currency": params.from_currency,
            "to_currency": params.to_currency,
            "converted_amount": converted_amount,
            "rate_date": params.rate_date
        }

    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.post("/sync")
def sync_rate(payload: ExchangeRateSync):
    exchange_service = ExchangeService()

    success = exchange_service.sync_rate(payload.from_currency, payload.to_currency, payload.rate_date)

    return {
        "success": success,
        "from_currency": payload.from_currency,
        "to_currency": payload.to_currency,
        "rate_date": payload.rate_date
    }


@router.post("/sync-range")
def sync_rates(payload: ExchangeRatesSync):
    exchange_service = ExchangeService()

    return exchange_service.sync_rates(
        payload.from_currency,
        payload.to_currency,
        payload.start_date,
        payload.end_date
    )
    
    