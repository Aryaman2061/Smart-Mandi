from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestRegressor

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

from app.database import SessionLocal
from app.models import Commodity, Market, MarketPrice

FEATURES = [
    "state",
    "district",
    "market",
    "commodity",
    "grade"
]

TARGET = "modal_price"

ARTIFACT_PATH = (
    Path(__file__).resolve().parent
    / "artifacts"
    / "random_forest_pipeline.joblib"
)


def fetch_training_data():

    db = SessionLocal()

    try:

        records = (
            db.query(
                Market.state.label("state"),
                Market.district.label("district"),
                Market.name.label("market"),
                Commodity.name.label("commodity"),
                MarketPrice.grade.label("grade"),
                MarketPrice.modal_price.label("modal_price")
            )
            .join(
                Market,
                MarketPrice.market_id == Market.id
            )
            .join(
                Commodity,
                MarketPrice.commodity_id == Commodity.id
            )
            .filter(
                MarketPrice.modal_price > 0
            )
            .all()
        )

        df = pd.DataFrame(
            records,
            columns=FEATURES + [TARGET]
        )

        return df

    finally:
        db.close()


def train_model():

    print("Fetching data from PostgreSQL...")

    df = fetch_training_data()

    print("Total records:", len(df))

    if len(df) < 10:
        raise ValueError(
            "Not enough records to train Random Forest. "
            "Ingest more market price data first."
        )

    # Convert target to numeric
    df[TARGET] = pd.to_numeric(
        df[TARGET],
        errors="coerce"
    )

    # Remove missing or invalid target values
    df = df.dropna(subset=[TARGET])
    df = df[df[TARGET] > 0]

    # Clean categorical features
    for column in FEATURES:

        df[column] = (
            df[column]
            .astype("string")
            .str.strip()
            .replace("", pd.NA)
        )

    print("Usable records:", len(df))

    if len(df) < 10:
        raise ValueError(
            "Not enough valid records after cleaning."
        )

    X = df[FEATURES]
    y = df[TARGET]

    categorical_transformer = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(
                    strategy="constant",
                    fill_value="Unknown"
                )
            ),
            (
                "onehot",
                OneHotEncoder(
                    handle_unknown="ignore"
                )
            )
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "categorical",
                categorical_transformer,
                FEATURES
            )
        ]
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    print("\nTraining records:", len(X_train))
    print("Testing records:", len(X_test))

    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),

            (
                "model",
                RandomForestRegressor(
                    n_estimators=200,
                    max_depth=None,
                    min_samples_split=2,
                    min_samples_leaf=1,
                    random_state=42,
                    n_jobs=-1
                )
            )
        ]
    )

    print("\nTraining Random Forest model...")

    pipeline.fit(X_train, y_train)

    print("Training completed!")

    predictions = pipeline.predict(X_test)

    mae = mean_absolute_error(
        y_test,
        predictions
    )

    rmse = np.sqrt(
        mean_squared_error(
            y_test,
            predictions
        )
    )

    r2 = r2_score(
        y_test,
        predictions
    )

    print("\nRandom Forest Model Results")
    print("---------------------------")

    print("MAE:", round(mae, 2))
    print("RMSE:", round(rmse, 2))
    print("R2:", round(r2, 4))

    ARTIFACT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    joblib.dump(
        pipeline,
        ARTIFACT_PATH
    )

    print("\nRandom Forest model saved successfully!")

    print("Location:", ARTIFACT_PATH)

if __name__ == "__main__":
    train_model()
