Markdown
# 🌤️ AI-Powered Weather Analytics & Automated Alert System

An end-to-end Machine Learning and Process Automation pipeline designed for real-time weather forecasting and alert dispatching in the Twin Cities (**Rawalpindi & Islamabad, Pakistan**). 

The system periodically ingests live meteorological data from Open-Meteo, calculates historical lag and rolling features, feeds them into trained **XGBoost** models hosted via **FastAPI**, and sends automated multi-channel email alerts through **n8n** and **Gmail OAuth 2.0**.

---

## 🏗️ System Architecture

```text
[ Schedule Trigger (Every Hour) ]
               │
               ▼
   [ Open-Meteo API Fetch ]  ──> Live Rawalpindi/Islamabad Data
               │
               ▼
   [ JS Feature Engineer ]   ──> Generates 1h/3h/24h Lags & Rolling Means
               │
               ▼
    [ FastAPI ML Engine ]    ──> Runs XGBoost Models (Temp & Rain Probability)
               │
               ▼
 [ Gmail OAuth Alert Node ]  ──> Automated Email Prediction Alert
🛠️ Tech Stack & Dependencies
Language: Python 3.11, JavaScript (Node.js)

ML Frameworks: XGBoost, Scikit-Learn, Pandas, NumPy

API Backend: FastAPI, Uvicorn, Pydantic

Workflow Automation: n8n (Self-hosted)

Database & Storage: SQLite3, Joblib (Model Persistence)

External Services: Open-Meteo Weather API, Google Cloud OAuth 2.0 (Gmail API)

📂 Project Structure
Plaintext
AI-Weather-System/
├── api/
│   └── main.py                   # FastAPI application & model inference endpoints
├── data/
│   └── weather.db                # SQLite database for historical weather storage
├── models/
│   ├── xgboost_temperature.joblib# Trained XGBoost model for temperature prediction
│   └── xgboost_rain.joblib       # Trained XGBoost model for precipitation forecasting
├── n8n/
│   └── n8n_workflow.json         # Exported n8n automation workflow pipeline
├── notebooks/
│   └── weather_analysis.ipynb    # Jupyter Notebook for EDA & model validation
├── src/
│   ├── data_collection.py        # Open-Meteo historical data fetching script
│   ├── feature_engineering.py    # Lag, rolling statistics, and temporal features
│   ├── train_temperature.py      # XGBoost temperature training script
│   └── train_rain.py             # XGBoost precipitation classifier script
├── .env.example                  # Environment variables template
├── .gitignore                    # Version control exclusion rules
├── requirements.txt              # Python package dependencies
└── README.md                     # Project documentation
🚀 Getting Started
1. Prerequisites
Ensure you have the following installed on your machine:

Python 3.11+

Node.js v18+ & n8n (npm install n8n -g)

2. Environment Setup
Clone the repository and set up a virtual environment:

PowerShell
# Clone repository
git clone [https://github.com/MuhammadWaleed20/AI-Weather-System.git](https://github.com/MuhammadWaleed20/AI-Weather-System.git)
cd AI-Weather-System

# Create & activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1   # On Windows
# source venv/bin/activate    # On Linux/macOS

# Install dependencies
pip install -r requirements.txt
Create your local environment configuration file:

PowerShell
cp .env.example .env
⚡ Running the System
To run the pipeline locally, execute both the inference engine and the automation manager:

Step 1: Launch FastAPI Server
In terminal tab 1:

PowerShell
uvicorn api.main:app --reload
The API engine will spin up at http://127.0.0.1:8000. You can inspect the Swagger documentation at http://127.0.0.1:8000/docs.

Step 2: Start n8n Workflow Manager
In terminal tab 2:

PowerShell
n8n
Access the n8n UI at http://localhost:5678.

Import n8n/n8n_workflow.json into your workspace.

Authenticate your Gmail OAuth2 credentials under the Send Email Alert node.

Activate the workflow toggle to execute hourly.

📊 API Reference
Predict Weather (POST /predict)
Payload Format:

JSON
{
  "hour": 15,
  "month": 10,
  "temperature_2m": 26.5,
  "relative_humidity_2m": 45.0,
  "precipitation": 0.0,
  "wind_speed_10m": 11.2,
  "surface_pressure": 1012.3,
  "cloud_cover": 15.0,
  "temp_lag_1": 26.0,
  "temp_lag_3": 25.2,
  "temp_lag_24": 27.0,
  "humidity_lag_1": 46.0,
  "rain_lag_1": 0.0,
  "temp_rolling_6": 25.8,
  "temp_rolling_24": 24.1
}
Response Format:

JSON
{
  "predicted_temperature_3h": 26.84,
  "rain_expected_3h": false,
  "rain_probability_percent": 2.0
}
✅ Completed Milestones
[x] Data Pipeline: Ingested multi-year historical weather data for Rawalpindi/Islamabad into SQLite.

[x] Feature Engineering: Implemented temporal lags (1h, 3h, 24h) and moving averages (6h, 24h).

[x] Model Training: Trained and tuned XGBoost models for temperature regression and rain probability classification.

[x] FastAPI Deployment: Built REST API endpoints for asynchronous model inferences.

[x] Automation & Integration: Built n8n pipeline for fetching live data, processing features, triggering API calls, and delivering Gmail OAuth alerts.