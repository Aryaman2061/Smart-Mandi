import argparse

import pandas as pd

from app.database import SessionLocal
from app.models import Commodity, Market, MarketPrice

from app.data_pipeline.cleaning import clean_market_data


def ingest_csv(file_path: str):

    print("Reading CSV...")

    df = pd.read_csv(file_path)

    print(f"Original rows: {len(df)}")

    df = clean_market_data(df)

    print(f"Cleaned rows: {len(df)}")

    db = SessionLocal()

    inserted = 0
    skipped = 0

    try:

        for _, row in df.iterrows():

            # 1. Get or create commodity

            commodity_name = row["commodity"]

            commodity = db.query(Commodity).filter(
                Commodity.name.ilike(commodity_name)
            ).first()

            if not commodity:

                commodity = Commodity(
                    name=commodity_name,
                    unit="quintal"
                )

                db.add(commodity)
                db.flush()

            # 2. Get or create market

            market = db.query(Market).filter(
                Market.name.ilike(row["market"]),
                Market.district.ilike(row["district"]),
                Market.state.ilike(row["state"])
            ).first()

            if not market:

                market = Market(
                    name=row["market"],
                    district=row["district"],
                    state=row["state"]
                )

                db.add(market)
                db.flush()

            # 3. Check for existing price record

            existing = db.query(MarketPrice).filter(
                MarketPrice.commodity_id == commodity.id,
                MarketPrice.market_id == market.id,
                MarketPrice.variety == row["variety"],
                MarketPrice.grade == row["grade"],
                MarketPrice.date == row["date"]
            ).first()

            if existing:

                skipped += 1
                continue

            # 4. Insert price record

            price = MarketPrice(
                commodity_id=commodity.id,
                market_id=market.id,
                variety=row["variety"],
                grade=row["grade"],
                date=row["date"],

                min_price=(
                    row["min_price"]
                    if "min_price" in row.index
                    else None
                ),

                max_price=(
                    row["max_price"]
                    if "max_price" in row.index
                    else None
                ),

                modal_price=row["modal_price"],

                arrivals=(
                    row["arrivals"]
                    if "arrivals" in row.index
                    else None
                ),

                source="data.gov.in"
            )

            db.add(price)

            inserted += 1

            # Commit in batches
            if inserted % 500 == 0:

                db.commit()

                print(f"Inserted {inserted} records...")

        db.commit()

        print("\nIngestion completed!")
        print(f"Inserted: {inserted}")
        print(f"Skipped: {skipped}")

    except Exception:

        db.rollback()
        raise

    finally:

        db.close()


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--file",
        required=True,
        help="Path to mandi CSV file"
    )

    args = parser.parse_args()

    ingest_csv(args.file)