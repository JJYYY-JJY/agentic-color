/// <reference types="vite/client" />
import { useRef, useState } from "react";
import type { ImageAnalysis } from "../types";

const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

interface Props {
  onResult: (analysis: ImageAnalysis) => void;
}

export function ImageUploader({ onResult }: Props) {
  const [loading, setLoading] = useState(false);
  const [filename, setFilename] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const fileRef = useRef<HTMLInputElement>(null);

  const handleAnalyze = async () => {
    const file = fileRef.current?.files?.[0];
    if (!file) return;

    setLoading(true);
    setError(null);

    const form = new FormData();
    form.append("file", file);

    try {
      const res = await fetch(`${API_URL}/analyze`, {
        method: "POST",
        body: form,
      });
      if (!res.ok) throw new Error(`Server error: ${res.status}`);
      const data: ImageAnalysis = await res.json();
      onResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="uploader">
      <label className="upload-zone">
        <input
          ref={fileRef}
          type="file"
          accept="image/jpeg,image/png,.dng,.cr2,.nef,.arw,.rw2"
          onChange={(e) => setFilename(e.target.files?.[0]?.name ?? null)}
        />
        {filename ? <span className="filename">{filename}</span> : <span className="placeholder">Click or drag JPG/PNG/DNG/CR2/NEF/ARW/RW2</span>}
      </label>
      <button className="analyze-btn" onClick={handleAnalyze} disabled={loading || !filename}>
        {loading ? "Analyzing…" : "Analyze"}
      </button>
      {error && <p className="error">{error}</p>}
    </div>
  );
}
