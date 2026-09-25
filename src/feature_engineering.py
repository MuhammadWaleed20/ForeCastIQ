import pandas as pd
import sqlite3
import os

def generate_features():
    print("Loading raw data from database...")
    # Connect to database and load data sorted by time
    conn = sqlite3.connect(os.path.join("data", "weather.db"))
    df = pd.read_sql_query("SELECT * FROM weather_data ORDER BY time ASC", conn)
    conn.close()

    # Convert time to datetime and set as index
    df['time'] = pd.to_datetime(df['time'])
    df.set_index('time', inplace=True)

    print("Creating time-based features...")
    df['hour'] = df.index.hour
    df['month'] = df.index.month
    df['day_of_week'] = df.index.dayofweek

    print("Creating lag features (past weather)...")
    df['temp_lag_1'] = df['temperature_2m'].shift(1)
    df['temp_lag_3'] = df['temperature_2m'].shift(3)
    df['temp_lag_24'] = df['temperature_2m'].shift(24)
    
    df['humidity_lag_1'] = df['relative_humidity_2m'].shift(1)
    df['rain_lag_1'] = df['precipitation'].shift(1)

    print("Creating rolling averages (trends)...")
    df['temp_rolling_6'] = df['temperature_2m'].rolling(window=6).mean()
    df['temp_rolling_24'] = df['temperature_2m'].rolling(window=24).mean()

    print("Setting up target variables (what we want to predict)...")
    # What will the temperature be 3 hours from now?
    df['target_temp_3h'] = df['temperature_2m'].shift(-3)
    
    # Will there be rain 3 hours from now? (1 for Yes, 0 for No)
    df['target_rain_3h'] = (df['precipitation'].shift(-3) > 0).astype(int)

    # Drop rows with missing values caused by shifting data
    df.dropna(inplace=True)

    # Save the ready-to-train data as a CSV in the processed folder
    output_path = os.path.join("data", "processed", "ml_features.csv")
    df.to_csv(output_path)
    
    print(f"✅ Feature engineering complete! {len(df)} rows ready for ML.")
    print(f"Saved to: {output_path}")

if __name__ == "__main__":
    generate_features()