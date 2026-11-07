from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Commodity
from app.schemas import CommodityResponse


router = APIRouter(
    prefix="/commodities",
    tags=["Commodities"]
)


@router.get("/", response_model=list[CommodityResponse])
def get_commodities(db: Session = Depends(get_db)):

    commodities = db.query(Commodity).order_by(
        Commodity.name
    ).all()

    return commodities