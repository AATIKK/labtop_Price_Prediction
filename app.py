from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI(title="Laptop Price Predictor")

# Load model once
model = joblib.load("model.joblib")

class LaptopFeatures(BaseModel):
    brand: str
    cpu: str
    ram_gb: int
    storage_type: str
    storage_gb: int
    gpu: str | None = None
    screen_size_in: float | None = None
    os: str | None = None
    age_years: float | None = None
    condition: str | None = "used"

@app.post("/predict")
def predict(features: LaptopFeatures):
    X = [{
        "brand": features.brand,
        "cpu": features.cpu,
        "ram_gb": features.ram_gb,
        "storage_type": features.storage_type,
        "storage_gb": features.storage_gb,
        "gpu": features.gpu or "unknown",
        "screen_size_in": features.screen_size_in or 0.0,
        "os": features.os or "unknown",
        "age_years": features.age_years or 0.0,
        "condition": features.condition or "used",
    }]
    pred = model.predict(X)[0]
    # If you trained on log(price), apply np.exp here
    return {"predicted_price_usd": float(pred)}
