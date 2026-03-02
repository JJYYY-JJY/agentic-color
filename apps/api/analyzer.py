import base64
import io
import uuid
from datetime import datetime, timezone

import numpy as np
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

from .models import ColorParams, ImageAnalysis, ModelCapability, SceneAnalysis, StyleVariant

try:
    import rawpy  # type: ignore
except Exception:  # optional dependency
    rawpy = None

RAW_EXTENSIONS = {".dng", ".cr2", ".nef", ".arw", ".rw2"}


def _to_data_url(image: Image.Image) -> str:
    out = io.BytesIO()
    image.save(out, format="JPEG", quality=85)
    encoded = base64.b64encode(out.getvalue()).decode("ascii")
    return f"data:image/jpeg;base64,{encoded}"


def _open_image(image_bytes: bytes, filename: str) -> Image.Image:
    ext = filename.lower().rsplit(".", 1)
    suffix = f".{ext[-1]}" if len(ext) > 1 else ""
    try:
        if suffix in RAW_EXTENSIONS:
            if rawpy is None:
                raise ValueError("RAW file support requires rawpy to be installed")
            with rawpy.imread(io.BytesIO(image_bytes)) as raw:
                rgb = raw.postprocess(use_camera_wb=True, output_bps=8)
                return Image.fromarray(rgb).convert("RGB")

        img = Image.open(io.BytesIO(image_bytes))
        return ImageOps.exif_transpose(img).convert("RGB")
    except ValueError:
        raise
    except Exception as exc:
        raise ValueError(f"Unsupported or corrupted image input: {filename}") from exc


def _clip(value: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, value))


def _analyze_scene(img: Image.Image) -> SceneAnalysis:
    arr = np.asarray(img).astype(np.float32) / 255.0
    luma = (0.2126 * arr[:, :, 0] + 0.7152 * arr[:, :, 1] + 0.0722 * arr[:, :, 2]).mean()
    warm_bias = float(arr[:, :, 0].mean() - arr[:, :, 2].mean())

    issues: list[str] = []
    if luma < 0.38:
        issues.append("underexposed")
    elif luma > 0.72:
        issues.append("overexposed")
    else:
        issues.append("balanced_exposure")

    if warm_bias > 0.08:
        issues.append("warm_color_cast")
    elif warm_bias < -0.08:
        issues.append("cool_color_cast")
    else:
        issues.append("neutral_white_balance")

    scene_type = "portrait_or_subject" if arr.std() < 0.22 else "landscape_or_complex_scene"
    recommendation = "Generate 3+ variants and choose by mood while preserving detail in highlights/shadows."
    return SceneAnalysis(scene_type=scene_type, key_issues=issues, recommendation=recommendation)


def _apply_params(img: Image.Image, params: ColorParams) -> Image.Image:
    # Exposure + contrast
    expo_factor = 2 ** (params.exposure * 0.5)
    out = ImageEnhance.Brightness(img).enhance(expo_factor)
    out = ImageEnhance.Contrast(out).enhance(1 + params.contrast / 200)

    # Saturation and vibrance approximation
    sat_factor = 1 + (params.saturation + params.vibrance * 0.6) / 200
    out = ImageEnhance.Color(out).enhance(max(0.1, sat_factor))

    # Temperature/tint approximation in RGB
    arr = np.asarray(out).astype(np.float32)
    temp_shift = (params.temperature - 5500) / 12000
    tint_shift = params.tint / 400
    arr[:, :, 0] *= 1 + temp_shift
    arr[:, :, 2] *= 1 - temp_shift
    arr[:, :, 1] *= 1 + tint_shift

    # Whites/blacks/highlights/shadows (approximate global tone mapping)
    tone = arr / 255.0
    tone = np.clip(tone + params.whites / 500 - params.blacks / 500, 0, 1)
    tone = np.where(tone > 0.6, np.clip(tone + params.highlights / 500, 0, 1), tone)
    tone = np.where(tone < 0.4, np.clip(tone + params.shadows / 500, 0, 1), tone)

    # Dehaze and color_boost simple boosts
    tone = np.clip((tone - 0.5) * (1 + params.dehaze / 300) + 0.5, 0, 1)
    tone = np.clip(tone * (1 + params.color_boost / 300), 0, 1)

    out = Image.fromarray((tone * 255).astype(np.uint8), mode="RGB")

    # Clarity/texture/sharpen/noise reduction approximation
    if params.clarity > 0 or params.texture > 0:
        out = out.filter(ImageFilter.UnsharpMask(radius=1.8, percent=int(40 + params.clarity), threshold=3))
    if params.sharpen > 0:
        out = out.filter(ImageFilter.UnsharpMask(radius=1.2, percent=int(50 + params.sharpen), threshold=2))
    if params.noise_reduction > 0:
        out = out.filter(ImageFilter.GaussianBlur(radius=params.noise_reduction / 100))

    return out


def analyze_image(image_bytes: bytes, filename: str) -> ImageAnalysis:
    image = _open_image(image_bytes, filename)
    image.thumbnail((768, 768))

    scene = _analyze_scene(image)

    base = {
        "temperature": 5500,
        "tint": 0,
        "exposure": 0.0,
        "contrast": 8,
        "highlights": -8,
        "shadows": 10,
        "whites": 6,
        "blacks": -6,
        "vibrance": 8,
        "saturation": 0,
        "clarity": 5,
        "dehaze": 2,
        "texture": 8,
        "sharpen": 25,
        "noise_reduction": 10,
        "color_boost": 5,
    }

    if "underexposed" in scene.key_issues:
        base["exposure"] = 0.35
        base["shadows"] = 18
    if "overexposed" in scene.key_issues:
        base["exposure"] = -0.2
        base["highlights"] = -22

    variants_spec = [
        ("clean_neutral", "Clean Neutral", "Natural correction with realistic colors", 0.88, {}),
        ("warm_film", "Warm Film", "Warm, nostalgic, softer highlight roll-off", 0.82, {"temperature": 6200, "tint": 6, "saturation": 8, "contrast": 14, "dehaze": 6, "color_boost": 10}),
        ("moody_cinematic", "Moody Cinematic", "Low-key cinematic mood with controlled saturation", 0.8, {"exposure": -0.25, "contrast": 28, "highlights": -28, "shadows": -12, "saturation": -8, "clarity": 20, "dehaze": 12, "temperature": 5200}),
    ]

    variants: list[StyleVariant] = []
    for vid, label, intent, confidence, patch in variants_spec:
        values = {**base, **patch}
        params = ColorParams(**{k: _clip(v, 2000, 50000) if k == "temperature" else _clip(v, -100, 100) if k not in {"exposure", "sharpen", "noise_reduction"} else _clip(v, -5, 5) if k == "exposure" else _clip(v, 0, 100) for k, v in values.items()})
        preview = _apply_params(image, params)
        variants.append(
            StyleVariant(
                id=vid,
                label=label,
                intent=intent,
                confidence=confidence,
                params=params,
                preview_data_url=_to_data_url(preview),
            )
        )

    return ImageAnalysis(
        image_id=str(uuid.uuid4()),
        filename=filename,
        analyzed_at=datetime.now(timezone.utc),
        original_preview_data_url=_to_data_url(image),
        scene_analysis=scene,
        compatible_models=[
            ModelCapability(provider="openai", model="gpt-4.1-mini"),
            ModelCapability(provider="google", model="gemini-2.0-flash"),
            ModelCapability(provider="anthropic", model="claude-3-5-sonnet"),
        ],
        variants=variants,
    )
