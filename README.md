# AI Weather Prediction & Automation System 🌤️🤖

An end-to-end automated machine learning pipeline that fetches local weather data, engineers time-series features, predicts future temperature and rain probabilities using XGBoost, and serves the models via a FastAPI REST interface. 

## 🚀 Tech Stack
* **Language:** Python 3.11
* **Machine Learning:** XGBoost, Scikit-Learn, Pandas
* **API Engine:** FastAPI, Uvicorn, Pydantic
* **Database & Storage:** SQLite
* **Data Source:** Open-Meteo API
* **Automation (In Progress):** n8n

## 📂 Project Structure
```text
AI-Weather-System/
├── api/
│   └── main.py                 # FastAPI inference engine
├── data/
│   ├── processed/              # Engineered ML features
│   └── raw/                    # Raw SQLite database extraction
├── models/                     # Compiled XGBoost .pkl files (git-ignored)
├── notebooks/                  # EDA and Data Visualization
├── src/
│   ├── data_collection.py      # Open-Meteo API integration
│   ├── database.py             # SQLite schema & initialization
│   ├── feature_engineering.py  # Time-series lags & rolling windows
│   ├── train_rain.py           # XGBoost Classification model
│   └── train_temperature.py    # XGBoost Regression model
├── weather.db                  # Local SQLite database
└── requirements.txt            # Python dependencies