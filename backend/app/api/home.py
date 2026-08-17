from fastapi import APIRouter

router = APIRouter()

@router.get("/about")
def about():
    return {
        "project": "AI Student Analytics Dashboard",
        "developer": "Asif Ali",
        "version": "1.0"
    }