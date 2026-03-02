import { useState } from "react";
import type { ColorParams, StyleVariant } from "../types";

interface Props {
  variant: StyleVariant;
  originalPreview: string;
}

type ParamKey = keyof ColorParams;

const PARAM_KEYS: ParamKey[] = [
  "temperature", "tint", "exposure", "contrast",
  "highlights", "shadows", "whites", "blacks",
  "vibrance", "saturation", "clarity", "dehaze",
  "texture", "sharpen", "noise_reduction", "color_boost",
];

export function StyleVariantCard({ variant, originalPreview }: Props) {
  const [params, setParams] = useState<ColorParams>({ ...variant.params });

  const handleChange = (key: ParamKey, value: number) => {
    setParams((prev) => ({ ...prev, [key]: value }));
  };

  return (
    <div className="card">
      <h2 className="card-title">{variant.label}</h2>
      <p className="intent">{variant.intent}</p>
      <p className="confidence">confidence: {(variant.confidence * 100).toFixed(0)}%</p>

      <div className="compare-grid">
        <div>
          <p className="preview-label">Original</p>
          <img src={originalPreview} className="preview" alt="original" />
        </div>
        <div>
          <p className="preview-label">Variant</p>
          <img src={variant.preview_data_url} className="preview" alt={variant.label} />
        </div>
      </div>

      <div className="params">
        {PARAM_KEYS.map((key) => (
          <div className="param-row" key={key}>
            <label className="param-label">{key}</label>
            <input
              type="number"
              className="param-input"
              value={params[key]}
              onChange={(e) => handleChange(key, Number(e.target.value))}
            />
          </div>
        ))}
      </div>
    </div>
  );
}
