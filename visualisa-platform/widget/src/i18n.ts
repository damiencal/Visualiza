export type Lang = "es" | "en";

const translations: Record<Lang, Record<string, string>> = {
  es: {
    uploadTitle: "Visualisa tu renovación",
    uploadSubtitle: "Sube una foto de tu habitación para comenzar",
    dropzone: "Arrastra tu imagen aquí o haz clic para seleccionar",
    next: "Continuar",
    back: "Atrás",
    selectSurface: "Selecciona la superficie a renovar",
    floor: "Piso",
    wall: "Pared",
    ceiling: "Techo",
    countertop: "Encimera",
    areaLabel: "Área (m²)",
    calculate: "Calcular presupuesto",
    bomTitle: "Presupuesto de materiales",
    subtotal: "Subtotal",
    total: "Total",
    share: "Compartir presupuesto",
    restart: "Nuevo presupuesto",
    loading: "Cargando…",
  },
  en: {
    uploadTitle: "Visualize your renovation",
    uploadSubtitle: "Upload a photo of your room to get started",
    dropzone: "Drag your image here or click to select",
    next: "Continue",
    back: "Back",
    selectSurface: "Select the surface to renovate",
    floor: "Floor",
    wall: "Wall",
    ceiling: "Ceiling",
    countertop: "Countertop",
    areaLabel: "Area (m²)",
    calculate: "Calculate estimate",
    bomTitle: "Bill of Materials",
    subtotal: "Subtotal",
    total: "Total",
    share: "Share estimate",
    restart: "New estimate",
    loading: "Loading…",
  },
};

export function t(lang: Lang, key: string): string {
  return translations[lang]?.[key] ?? translations.es[key] ?? key;
}
