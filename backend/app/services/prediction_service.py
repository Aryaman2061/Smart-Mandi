from pathlib import Path

import joblib
import pandas as pd

MODEL_PATH = (
    Path(__file__).resolve().parents[1]
    / "ml"
    / "artifacts"
    / "random_forest_pipeline.joblib"
)

def predict_market_price(input_data):

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            "Random Forest model not found. "
            "Please train the model first."
        )

    # Load trained Random Forest pipeline
    model = joblib.load(MODEL_PATH)

    # Convert input dictionary into DataFrame
    input_df = pd.DataFrame([input_data])

    # Predict modal price
    prediction = model.predict(input_df)

    return round(float(prediction[0]), 2)
