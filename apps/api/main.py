import os

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from .analyzer import analyze_image
from .models import ImageAnalysis

app = FastAPI(title="agentic-color API")

_cors_origins = [
    o.strip()
    for o in os.environ.get("CORS_ORIGINS", "http://localhost:5173").split(",")
    if o.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}


@app.post("/analyze", response_model=ImageAnalysis)
async def analyze(file: UploadFile = File(...)) -> ImageAnalysis:
    image_bytes = await file.read()
    return analyze_image(image_bytes, file.filename or "upload")
