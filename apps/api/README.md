# agentic-color API

FastAPI backend that accepts an image upload and returns three style variant presets.

## Setup

```bash
pip install -r requirements.txt
```

## Run

```bash
cd apps
uvicorn api.main:app --reload --port 8000
```

## Endpoints

| Method | Path       | Description                          |
|--------|------------|--------------------------------------|
| GET    | `/health`  | Health check                         |
| POST   | `/analyze` | Upload an image, get style variants  |

### POST /analyze

**Request:** `multipart/form-data` with a `file` field containing an image.

**Response:** `ImageAnalysis` JSON object with 3 `StyleVariant` entries.

```json
{
  "image_id": "uuid",
  "filename": "photo.jpg",
  "analyzed_at": "2024-01-01T00:00:00Z",
  "variants": [...]
}
```
