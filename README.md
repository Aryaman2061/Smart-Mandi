# 🌾 Smart-Mandi
### AI-Powered Mandi Price Prediction & Market Intelligence Platform

Smart-Mandi is an AgriTech platform designed to help farmers make informed selling decisions through data-driven mandi price insights.

The platform uses historical agricultural market data to predict commodity prices, compare prices across markets, and help farmers identify potentially better selling opportunities.

Instead of relying only on current market prices, Smart-Mandi aims to provide insights into price trends and market behaviour using Machine Learning.

---

## 🚀 Key Features

- **Mandi Price Prediction:** Predicts commodity modal prices using a Random Forest regression model.
- **Market Comparison:** Helps compare commodity prices across different mandis.
- **Historical Price Data:** Stores historical market price records in PostgreSQL.
- **Data Ingestion Pipeline:** Imports, cleans, validates, and stores mandi data from CSV files.
- **Duplicate Detection:** Prevents previously ingested market price records from being inserted again.
- **Machine Learning Pipeline:** Includes categorical preprocessing, One-Hot Encoding, and Random Forest regression.
- **Model Persistence:** Saves the trained ML pipeline using Joblib for reuse during predictions.

---

## 🛠️ Technology Stack

| Category | Technologies |
|---|---|
| Backend | Python, FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Data Processing | Pandas, NumPy |
| Machine Learning | Scikit-learn |
| ML Model | Random Forest Regressor |
| Preprocessing | OneHotEncoder, SimpleImputer |
| Model Persistence | Joblib |
| API Testing | Postman |
| Database Management | pgAdmin |

---

## 🧠 Machine Learning Workflow

Smart-Mandi uses a supervised machine learning approach to predict mandi modal prices.

### Features Used

The current Random Forest model uses the following input features:

- State
- District
- Market
- Commodity
- Grade

### Prediction Target

- `modal_price`

### Model Pipeline

1. Fetch historical market price records from PostgreSQL.
2. Clean and prepare the dataset.
3. Separate input features and target variable.
4. Split data into training and testing sets.
5. Handle missing categorical values using SimpleImputer.
6. Convert categorical features into numerical representations using OneHotEncoder.
7. Train a Random Forest Regressor.
8. Evaluate model performance using MAE, RMSE, and R².
9. Save the complete preprocessing and model pipeline using Joblib.

### Evaluation Metrics

- **MAE:** Mean Absolute Error
- **RMSE:** Root Mean Squared Error
- **R² Score:** Coefficient of Determination

---

## 📊 Data Pipeline

Smart-Mandi uses a CSV-based ingestion pipeline to populate its PostgreSQL database.

### Data Flow

```text
Government Mandi Dataset (CSV)
             |
             v
      CSV Ingestion
             |
             v
       Data Cleaning
             |
             v
    Duplicate Detection
             |
             v
       PostgreSQL
             |
             v
     Training Dataset
             |
             v
      Random Forest
             |
             v
     Model Evaluation
             |
             v
      Saved Pipeline
             |
             v
      Price Prediction
```

### Incremental Data Ingestion

New datasets can be added without deleting existing database records.

The ingestion pipeline:

- Reads new CSV files.
- Cleans and normalizes the data.
- Creates new commodity and market entries when required.
- Checks for existing market price records.
- Skips matching records.
- Inserts new market price records into PostgreSQL.

This allows historical market data to accumulate over time.

---

## 📁 Project Structure

```text
Smart-Mandi/
│
├── backend/
│   │
│   ├── app/
│   │   ├── routers/
│   │   │   ├── markets.py
│   │   │   ├── commodities.py
│   │   │   └── prices.py
│   │   │
│   │   ├── services/
│   │   │   └── price_service.py
│   │   │
│   │   ├── data_pipeline/
│   │   │   ├── ingest_csv.py
│   │   │   └── cleaning.py
│   │   │
│   │   ├── artifacts/
│   │   │   └── random_forest_pipeline.joblib
│   │   │
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   └── main.py
│   │
│   ├── data/
│   │   ├── raw/
│   │   └── processed/
│   │
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│
└── README.md
```

*The structure above represents the main project components; individual files may vary as development progresses.*

---

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/Smart-Mandi.git

cd Smart-Mandi
```

### 2. Navigate to the backend

```bash
cd backend
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

**macOS / Linux**

```bash
source .venv/bin/activate
```

**Windows**

```bash
.venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure PostgreSQL

Create a PostgreSQL database:

```sql
CREATE DATABASE smart_mandi;
```

Configure your `.env` file using `.env.example`.

Example:

```env
DATABASE_URL=postgresql+psycopg://username:password@localhost:5432/smart_mandi
```

Replace the credentials with your local PostgreSQL credentials.

### 6. Run the backend

```bash
uvicorn app.main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

FastAPI interactive documentation:

```text
http://127.0.0.1:8000/docs
```

---

## 📥 Importing Mandi Data

Place your CSV dataset inside the appropriate data directory.

Example:

```text
backend/
└── data/
    └── raw/
        └── mandi.csv
```

Run the ingestion script from the backend directory:

```bash
python -m app.data_pipeline.ingest_csv --file data/raw/mandi.csv
```

The script cleans the dataset and inserts new records into PostgreSQL.

---

## 🌲 Training the Machine Learning Model

After ingesting sufficient market price data, run the model training script.

```bash
python -m app.ml.train
```

The training pipeline:

- Fetches records from PostgreSQL.
- Preprocesses categorical features.
- Trains the Random Forest model.
- Evaluates predictions.
- Saves the trained pipeline as a `.joblib` artifact.

The saved pipeline can then be loaded by the prediction service without retraining every time a prediction is requested.

---

## 📈 Future Improvements

- Automated mandi data fetching from government APIs.
- Time-series forecasting for future price trends.
- Market arrival and demand prediction.
- Price anomaly detection.
- Best mandi recommendation based on price and transportation considerations.
- Automated model retraining when sufficient new data becomes available.
- Model performance monitoring.
- Improved farmer-friendly interface.

---

## 🎯 Project Objective

The primary objective of Smart-Mandi is to bridge the information gap between farmers and agricultural markets.

By combining historical mandi data, Machine Learning, and market intelligence, the platform aims to help farmers make more informed decisions about **where and when to sell their agricultural produce**.

---

## 👨‍💻 Author

Developed as an AgriTech and Machine Learning project.

**Smart-Mandi — Turning Agricultural Market Data into Smarter Selling Decisions.**
