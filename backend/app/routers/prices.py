from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import PriceResponse
from app.services.price_service import (
    get_price_history,
    get_latest_prices
)


router = APIRouter(
    prefix="/prices",
    tags=["Market Prices"]
)


@router.get("/latest", response_model=list[PriceResponse])
def latest_prices(
    commodity: str | None = None,
    state: str | None = None,
    district: str | None = None,
    db: Session = Depends(get_db)
):

    return get_latest_prices(
        db,
        commodity,
        state,
        district
    )


@router.get("/history", response_model=list[PriceResponse])
def price_history(
    commodity: str,
    market_id: int,
    start_date: date | None = None,
    end_date: date | None = None,
    variety: str | None = None,
    grade: str | None = None,
    db: Session = Depends(get_db)
):

    if start_date and end_date and start_date > end_date:
        raise HTTPException(
            status_code=400,
            detail="Start date cannot be after end date"
        )

    return get_price_history(
        db,
        commodity,
        market_id,
        start_date,
        end_date,
        variety,
        grade
    )