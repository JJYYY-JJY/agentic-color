# agentic-color

An agentic color-grading engine that analyzes images and generates multiple editable, parameter-based style presets — ready to export to darktable, Lightroom, or ComfyUI workflows.

---

## Architecture

```
agentic-color/
├── packages/
│   └── core/          # Shared JSON Schema (ImageAnalysis, StyleVariant)
└── apps/
    ├── api/           # FastAPI backend  (Python)
    └── web/           # React + Vite frontend  (TypeScript)
```

The **API** accepts an image upload, runs analysis (or mock variants in MVP), and returns a JSON `ImageAnalysis` object containing three `StyleVariant` presets.  
The **Web UI** uploads an image, receives the variants, and renders each as an editable card where every parameter can be tweaked before export.

---

## Getting started

### 1 — API

```bash
cd apps/api
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
# → http://localhost:8000/health
```

### 2 — Web

```bash
cd apps/web
npm install
npm run dev
# → http://localhost:5173
```

Open `http://localhost:5173`, upload any image, and the three style cards appear.

---

## Folder structure

```
packages/
  core/
    schema.json          # JSON Schema draft-07 for all shared types
    README.md

apps/
  api/
    main.py              # FastAPI app (GET /health, POST /analyze)
    models.py            # Pydantic v2 models
    analyzer.py          # analyze_image() — mock variants (swap for real ML)
    requirements.txt
    README.md

  web/
    index.html
    vite.config.ts
    tsconfig.json
    package.json
    src/
      main.tsx
      App.tsx / App.css
      types.ts            # TypeScript interfaces mirroring schema.json
      components/
        ImageUploader.tsx
        StyleVariantCard.tsx
    README.md
```

---

## Style variants (MVP)

| ID | Label | Character |
|----|-------|-----------|
| `clean_neutral` | Clean & Neutral | Balanced, slight vibrance boost |
| `warm_film` | Warm Film | 4200 K, lifted shadows, golden tones |
| `moody_cinematic` | Moody Cinematic | High contrast, crushed blacks, desaturated |

---

## How to extend

### Real image analysis
Replace the body of `apps/api/analyzer.py::analyze_image()` with your ML pipeline. The function signature and return type stay the same.

### darktable adapter
Export a `StyleVariant.params` dict as a darktable style XML (`.dtstyle`) by mapping each `ColorParams` field to the corresponding darktable module parameter.

### ComfyUI adapter
Map `ColorParams` fields to ComfyUI node inputs (e.g., `CLIPTextEncode` color-correction nodes) and POST the workflow JSON to the ComfyUI API.

### Lightroom / ACR
Serialize `ColorParams` to an `.xmp` sidecar file — field names already mirror Lightroom's develop settings.

