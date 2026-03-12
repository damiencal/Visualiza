import type { Product, SurfaceType } from "./product";
import type { RoomType } from "./property";

export interface RoomDimensions {
  width: number; // meters
  length: number; // meters
  height: number; // meters
}

export interface BomItem {
  productId: string;
  product: Product;
  surfaceId: string;
  surfaceType: SurfaceType | string;
  surfaceLabel: string;
  areaM2: number;
  coveragePerUnit: number;
  quantity: number;
  unitPrice: number;
  totalPrice: number;
  currency: "DOP" | "USD";
}

export interface AIDesignAnalysis {
  score: number;
  summary: string;
  suggestions: string[];
  colorHarmony: string;
  styleMatch: string;
  estimatedCoverage: string;
}

export interface Surface {
  id: string;
  type: SurfaceType;
  mask: string;
  label: string;
  isSelected: boolean;
}

export interface VisualizerLayer {
  id: string;
  surfaceId: string;
  productId: string;
  product: Product;
  opacity: number;
  blendMode: string;
  transform: {
    scale: number;
    rotation: number;
    offsetX: number;
    offsetY: number;
  };
}

export interface VisualizerSnapshot {
  timestamp: number;
  layers: VisualizerLayer[];
  thumbnail?: string;
}

export interface VisualizerSession {
  id: string;
  roomImage: string;
  roomType: RoomType;
  surfaces: Surface[];
  layers: VisualizerLayer[];
  history: VisualizerSnapshot[];
  currentIndex: number;
}
