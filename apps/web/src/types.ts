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
}

export type VariantId = "clean_neutral" | "warm_film" | "moody_cinematic";

export interface StyleVariant {
  id: VariantId;
  label: string;
  params: ColorParams;
}

export interface ImageAnalysis {
  image_id: string;
  filename: string;
  analyzed_at: string;
  variants: StyleVariant[];
}
