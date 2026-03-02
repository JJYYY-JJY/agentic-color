# @agentic-color/core

Shared JSON Schema definitions for the agentic-color project.

## Schema

`schema.json` defines two primary types using JSON Schema draft-07:

- **`ImageAnalysis`** — top-level result returned by the API after analyzing an image.
- **`StyleVariant`** — one of three style presets (`clean_neutral`, `warm_film`, `moody_cinematic`), each containing a `ColorParams` object.
- **`ColorParams`** — numeric light-room style parameters (temperature, tint, exposure, etc.)

## Usage

Reference the schema for validation in any language:

```bash
# Python (jsonschema)
python -c "import json, jsonschema; jsonschema.validate(data, json.load(open('schema.json')))"
```

The Pydantic models in `apps/api/models.py` and the TypeScript interfaces in `apps/web/src/types.ts` are both derived from this schema.
