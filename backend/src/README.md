# Weather Prediction Backend API

A clean, modular FastAPI backend for serving 7-day weather predictions using pre-trained machine learning models.

## Project Structure

```
backend/
├── main.py                   # FastAPI app instance and lifespan management
├── requirements.txt          # Python dependencies
├── api/
│   ├── __init__.py
│   └── routes.py             # API endpoints (e.g. /forecast/{location})
├── schemas/
│   ├── __init__.py
│   └── weather.py            # Pydantic models for validation and response schemas
└── services/
    ├── __init__.py
    └── ml_models.py          # Machine learning model loading and 7-day inference logic
```

## Setup Instructions

1. **Activate the environment**:
Ensure your Conda environment is activated (based on your earlier setup, it seems to be `dsenv`).
```bash
conda activate dsenv
```

2. **Navigate to the backend directory**:
```bash
cd backend
```

3. **Install Dependencies**:
(If you haven't already installed them in your environment)
```bash
pip install -r requirements.txt
```

4. **Run the FastAPI Server**:
Use `uvicorn` to start the server with auto-reload enabled.
```bash
uvicorn main:app --reload
```

## API Usage

Once the server is running, you can access the API documentation at:
http://127.0.0.1:8000/docs

### Endpoint: `GET /forecast/{location}`

**Description**: Get a 7-day weather forecast for a specific location.

**Valid Locations**: `blr`, `delhi`, `hyd`, `mumbai` (case-insensitive).

**Example Request**:
```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/forecast/delhi' \
  -H 'accept: application/json'
```

**Example Response**:
```json
{
  "location": "delhi",
  "forecast": [
    {
      "date": "2026-05-26",
      "max_temp": 43.4,
      "min_temp": 29.7,
      "weather": "cloudy"
    },
    ...
  ]
}
```
