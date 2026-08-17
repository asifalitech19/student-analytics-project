from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.ml.predictor import (
    predict_cgpa,
    get_prediction_options,
    prediction_service_status,
)

router = APIRouter(prefix="/api/predict", tags=["Prediction"])

class PredictionRequest(BaseModel):
    age: float = Field(..., ge=15, le=80)
    gender: str
    relationship_status: str
    living_arrangement: str
    health_issues: str
    physical_disability: str
    admission_year: int = Field(..., ge=1990, le=2035)
    hsc_year: int = Field(..., ge=1990, le=2035)
    scholarship: str
    english_proficiency: str
    study_hours: float = Field(..., ge=0, le=24)
    study_sessions: float = Field(..., ge=0, le=30)
    social_media_hours: float = Field(..., ge=0, le=24)
    skill_development_hours: float = Field(..., ge=0, le=24)
    current_semester: float = Field(..., ge=1, le=12)
    attendance: float = Field(..., ge=0, le=100)
    completed_credits: float = Field(..., ge=0, le=145)

@router.get("/options")
def prediction_options():
    try:
        return {"success": True, **get_prediction_options()}
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Unable to load prediction options: {error}")

@router.get("/health")
def prediction_health():
    status = prediction_service_status()
    if status.get("status") != "ready":
        raise HTTPException(status_code=503, detail=status.get("message", "Prediction service is not ready."))
    return {"success": True, **status}

@router.post("/")
def predict(request: PredictionRequest):
    try:
        result = predict_cgpa(
            age=request.age, gender=request.gender,
            relationship_status=request.relationship_status,
            living_arrangement=request.living_arrangement,
            health_issues=request.health_issues,
            physical_disability=request.physical_disability,
            admission_year=request.admission_year,
            hsc_year=request.hsc_year,
            scholarship=request.scholarship,
            english_proficiency=request.english_proficiency,
            study_hours=request.study_hours,
            study_sessions=request.study_sessions,
            social_media_hours=request.social_media_hours,
            skill_development_hours=request.skill_development_hours,
            current_semester=request.current_semester,
            attendance=request.attendance,
            completed_credits=request.completed_credits,
        )
        return {"success": True, "prediction": result}
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
    except Exception as error:
        print(f"[PREDICTION API ERROR] {error}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {error}")


    



