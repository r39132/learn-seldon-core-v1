"""FastAPI model serving endpoint (alternative to Seldon)."""
import os
from pathlib import Path

import joblib
from fastapi import FastAPI
from pydantic import BaseModel


class PredictionRequest(BaseModel):
    """Prediction request model."""

    text: str


class PredictionResponse(BaseModel):
    """Prediction response model."""

    prediction: str
    probability: float


# Initialize FastAPI app
app = FastAPI(title="Sentiment Model Server", version="1.0.0")

# Load model
MODEL_PATH = os.getenv("MODEL_PATH", "/mnt/models/sentiment_model.pkl")
model = None


@app.on_event("startup")
async def load_model():
    """Load the model on startup."""
    global model
    model_path = Path(MODEL_PATH)
    if model_path.exists():
        model = joblib.load(model_path)
        print(f"Model loaded from {model_path}")
    else:
        raise FileNotFoundError(f"Model not found at {model_path}")


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy", "model_loaded": model is not None}


@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """Make prediction."""
    if model is None:
        raise RuntimeError("Model not loaded")
    
    # Get prediction
    prediction = model.predict([request.text])[0]
    proba = model.predict_proba([request.text])[0]
    
    # Get confidence for predicted class
    confidence = float(max(proba))
    
    return PredictionResponse(
        prediction=prediction,
        probability=confidence
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
