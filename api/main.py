from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pickle
import pandas as pd
import os

app = FastAPI(title="Weather ML Prediction API")

# Load the trained models at startup
try:
    with open(os.path.join("models", "temperature_model.pkl"), 'rb') as f:
        temp_model = pickle.load(f)
    with open(os.path.join("models", "rain_model.pkl"), 'rb') as f:
        rain_model = pickle.load(f)
except FileNotFoundError:
    print("Warning: Model files not found in models/ directory.")

# Include ALL features needed by both models
class WeatherInput(BaseModel):
    hour: int
    month: int
    temperature_2m: float
    relative_humidity_2m: float
    precipitation: float
    wind_speed_10m: float
    surface_pressure: float
    cloud_cover: float
    temp_lag_1: float
    temp_lag_3: float      
    temp_lag_24: float     
    humidity_lag_1: float  
    rain_lag_1: float      
    temp_rolling_6: float
    temp_rolling_24: float

@app.get("/")
def health_check():
    return {"status": "online", "message": "Weather API is running."}

@app.post("/predict")
def predict_weather(data: WeatherInput):
    try:
        # Convert JSON to a dictionary (handles Pydantic v1 and v2)
        input_dict = data.model_dump() if hasattr(data, 'model_dump') else data.dict()
        input_df = pd.DataFrame([input_dict])
        
        # Define the exact columns each model expects
        temp_features = ['hour', 'month', 'temperature_2m', 'relative_humidity_2m', 
                         'precipitation', 'wind_speed_10m', 'surface_pressure', 'cloud_cover',
                         'temp_lag_1', 'temp_lag_3', 'temp_lag_24', 'temp_rolling_6', 'temp_rolling_24']
                         
        rain_features = ['hour', 'month', 'temperature_2m', 'relative_humidity_2m', 
                         'precipitation', 'wind_speed_10m', 'surface_pressure', 'cloud_cover',
                         'temp_lag_1', 'humidity_lag_1', 'rain_lag_1', 'temp_rolling_6', 'temp_rolling_24']
        
        # Make predictions using only the required columns
        future_temp = temp_model.predict(input_df[temp_features])[0]
        will_rain = rain_model.predict(input_df[rain_features])[0]
        rain_prob = rain_model.predict_proba(input_df[rain_features])[0][1] 
        
        return {
            "predicted_temperature_3h": round(float(future_temp), 2),
            "rain_expected_3h": bool(will_rain),
            "rain_probability_percent": round(float(rain_prob) * 100, 1)
        }
    except Exception as e:
        print(f"Server Error: {e}") # This will print the exact error in your VS Code terminal
        raise HTTPException(status_code=500, detail=str(e))