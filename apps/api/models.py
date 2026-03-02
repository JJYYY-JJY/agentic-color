from pydantic import BaseModel, Field
from typing import Literal
from datetime import datetime


class ColorParams(BaseModel):
    temperature: float = Field(..., ge=2000, le=50000)
    tint: float = Field(..., ge=-100, le=100)
    exposure: float = Field(..., ge=-5, le=5)
    contrast: float = Field(..., ge=-100, le=100)
    highlights: float = Field(..., ge=-100, le=100)
    shadows: float = Field(..., ge=-100, le=100)
    whites: float = Field(..., ge=-100, le=100)
    blacks: float = Field(..., ge=-100, le=100)
    vibrance: float = Field(..., ge=-100, le=100)
    saturation: float = Field(..., ge=-100, le=100)
    clarity: float = Field(..., ge=-100, le=100)
    dehaze: float = Field(..., ge=-100, le=100)


VariantId = Literal["clean_neutral", "warm_film", "moody_cinematic"]


class StyleVariant(BaseModel):
    id: VariantId
    label: str
    params: ColorParams


class ImageAnalysis(BaseModel):
    image_id: str
    filename: str
    analyzed_at: datetime
    variants: list[StyleVariant] = Field(..., min_length=3, max_length=3)


class AnalyzeResponse(BaseModel):
    analysis: ImageAnalysis
