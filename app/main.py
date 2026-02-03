"""
FastAPI Inference Service - Milestone 1

Implements:
- Health check endpoint
- Prediction endpoint
- Pydantic request/response validation
- Eager model loading (startup)
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import pickle
import numpy as np
from pathlib import Path


##App initialization

app = FastAPI(
    title="Iris Classifier API",
    description="Milestone 1: FastAPI model serving",
    version="1.0.0",
)


##Model loading (eager / startup)

MODEL_PATH = Path(__file__).resolve().parent.parent / "model.pkl"

try:
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
except Exception as e:
    model = None
    print(f"Failed to load model: {e}")


##Pydantic Schemas

class PredictionRequest(BaseModel):
    """Input schema for prediction endpoint."""

    sepal_length: float = Field(..., gt=0, example=5.1)
    sepal_width: float = Field(..., gt=0, example=3.5)
    petal_length: float = Field(..., gt=0, example=1.4)
    petal_width: float = Field(..., gt=0, example=0.2)


class PredictionResponse(BaseModel):
    """Output schema for prediction endpoint."""

    prediction: int
    model_version: str



##Endpoints

@app.get("/health")
def health_check():
    """Health check for deployment and monitoring."""
    return {
        "status": "healthy",
        "model_loaded": model is not None,
    }


@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    """
    Generate a prediction from iris input features.
    """

    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    features = np.array(
        [[
            request.sepal_length,
            request.sepal_width,
            request.petal_length,
            request.petal_width,
        ]]
    )

    prediction = model.predict(features)[0]

    return PredictionResponse(
        prediction=int(prediction),
        model_version="1.0.0",
    )



##Entry point (Cloud Run compatible)

if __name__ == "__main__":
    import os
    import uvicorn

    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
