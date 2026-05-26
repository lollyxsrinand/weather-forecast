from pydantic import BaseModel
from typing import List
from datetime import date

class DailyForecast(BaseModel):
    date: date
    max_temp: float
    min_temp: float
    weather: str

class ForecastResponse(BaseModel):
    location: str
    forecast: List[DailyForecast]
