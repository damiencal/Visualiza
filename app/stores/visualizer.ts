import { defineStore } from "pinia";
import type {
  VisualizerSession,
  VisualizerLayer,
  VisualizerSnapshot,
  Surface,
  RoomDimensions,
  BomItem,
  AIDesignAnalysis,
} from "~/types/visualizer";
import type { Product } from "~/types/product";
import type { RoomType } from "~/types/property";

const SURFACE_LABELS: Record<string, string> = {
  floor: "Piso",
  wall: "Pared",
  ceiling: "Techo",
  "counter-top": "Encimera",
  backsplash: "Salpicadero",
};

function computeAreaM2(surfaceType: string, dims: RoomDimensions): number {
  const { width, length, height } = dims;
  switch (surfaceType) {
    case "floor":
    case "ceiling":
      return width * length;
    case "wall":
      // both pairs of walls minus ~15% for doors & windows
      return 2 * (width + length) * height * 0.85;
    case "counter-top":
      return width * 0.6; // 60 cm standard depth
    case "backsplash":
      return width * 0.45;
    default:
      return width * length;
  }
}

function calcQuantity(
  product: Product,
  areaM2: number,
  waste: number,
): { coveragePerUnit: number; quantity: number } {
  const unit = (product.unit ?? "").toLowerCase();
  if (unit === "m²" || unit === "m2") {
    return {
      coveragePerUnit: 1,
      quantity: Math.ceil(areaM2 * (1 + waste)),
    };
  }
  if (unit === "galón" || unit === "galon" || unit === "gallon") {
    const spec: string =
      (product.specs as Record<string, string>)?.Rendimiento ?? "";
    const match = spec.match(/(\d+)\s*m²?\s*\/\s*gal/i);
    const coverage = match ? parseInt(match[1]) : 10;
    return {
      coveragePerUnit: coverage,
      quantity: Math.ceil((areaM2 / coverage) * (1 + waste)),
    };
  }
  // per-unit items (furniture, fixtures, etc.) — 1 per surface
  return { coveragePerUnit: areaM2, quantity: 1 };
}

