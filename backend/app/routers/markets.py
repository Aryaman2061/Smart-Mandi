from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Market
from app.schemas import MarketResponse


router = APIRouter(
    prefix="/markets",
    tags=["Markets"]
)


@router.get("/", response_model=list[MarketResponse])
def get_markets(
    state: str | None = None,
    district: str | None = None,
    db: Session = Depends(get_db)
):

    query = db.query(Market)

    if state:
        query = query.filter(Market.state.ilike(state))

    if district:
        query = query.filter(Market.district.ilike(district))

    return query.order_by(Market.name).all()