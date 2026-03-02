# agentic-color Web

React + TypeScript + Vite frontend for the agentic-color project.

## Setup & Run

```bash
npm install
npm run dev       # http://localhost:5173
```

## Build

```bash
npm run build     # output in dist/
npm run preview   # preview production build
```

## Key files

| File | Purpose |
|------|---------|
| `src/types.ts` | TypeScript interfaces matching the API schema |
| `src/components/ImageUploader.tsx` | File picker + upload form |
| `src/components/StyleVariantCard.tsx` | Editable style-variant card |
| `src/App.tsx` | Root component, upload → results flow |