export const useVisualizerStore = defineStore("visualizer", () => {
  const session = ref<VisualizerSession | null>(null);
  const isProcessing = ref(false);
  const selectedSurfaceId = ref<string | null>(null);
  const showBeforeAfter = ref(false);
  const sliderPosition = ref(50);
  const generatedImage = ref<string | null>(null);
  const isGenerating = ref(false);
  // Stores the current canvas snapshot so AI generation always has the latest rendered state
  const currentCanvasDataUrl = ref<string | null>(null);

  function setCurrentCanvas(dataUrl: string | null) {
    currentCanvasDataUrl.value = dataUrl;
  }

  // BoM state
  const roomDimensions = ref<RoomDimensions>({
    width: 4,
    length: 5,
    height: 2.6,
  });
  const wasteFactor = ref(0.05); // 5 %
  const aiAnalysis = ref<AIDesignAnalysis | null>(null);
  const isAnalyzing = ref(false);

  // Bill of Materials
  const bom = computed<BomItem[]>(() => {
    if (!session.value?.layers.length) return [];
    return session.value.layers.map((layer) => {
      const surface = session.value!.surfaces.find(
        (s) => s.id === layer.surfaceId,
      );
      const surfaceType = surface?.type ?? "floor";
      const areaM2 =
        Math.round(computeAreaM2(surfaceType, roomDimensions.value) * 100) /
        100;
      const { coveragePerUnit, quantity } = calcQuantity(
        layer.product,
        areaM2,
        wasteFactor.value,
      );
      return {
        productId: layer.productId,
        product: layer.product,
        surfaceId: layer.surfaceId,
        surfaceType,
        surfaceLabel: SURFACE_LABELS[surfaceType] ?? surfaceType,
        areaM2,
        coveragePerUnit,
        quantity,
        unitPrice: layer.product.price,
        totalPrice: Math.round(quantity * layer.product.price),
        currency: layer.product.currency,
      } satisfies BomItem;
    });
  });

  const bomTotalDOP = computed(() =>
    bom.value
      .filter((i) => i.currency === "DOP")
      .reduce((s, i) => s + i.totalPrice, 0),
  );
  const bomTotalUSD = computed(() =>
    bom.value
      .filter((i) => i.currency === "USD")
      .reduce((s, i) => s + i.totalPrice, 0),
  );

  const canUndo = computed(() => {
    if (!session.value) return false;
    return session.value.currentIndex > 0;
  });

  const canRedo = computed(() => {
    if (!session.value) return false;
    return session.value.currentIndex < session.value.history.length - 1;
  });

  const currentLayers = computed(() => session.value?.layers ?? []);
  const selectedSurface = computed(
    () =>
      session.value?.surfaces.find((s) => s.id === selectedSurfaceId.value) ??
      null,
  );

  function createSession(
    roomImage: string,
    roomType: RoomType,
  ): VisualizerSession {
    const newSession: VisualizerSession = {
      id: crypto.randomUUID(),
      roomImage,
      roomType,
      surfaces: [],
      layers: [],
      history: [],
      currentIndex: -1,
    };
    session.value = newSession;
    pushSnapshot();
    return newSession;
  }

  function selectSurface(surfaceId: string | null) {
    selectedSurfaceId.value = surfaceId;
    if (session.value) {
      session.value.surfaces = session.value.surfaces.map((s) => ({
        ...s,
        isSelected: s.id === surfaceId,
      }));
    }
  }

  function addSurface(type: Surface["type"]) {
    if (!session.value) return;
    const surface: Surface = {
      id: crypto.randomUUID(),
      type,
      mask: "",
      label: type,
      isSelected: false,
    };
    session.value.surfaces.push(surface);
    selectSurface(surface.id);
  }

  function applyProduct(surfaceId: string, product: Product, opacity = 0.75) {
    if (!session.value) return;
    const existingIndex = session.value.layers.findIndex(
      (l) => l.surfaceId === surfaceId,
    );
    // Furniture uses source-over (overlay the product image); surfaces use multiply (texture blend)
    const isFurniture = product.category === "furniture";
    const isPaint = product.category === "paint";
    const layer: VisualizerLayer = {
      id: crypto.randomUUID(),
      surfaceId,
      productId: product.id,
      product,
      opacity: isFurniture ? 0.92 : isPaint ? 0.55 : opacity,
      blendMode: isFurniture ? "source-over" : isPaint ? "color" : "multiply",
      transform: { scale: 1, rotation: 0, offsetX: 0, offsetY: 0 },
    };
    if (existingIndex >= 0) {
      session.value.layers[existingIndex] = layer;
    } else {
      session.value.layers.push(layer);
    }
    pushSnapshot();
  }

  function updateLayerOpacity(layerId: string, opacity: number) {
    if (!session.value) return;
    const layer = session.value.layers.find((l) => l.id === layerId);
    if (layer) {
      layer.opacity = opacity;
      pushSnapshot();
    }
  }

  function removeLayer(layerId: string) {
    if (!session.value) return;
    session.value.layers = session.value.layers.filter((l) => l.id !== layerId);
    pushSnapshot();
  }

  function pushSnapshot(thumbnail?: string) {
    if (!session.value) return;
    const snapshot: VisualizerSnapshot = {
      timestamp: Date.now(),
      layers: JSON.parse(JSON.stringify(session.value.layers)),
      thumbnail,
    };
    // Remove forward history if we're not at the end
    session.value.history = session.value.history.slice(
      0,
      session.value.currentIndex + 1,
    );
    session.value.history.push(snapshot);
    session.value.currentIndex = session.value.history.length - 1;
  }

  function undo() {
    if (!canUndo.value || !session.value) return;
    session.value.currentIndex--;
    const snapshot = session.value.history[session.value.currentIndex];
    if (snapshot)
      session.value.layers = JSON.parse(JSON.stringify(snapshot.layers));
  }

  function redo() {
    if (!canRedo.value || !session.value) return;
    session.value.currentIndex++;
    const snapshot = session.value.history[session.value.currentIndex];
    if (snapshot)
      session.value.layers = JSON.parse(JSON.stringify(snapshot.layers));
  }

  function reset() {
    if (!session.value) return;
    session.value.layers = [];
    session.value.history = [];
    session.value.currentIndex = -1;
    generatedImage.value = null;
    pushSnapshot();
  }

  async function generateWithAI(style?: string, base64Image?: string) {
    if (!session.value) return;
    isGenerating.value = true;
    try {
      const products = session.value.layers.map((l) => ({
        name: l.product.nameEs || l.product.name,
        category: l.product.category,
        colors: l.product.colors,
      }));
      // Use the explicitly passed base64, otherwise fall back to the stored canvas snapshot
      const imageData =
        base64Image ??
        (currentCanvasDataUrl.value
          ? currentCanvasDataUrl.value.split(",")[1]
          : undefined);
      const result = await $fetch<{ imageDataUrl: string }>(
        "/api/visualizer/generate",
        {
          method: "POST",
          body: {
            roomType: session.value.roomType,
            products,
            style,
            base64Image: imageData,
          },
        },
      );
      generatedImage.value = result.imageDataUrl;
    } finally {
      isGenerating.value = false;
    }
  }

  async function analyzeWithAI() {
    if (!generatedImage.value || !session.value) return;
    isAnalyzing.value = true;
    aiAnalysis.value = null;
    try {
      const products = session.value.layers.map((l) => {
        const surface = session.value!.surfaces.find(
          (s) => s.id === l.surfaceId,
        );
        return {
          name: l.product.nameEs || l.product.name,
          category: l.product.category,
          surfaceType: surface?.type ?? "floor",
        };
      });
      const result = await $fetch<AIDesignAnalysis>("/api/visualizer/analyze", {
        method: "POST",
        body: {
          imageDataUrl: generatedImage.value,
          products,
          roomType: session.value.roomType,
          totalEstimatedCost: bomTotalDOP.value,
        },
      });
      aiAnalysis.value = result;
    } finally {
      isAnalyzing.value = false;
    }
  }

  function clearGeneratedImage() {
    generatedImage.value = null;
  }

  function toggleBeforeAfter() {
    showBeforeAfter.value = !showBeforeAfter.value;
  }

  function setSliderPosition(pos: number) {
    sliderPosition.value = Math.min(100, Math.max(0, pos));
  }

  return {
    session,
    isProcessing,
    isGenerating,
    generatedImage,
    selectedSurfaceId,
    showBeforeAfter,
    sliderPosition,
    canUndo,
    canRedo,
    currentLayers,
    selectedSurface,
    // BoM
    roomDimensions,
    wasteFactor,
    bom,
    bomTotalDOP,
    bomTotalUSD,
    aiAnalysis,
    isAnalyzing,
    currentCanvasDataUrl,
    setCurrentCanvas,
    createSession,
    selectSurface,
    addSurface,
    applyProduct,
    updateLayerOpacity,
    removeLayer,
    pushSnapshot,
    undo,
    redo,
    reset,
    toggleBeforeAfter,
    setSliderPosition,
    generateWithAI,
    clearGeneratedImage,
    analyzeWithAI,
  };
});
