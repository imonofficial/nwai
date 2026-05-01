from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from utils.helpers import dummy_ml_predict, logger

router = APIRouter()

# Input Validation Model
class PredictRequest(BaseModel):
    text: str = Field(..., min_length=1, description="The input text to be processed by the AI.")
    
# Output Validation Model
class PredictResponse(BaseModel):
    summary: str
    word_count: int
    confidence: float
    model_version: str

@router.get("/", tags=["Health"])
async def health_check():
    """
    Health check endpoint to ensure the service is running.
    """
    return {"status": "ok", "message": "AI API is up and running!"}

@router.post("/predict", response_model=PredictResponse, tags=["AI Prediction"])
async def predict(request: PredictRequest):
    """
    Accepts JSON input and returns an AI-generated output.
    """
    try:
        logger.info("Received prediction request.")
        
        # Call the machine learning helper function
        result = dummy_ml_predict(request.text)
        
        return result
    except Exception as e:
        logger.error(f"Error during prediction: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error during prediction.")
