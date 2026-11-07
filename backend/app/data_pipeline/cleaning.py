
import re
import pandas as pd


def normalize_column_name(column):

    column = str(column).strip().lower()

    # Handle encoded spaces
    column = column.replace("_x0020_", "_")

    # Remove text inside parentheses
    column = re.sub(r"\([^)]*\)", "", column)

    # Replace special characters
    column = re.sub(r"[^a-z0-9]+", "_", column)

    return column.strip("_")


def clean_market_data(df: pd.DataFrame):

    df = df.copy()

    # 1. Normalize column names
    df.columns = [
        normalize_column_name(col)
        for col in df.columns
    ]

    print("Normalized columns:", df.columns.tolist())

    # 2. Rename columns
    df = df.rename(columns={
        "arrival_date": "date",
        "min_price": "min_price",
        "max_price": "max_price",
        "modal_price": "modal_price"
    })

    # 3. Check required columns
    required_columns = [
        "state",
        "district",
        "market",
        "commodity",
        "date",
        "modal_price"
    ]

    missing = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Missing required columns: {missing}"
        )

    # 4. Add optional columns
    optional_columns = [
        "variety",
        "grade",
        "min_price",
        "max_price",
        "arrivals"
    ]

    for col in optional_columns:
        if col not in df.columns:
            df[col] = pd.NA

    # 5. Clean text columns
    text_columns = [
        "state",
        "district",
        "market",
        "commodity",
        "variety",
        "grade"
    ]

    for col in text_columns:
        df[col] = (
            df[col]
            .astype("string")
            .str.strip()
        )

        df[col] = df[col].replace("", pd.NA)

    # Preserve missing variety/grade explicitly
    df["variety"] = df["variety"].fillna("Unknown")
    df["grade"] = df["grade"].fillna("Unknown")

    # 6. Convert dates
    df["date"] = pd.to_datetime(
        df["date"],
        dayfirst=True,
        errors="coerce"
    ).dt.date

    # 7. Convert numerical columns
    numerical_columns = [
        "min_price",
        "max_price",
        "modal_price",
        "arrivals"
    ]

    for col in numerical_columns:
        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )

    # 8. Remove rows missing essential data
    df = df.dropna(
        subset=[
            "state",
            "district",
            "market",
            "commodity",
            "date",
            "modal_price"
        ]
    )

    # 9. Remove invalid prices
    df = df[df["modal_price"] > 0]

    valid_range = (
        df["min_price"].isna()
        | df["max_price"].isna()
        | (df["min_price"] <= df["max_price"])
    )

    df = df[valid_range]

    # 10. Remove duplicates
    df = df.drop_duplicates(
        subset=[
            "state",
            "district",
            "market",
            "commodity",
            "variety",
            "grade",
            "date"
        ]
    )

    # 11. Select columns
    final_columns = [
        "state",
        "district",
        "market",
        "commodity",
        "variety",
        "grade",
        "date",
        "min_price",
        "max_price",
        "modal_price",
        "arrivals"
    ]

    df = df[final_columns].reset_index(drop=True)

    print(f"Cleaned dataset: {len(df)} rows")

    return df
