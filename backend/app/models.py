from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Date,
    ForeignKey,
    UniqueConstraint
)

from sqlalchemy.orm import relationship

from app.database import Base


class Commodity(Base):

    __tablename__ = "commodities"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), unique=True, nullable=False)

    category = Column(String(100), nullable=True)

    unit = Column(String(30), default="quintal")

    prices = relationship(
        "MarketPrice",
        back_populates="commodity"
    )


class Market(Base):

    __tablename__ = "markets"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(150), nullable=False)

    state = Column(String(100), nullable=False)

    district = Column(String(100), nullable=False)

    latitude = Column(Float, nullable=True)

    longitude = Column(Float, nullable=True)

    prices = relationship(
        "MarketPrice",
        back_populates="market"
    )

    __table_args__ = (
        UniqueConstraint(
            "name",
            "district",
            "state",
            name="uq_market_location"
        ),
    )


class MarketPrice(Base):

    __tablename__ = "market_prices"

    id = Column(Integer, primary_key=True, index=True)

    commodity_id = Column(
        Integer,
        ForeignKey("commodities.id"),
        nullable=False
    )

    market_id = Column(
        Integer,
        ForeignKey("markets.id"),
        nullable=False
    )

    variety = Column(
        String(150),
        nullable=False,
        default="Unknown"
    )

    grade = Column(
        String(100),
        nullable=False,
        default="Unknown"
    )

    date = Column(Date, nullable=False)

    min_price = Column(Float, nullable=True)

    max_price = Column(Float, nullable=True)

    modal_price = Column(Float, nullable=False)

    arrivals = Column(Float, nullable=True)

    arrivals_unit = Column(String(30), nullable=True)

    source = Column(String(100), nullable=True)

    commodity = relationship(
        "Commodity",
        back_populates="prices"
    )

    market = relationship(
        "Market",
        back_populates="prices"
    )

    __table_args__ = (
        UniqueConstraint(
            "commodity_id",
            "market_id",
            "variety",
            "grade",
            "date",
            name="uq_market_price_record"
        ),
    )