from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.config import settings

from app.routers import (
    commodities,
    markets,
    prices
)


@asynccontextmanager
async def lifespan(app: FastAPI):

    # Create database tables during development
    Base.metadata.create_all(bind=engine)

    yield


app = FastAPI(
    title="Smart Mandi API",
    description="Agricultural Market Intelligence Platform",
    version="1.0.0",
    lifespan=lifespan
)


origins = [
    origin.strip()
    for origin in settings.CORS_ORIGINS.split(",")
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


app.include_router(
    commodities.router,
    prefix="/api/v1"
)

app.include_router(
    markets.router,
    prefix="/api/v1"
)

app.include_router(
    prices.router,
    prefix="/api/v1"
)


@app.get("/")
def root():

    return {
        "message": "Welcome to Smart Mandi API",
        "status": "running"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }