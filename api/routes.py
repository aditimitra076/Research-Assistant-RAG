from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def home():
    return {
        "message": "Reserach Assitant API is running."
    }