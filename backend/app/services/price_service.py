
from datetime import date

from sqlalchemy.orm import Session

from app.models import MarketPrice, Commodity, Market


def get_price_history(
    db: Session,
    commodity: str,
    market_id: int,
    start_date: date | None = None,
    end_date: date | None = None,
    variety: str | None = None,
    grade: str | None = None
):

    query = (
        db.query(MarketPrice)
        .join(Commodity)
        .filter(Commodity.name.ilike(commodity))
        .filter(MarketPrice.market_id == market_id)
    )

    if start_date:
        query = query.filter(
            MarketPrice.date >= start_date
        )

    if end_date:
        query = query.filter(
            MarketPrice.date <= end_date
        )

    if variety:
        query = query.filter(
            MarketPrice.variety.ilike(variety)
        )

    if grade:
        query = query.filter(
            MarketPrice.grade.ilike(grade)
        )

    return query.order_by(
        MarketPrice.date.asc()
    ).all()


def get_latest_prices(
    db: Session,
    commodity: str | None = None,
    state: str | None = None,
    district: str | None = None,
    variety: str | None = None,
    grade: str | None = None
):

    query = (
        db.query(MarketPrice)
        .join(Commodity)
        .join(Market)
    )

    if commodity:
        query = query.filter(
            Commodity.name.ilike(commodity)
        )

    if state:
        query = query.filter(
            Market.state.ilike(state)
        )

    if district:
        query = query.filter(
            Market.district.ilike(district)
        )

    if variety:
        query = query.filter(
            MarketPrice.variety.ilike(variety)
        )

    if grade:
        query = query.filter(
            MarketPrice.grade.ilike(grade)
        )

    return query.order_by(
        MarketPrice.date.desc()
    ).limit(100).all()
