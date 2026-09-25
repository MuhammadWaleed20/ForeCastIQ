import pandas as pd
import os
import pickle
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from xgboost import XGBRegressor

def train_temperature_model():
    print("Loading engineered features...")
    data_path = os.path.join("data", "processed", "ml_features.csv")
    df = pd.read_csv(data_path, index_col='time')

    # Define the features (X) we want the model to learn from
    features = [
        'hour', 'month', 'temperature_2m', 'relative_humidity_2m', 
        'precipitation', 'wind_speed_10m', 'surface_pressure', 'cloud_cover',
        'temp_lag_1', 'temp_lag_3', 'temp_lag_24', 
        'temp_rolling_6', 'temp_rolling_24'
    ]
    
    X = df[features]
    y = df['target_temp_3h'] # What we are trying to predict

    # Split the data: 80% for training, 20% for testing. 
    # shuffle=False ensures we don't mix future data into past training data (Time Series rule)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    print(f"Training XGBoost Model on {len(X_train)} records...")
    model = XGBRegressor(n_estimators=100, learning_rate=0.1, max_depth=5, random_state=42)
    model.fit(X_train, y_train)

    print("Evaluating model on test data...")
    predictions = model.predict(X_test)
    
    mae = mean_absolute_error(y_test, predictions)
    rmse = mean_squared_error(y_test, predictions) ** 0.5
    r2 = r2_score(y_test, predictions)

    print("\n--- Model Performance ---")
    print(f"MAE:  {mae:.2f}°C (Average error margin)")
    print(f"RMSE: {rmse:.2f}°C")
    print(f"R²:   {r2:.2f} (1.0 is perfect)")
    print("-------------------------")

    # Save the trained model to a file so FastAPI can load it later
    model_path = os.path.join("models", "temperature_model.pkl")
    with open(model_path, 'wb') as file:
        pickle.dump(model, file)
        
    print(f"\n✅ Temperature model saved to {model_path}")

if __name__ == "__main__":
    train_temperature_model()