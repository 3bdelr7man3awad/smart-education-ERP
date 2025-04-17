from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Union
from app.ml.grading_model import AutoGradingModel
from app.ml.performance_predictor import PerformancePredictor
from app.core.auth import get_current_user
from pydantic import BaseModel
import os

router = APIRouter()

# Initialize models
grading_model = AutoGradingModel()
performance_predictor = PerformancePredictor()

class GradingRequest(BaseModel):
    answer: str
    correct_answer: str

class GradingResponse(BaseModel):
    predicted_grade: int
    confidence: float

class PerformanceData(BaseModel):
    attendance_rate: float
    assignment_completion: float
    quiz_average: float
    study_hours: float

class PerformancePrediction(BaseModel):
    predicted_performance: float
    confidence_interval: Dict[str, float]

class TrainingResponse(BaseModel):
    status: str
    metrics: Dict[str, float]

@router.post("/train/grading", response_model=TrainingResponse)
async def train_grading_model(current_user: dict = Depends(get_current_user)):
    """Train the auto-grading model with sample data."""
    try:
        # Generate sample data and train model
        sample_data = grading_model.generate_sample_data(100)
        metrics = grading_model.train(sample_data)
        
        return {
            "status": "success",
            "metrics": metrics
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/train/performance", response_model=TrainingResponse)
async def train_performance_model(current_user: dict = Depends(get_current_user)):
    """Train the performance prediction model with sample data."""
    try:
        # Generate sample data and train model
        sample_data = performance_predictor.generate_sample_data(100)
        metrics = performance_predictor.train(sample_data)
        
        return {
            "status": "success",
            "metrics": metrics
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/predict/grade", response_model=GradingResponse)
async def predict_grade(
    request: GradingRequest,
    current_user: dict = Depends(get_current_user)
):
    """Predict the grade for a given answer."""
    try:
        prediction = grading_model.predict(request.answer, request.correct_answer)
        return prediction
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/predict/performance", response_model=PerformancePrediction)
async def predict_performance(
    data: PerformanceData,
    current_user: dict = Depends(get_current_user)
):
    """Predict student performance based on current metrics."""
    try:
        prediction = performance_predictor.predict(data.dict())
        return prediction
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/models/status")
async def get_models_status(current_user: dict = Depends(get_current_user)):
    """Get the training status of all ML models."""
    return {
        "grading_model": {
            "trained": grading_model.is_trained,
            "model_file_exists": os.path.exists(grading_model.model_path)
        },
        "performance_model": {
            "trained": performance_predictor.is_trained,
            "model_file_exists": os.path.exists(performance_predictor.model_path)
        }
    } 