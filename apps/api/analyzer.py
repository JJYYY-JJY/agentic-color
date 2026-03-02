import uuid
from datetime import datetime, timezone

from models import ColorParams, ImageAnalysis, StyleVariant


def analyze_image(image_bytes: bytes, filename: str) -> ImageAnalysis:
    """Return mock style variants for the uploaded image."""
    return ImageAnalysis(
        image_id=str(uuid.uuid4()),
        filename=filename,
        analyzed_at=datetime.now(timezone.utc),
        variants=[
            StyleVariant(
                id="clean_neutral",
                label="Clean & Neutral",
                params=ColorParams(
                    temperature=5500,
                    tint=0,
                    exposure=0.0,
                    contrast=5,
                    highlights=-10,
                    shadows=5,
                    whites=5,
                    blacks=-5,
                    vibrance=10,
                    saturation=0,
                    clarity=5,
                    dehaze=0,
                ),
            ),
            StyleVariant(
                id="warm_film",
                label="Warm Film",
                params=ColorParams(
                    temperature=4200,
                    tint=8,
                    exposure=0.3,
                    contrast=15,
                    highlights=-20,
                    shadows=20,
                    whites=10,
                    blacks=-15,
                    vibrance=20,
                    saturation=10,
                    clarity=10,
                    dehaze=5,
                ),
            ),
            StyleVariant(
                id="moody_cinematic",
                label="Moody Cinematic",
                params=ColorParams(
                    temperature=6200,
                    tint=-5,
                    exposure=-0.5,
                    contrast=40,
                    highlights=-40,
                    shadows=-20,
                    whites=-10,
                    blacks=-30,
                    vibrance=-10,
                    saturation=-15,
                    clarity=25,
                    dehaze=15,
                ),
            ),
        ],
    )
