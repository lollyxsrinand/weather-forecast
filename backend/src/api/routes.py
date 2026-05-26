from fastapi import APIRouter, Path
from schemas.weather import ForecastResponse
from services.ml_models import model_manager

router = APIRouter()

@router.get("/forecast/{location}", response_model=ForecastResponse, summary="Get 7-day weather forecast for a location")
def get_forecast(
    location: str = Path(..., description="The name of the location (e.g., blr, delhi, hyd, mumbai)")
):
    """
    Returns a 7-day weather forecast for the specified location based on pre-trained ML models.
    """
    # Location should be case-insensitive to handle 'Delhi', 'DELHI', etc.
    location = location.lower()
    
    forecast_data = model_manager.predict_7_days(location)
    
    return ForecastResponse(
        location=location,
        forecast=forecast_data
    )
