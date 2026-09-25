import pandas as pd
import os
import pickle
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score
from xgboost import XGBClassifier

def train_rain_model():
    print("Loading engineered features...")
    data_path = os.path.join("data", "processed", "ml_features.csv")
    
    if not os.path.exists(data_path):
        print("Error: Feature data not found. Run feature_engineering.py first.")
        return

    df = pd.read_csv(data_path, index_col='time')

    # The features used to make the prediction
    features = [
        'hour', 'month', 'temperature_2m', 'relative_humidity_2m', 
        'precipitation', 'wind_speed_10m', 'surface_pressure', 'cloud_cover',
        'temp_lag_1', 'humidity_lag_1', 'rain_lag_1', 
        'temp_rolling_6', 'temp_rolling_24'
    ]
    
    X = df[features]
    y = df['target_rain_3h'] # 1 for rain, 0 for no rain

    # Split the data (shuffle=False for time-series data)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    print(f"Training XGBoost Classifier on {len(X_train)} records...")
    
    # Calculate ratio to handle class imbalance (since "no rain" is much more common)
    rain_ratio = (len(y_train) - sum(y_train)) / sum(y_train) if sum(y_train) > 0 else 1
    
    model = XGBClassifier(n_estimators=100, learning_rate=0.1, max_depth=5, 
                          scale_pos_weight=rain_ratio, random_state=42)
    model.fit(X_train, y_train)

    print("Evaluating model on test data...")
    predictions = model.predict(X_test)
    
    accuracy = accuracy_score(y_test, predictions)
    precision = precision_score(y_test, predictions, zero_division=0)
    recall = recall_score(y_test, predictions, zero_division=0)

    print("\n--- Rain Model Performance ---")
    print(f"Accuracy:  {accuracy * 100:.1f}% (Overall correctness)")
    print(f"Precision: {precision * 100:.1f}% (When it predicts rain, how often is it right?)")
    print(f"Recall:    {recall * 100:.1f}% (Of all actual rain events, how many did it catch?)")
    print("------------------------------")

    # Save the trained model
    model_path = os.path.join("models", "rain_model.pkl")
    with open(model_path, 'wb') as file:
        pickle.dump(model, file)
        
    print(f"\n✅ Rain model saved to {model_path}")

if __name__ == "__main__":
    train_rain_model()