export interface ColorParams {
  temperature: number;
  tint: number;
  exposure: number;
  contrast: number;
  highlights: number;
  shadows: number;
  whites: number;
  blacks: number;
  vibrance: number;
  saturation: number;
  clarity: number;
  dehaze: number;
  texture: number;
  sharpen: number;
  noise_reduction: number;
  color_boost: number;
}

export interface SceneAnalysis {
  scene_type: string;
  key_issues: string[];
  recommendation: string;
}

export interface ModelCapability {
  provider: "openai" | "google" | "anthropic";
  model: string;
  vision_input: boolean;
}

export interface StyleVariant {
  id: string;
  label: string;
  intent: string;
  confidence: number;
  params: ColorParams;
  preview_data_url: string;
}

export interface ImageAnalysis {
  image_id: string;
  filename: string;
  analyzed_at: string;
  original_preview_data_url: string;
  scene_analysis: SceneAnalysis;
  compatible_models: ModelCapability[];
  variants: StyleVariant[];
}
