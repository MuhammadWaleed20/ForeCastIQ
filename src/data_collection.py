import requests
import json

def fetch_current_weather(lat=33.5973, lon=73.0479):
    """
    Fetches today's hourly weather data for a given location (Rawalpindi by default).
    """
    url = "https://api.open-meteo.com/v1/forecast"
    
    # Define the parameters we need from the API
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": [
            "temperature_2m",
            "relative_humidity_2m",
            "precipitation",
            "wind_speed_10m",
            "surface_pressure",
            "cloud_cover"
        ],
        "timezone": "Asia/Karachi",
        "forecast_days": 1 
    }
    
    try:
        print("Fetching data from Open-Meteo API...")
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Extract and print a sample of the first 3 hours to verify it works
        sample_data = {
            "time": data["hourly"]["time"][:3],
            "temperature_2m_C": data["hourly"]["temperature_2m"][:3],
            "humidity_pct": data["hourly"]["relative_humidity_2m"][:3],
            "precipitation_mm": data["hourly"]["precipitation"][:3]
        }
        
        print("\n✅ API Connection Successful! Sample Hourly Data:")
        print(json.dumps(sample_data, indent=4))
        
        return data

    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to fetch data: {e}")
        return None

if __name__ == "__main__":
    fetch_current_weather()