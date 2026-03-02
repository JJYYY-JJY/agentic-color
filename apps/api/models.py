from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


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
    texture: float = Field(..., ge=-100, le=100)
    sharpen: float = Field(..., ge=0, le=100)
    noise_reduction: float = Field(..., ge=0, le=100)
    color_boost: float = Field(..., ge=-100, le=100)


class SceneAnalysis(BaseModel):
    scene_type: str
    key_issues: list[str]
    recommendation: str


class ModelCapability(BaseModel):
    provider: Literal["openai", "google", "anthropic"]
    model: str
    vision_input: bool = True


class StyleVariant(BaseModel):
    id: str
    label: str
    intent: str
    confidence: float = Field(..., ge=0, le=1)
    params: ColorParams
    preview_data_url: str


class ImageAnalysis(BaseModel):
    image_id: str
    filename: str
    analyzed_at: datetime
    original_preview_data_url: str
    scene_analysis: SceneAnalysis
    compatible_models: list[ModelCapability]
    variants: list[StyleVariant] = Field(..., min_length=3)
