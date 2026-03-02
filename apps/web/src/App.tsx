import { useState } from "react";
import { ImageUploader } from "./components/ImageUploader";
import { StyleVariantCard } from "./components/StyleVariantCard";
import type { ImageAnalysis } from "./types";
import "./App.css";

export default function App() {
  const [analysis, setAnalysis] = useState<ImageAnalysis | null>(null);

  return (
    <div className="app">
      <h1 className="app-title">agentic-color</h1>
      {analysis === null ? (
        <ImageUploader onResult={setAnalysis} />
      ) : (
        <>
          <button className="reset-btn" onClick={() => setAnalysis(null)}>
            ← Reset
          </button>
          <p className="filename-label">{analysis.filename}</p>
          <p className="scene-line">
            Scene: {analysis.scene_analysis.scene_type} · Issues: {analysis.scene_analysis.key_issues.join(", ")}
          </p>
          <p className="scene-line">Recommendation: {analysis.scene_analysis.recommendation}</p>
          <p className="scene-line">Vision API adapters: {analysis.compatible_models.map((m) => `${m.provider}/${m.model}`).join(" · ")}</p>
          <div className="cards-row">
            {analysis.variants.map((v) => (
              <StyleVariantCard key={`${analysis.image_id}-${v.id}`} variant={v} originalPreview={analysis.original_preview_data_url} />
            ))}
          </div>
        </>
      )}
    </div>
  );
}
