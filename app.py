import os
from fastapi import FastAPI
from dotenv import load_dotenv
import uvicorn
from routes.api import router as api_router

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="AI Backend API",
    description="A production-ready AI backend built with FastAPI",
    version="1.0.0"
)

# Include API routes
app.include_router(api_router)

if __name__ == "__main__":
    # Get port from environment variable for Render compatibility
    port = int(os.environ.get("PORT", 8000))
    
    # Run the application using uvicorn
    # Use reload=True only in development mode
    is_dev = os.environ.get("ENVIRONMENT") == "development"
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=is_dev)
