from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import ImageCaptionRoutes 

app = FastAPI(
    title="Image Caption Generator",
    description="Generates captions from image and instruction using OpenRouter API",
    version="1.0.0"
)

# CORS (if needed for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#routes
app.include_router(ImageCaptionRoutes.router, prefix="/api/v1", tags=["Caption Generator"])
