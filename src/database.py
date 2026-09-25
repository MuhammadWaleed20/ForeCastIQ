import sqlite3
import pandas as pd
import os

DB_PATH = os.path.join("data", "weather.db")

def init_db():
    """Creates the SQLite database and necessary tables if they don't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Table for historical and daily weather data
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS weather_data (
            time TEXT PRIMARY KEY,
            temperature_2m REAL,
            relative_humidity_2m REAL,
            precipitation REAL,
            wind_speed_10m REAL,
            surface_pressure REAL,
            cloud_cover REAL,
            weather_code INTEGER
        )
    ''')
    
    # We will use these tables later in the project
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prediction_time TEXT,
            target_time TEXT,
            predicted_temperature REAL,
            predicted_rain REAL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            alert_type TEXT,
            severity TEXT,
            status TEXT
        )
    ''')
    
    conn.commit()
    conn.close()
    print(f"✅ Database initialized at {DB_PATH}")

def save_weather_to_db(df):
    """Saves a Pandas DataFrame of weather data into the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    
    try:
        # to_sql automatically matches dataframe columns to table columns
        # if_exists='append' ensures we add new data without deleting old data
        df.to_sql('weather_data', conn, if_exists='append', index=False)
        print(f"✅ Successfully inserted {len(df)} rows into the database.")
    except sqlite3.IntegrityError:
        print("⚠️ Warning: Some records already exist in the database (duplicate timestamps).")
    except Exception as e:
        print(f"❌ Database error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    init_db()