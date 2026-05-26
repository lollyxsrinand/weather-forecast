from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from api.routes import router
from services.ml_models import model_manager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Preload models at startup
    model_manager.load_models()
    yield
    # Clean up at shutdown

app = FastAPI(
    title="Weather Prediction API",
    description="A FastAPI backend for serving 7-day weather predictions using ML models.",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/", tags=["Health"])
def read_root():
    return {"message": "Welcome to the Weather Prediction API. Go to /docs for the API documentation."}
