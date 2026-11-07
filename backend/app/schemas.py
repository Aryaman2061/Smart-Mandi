from datetime import date

from pydantic import BaseModel, ConfigDict


class CommodityResponse(BaseModel):

    id: int
    name: str
    category: str | None = None
    unit: str

    model_config = ConfigDict(from_attributes=True)


class MarketResponse(BaseModel):

    id: int
    name: str
    state: str
    district: str

    latitude: float | None = None
    longitude: float | None = None

    model_config = ConfigDict(from_attributes=True)


class PriceResponse(BaseModel):

    id: int

    commodity_id: int
    market_id: int

    date: date

    min_price: float | None
    max_price: float | None
    modal_price: float

    arrivals: float | None
    arrivals_unit: str | None

    source: str | None

    model_config = ConfigDict(from_attributes=True)