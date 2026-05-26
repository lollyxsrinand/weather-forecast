import joblib
import pandas as pd
from pathlib import Path
from datetime import timedelta
from fastapi import HTTPException

BASE_DIR = Path(__file__).resolve().parent.parent.parent
MODELS_DIR = BASE_DIR / "models"

LOCATIONS = ["blr", "delhi", "hyd", "mumbai"]

class WeatherModelManager:
    def __init__(self):
        self.models = {}
        self.latest_data = {}
        
    def load_models(self):
        print("Preloading ML models from:", MODELS_DIR)
        for loc in LOCATIONS:
            loc_path = MODELS_DIR / loc
            if not loc_path.exists():
                print(f"Warning: Model directory for {loc} does not exist.")
                continue
            
            try:
                max_model = joblib.load(loc_path / "max.pkl")
                min_model = joblib.load(loc_path / "min.pkl")
                weather_model = joblib.load(loc_path / "weather.pkl")
                
                self.models[loc] = {
                    "max": max_model,
                    "min": min_model,
                    "weather": weather_model
                }
                
                # Load latest data from csv
                csv_path = BASE_DIR / f"{loc}.csv"
                if csv_path.exists():
                    df = pd.read_csv(csv_path)
                    df["time"] = pd.to_datetime(df["time"])
                    df["month"] = df["time"].dt.month
                    df["day"] = df["time"].dt.day
                    df["day_of_week"] = df["time"].dt.dayofweek
                    df["day_of_year"] = df["time"].dt.dayofyear
                    
                    features = [
                        "temperature_2m_max (°C)",
                        "temperature_2m_min (°C)",
                        "rain_sum (mm)",
                        "month",
                        "day",
                        "day_of_week",
                        "day_of_year",
                        "precipitation_sum (mm)",
                        "precipitation_hours (h)",
                        "sunshine_duration (s)",
                        "relative_humidity_2m_mean (%)",
                        "wind_speed_10m_max (km/h)",
                        "wind_direction_10m_dominant (°)",
                        "weather_code (wmo code)"
                    ]
                    
                    last_row = df.iloc[-1]
                    self.latest_data[loc] = {
                        "features": last_row[features].to_dict(),
                        "date": last_row["time"].date()
                    }
                    print(f"Successfully loaded models and data for location: {loc}")
            except Exception as e:
                print(f"Error loading models for {loc}: {e}")

    def predict_7_days(self, location: str):
        if location not in self.models or location not in self.latest_data:
            raise HTTPException(status_code=404, detail=f"Models or data not found for location: '{location}'. Available: {list(self.models.keys())}")
            
        models = self.models[location]
        current_input = pd.Series(self.latest_data[location]["features"])
        current_date = self.latest_data[location]["date"]
        
        weather_mapping = {
            "sunny": 0,
            "cloudy": 3,
            "rainy": 61,
            "foggy": 45,
            "snowy": 71,
            "stormy": 95,
            "other": 1
        }
        
        forecast = []
        for i in range(1, 8):
            next_date = current_date + timedelta(days=i)
            
            # Update date features in current_input
            current_input["month"] = next_date.month
            current_input["day"] = next_date.day
            current_input["day_of_week"] = next_date.weekday()
            current_input["day_of_year"] = next_date.timetuple().tm_yday
            
            # Predict
            input_df = pd.DataFrame([current_input])
            
            next_max = models["max"].predict(input_df)[0]
            next_min = models["min"].predict(input_df)[0]
            next_weather_label = models["weather"].predict(input_df)[0]
            
            # Store prediction
            forecast.append({
                "date": next_date,
                "max_temp": round(float(next_max), 1),
                "min_temp": round(float(next_min), 1),
                "weather": next_weather_label
            })
            
            # Update current_input for next iteration
            current_input["temperature_2m_max (°C)"] = next_max
            current_input["temperature_2m_min (°C)"] = next_min
            if next_weather_label in weather_mapping:
                current_input["weather_code (wmo code)"] = weather_mapping[next_weather_label]
            else:
                current_input["weather_code (wmo code)"] = 1 # default
                
        return forecast

# Instantiate a global model manager
model_manager = WeatherModelManager()
