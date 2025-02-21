import uvicorn
from fastapi import FastAPI
from src.processing_service.modules.processing.api.api import app as processing_app
from src.processing_service.config.database import init_models
from src.processing_service.config.settings import Settings

settings = Settings()

app = FastAPI(title="Processing Service")

# Mount the processing module
app.mount("/processing", processing_app)


@app.on_event("startup")
async def startup_event():
    # Initialize database models
    await init_models()


if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.API_HOST, port=settings.API_PORT, reload=True)
