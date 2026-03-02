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
          <div className="cards-row">
            {analysis.variants.map((v) => (
              <StyleVariantCard key={v.id} variant={v} />
            ))}
          </div>
        </>
      )}
    </div>
  );
}
