import { useState, useEffect } from "react";
import type { StyleVariant } from "../types";
import type { ColorParams } from "../types";

interface Props {
  variant: StyleVariant;
}

type ParamKey = keyof ColorParams;

const PARAM_KEYS: ParamKey[] = [
  "temperature", "tint", "exposure", "contrast",
  "highlights", "shadows", "whites", "blacks",
  "vibrance", "saturation", "clarity", "dehaze",
];

export function StyleVariantCard({ variant }: Props) {
  const [params, setParams] = useState<ColorParams>({ ...variant.params });

  useEffect(() => {
    setParams({ ...variant.params });
  }, [variant]);

  const handleChange = (key: ParamKey, value: number) => {
    setParams((prev) => ({ ...prev, [key]: value }));
  };

  return (
    <div className="card">
      <h2 className="card-title">{variant.label}</h2>
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
