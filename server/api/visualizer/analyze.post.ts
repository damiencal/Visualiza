import { defineEventHandler, readBody, createError } from "h3";

const ROOM_LABELS: Record<string, string> = {
  "living-room": "sala de estar",
  bedroom: "dormitorio",
  kitchen: "cocina",
  bathroom: "baño",
  "dining-room": "comedor",
  office: "oficina en casa",
  balcony: "balcón",
  exterior: "fachada exterior",
  other: "habitación",
};

interface AnalyzeBody {
  imageDataUrl: string;
  products: Array<{ name: string; category: string; surfaceType: string }>;
  roomType: string;
  totalEstimatedCost?: number;
}

export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig(event);
  const apiKey = config.imagenApiKey;

  if (!apiKey) {
    throw createError({
      statusCode: 500,
      statusMessage: "API key not configured",
    });
  }

  const body = await readBody<AnalyzeBody>(event);

  if (!body?.imageDataUrl || !body.roomType) {
    throw createError({
      statusCode: 400,
      statusMessage: "imageDataUrl and roomType are required",
    });
  }

  // Extract base64 payload from data URL
  const commaIdx = body.imageDataUrl.indexOf(",");
  if (commaIdx === -1) {
    throw createError({ statusCode: 400, statusMessage: "Invalid imageDataUrl" });
  }
  const mimeType = body.imageDataUrl
    .slice(0, commaIdx)
    .replace("data:", "")
    .replace(";base64", "");
  const b64data = body.imageDataUrl.slice(commaIdx + 1);

  const room = ROOM_LABELS[body.roomType] ?? "habitación";
  const productList = body.products
    .map((p) => `${p.name} (${p.category}, ${p.surfaceType})`)
    .join("; ");

  const prompt = `Eres un experto en diseño de interiores y arquitectura. Analiza cuidadosamente esta imagen de un ${room} que tiene los siguientes materiales aplicados: ${productList || "materiales no especificados"}.

Evalúa el diseño y responde EXCLUSIVAMENTE con un objeto JSON válido con esta estructura exacta (sin texto adicional, sin markdown, sin bloques de código):
{
  "score": <número entero del 0 al 10>,
  "summary": "<resumen breve en español del diseño general>",
  "suggestions": ["<sugerencia 1>", "<sugerencia 2>", "<sugerencia 3>"],
  "colorHarmony": "<evaluación de la armonía cromática>",
  "styleMatch": "<coherencia estilística de los materiales>",
  "estimatedCoverage": "<comentario sobre la cobertura visual y distribución de materiales>"
}`;

  const response = await $fetch<{
    candidates: Array<{
      content: {
        parts: Array<{ text?: string }>;
      };
    }>;
  }>(
    `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${apiKey}`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: {
        contents: [
          {
            parts: [
              { text: prompt },
              {
                inlineData: {
                  mimeType,
                  data: b64data,
                },
              },
            ],
          },
        ],
        generationConfig: {
          temperature: 0.4,
          maxOutputTokens: 512,
        },
      },
    },
  );

  const rawText =
    response.candidates?.[0]?.content?.parts
      ?.map((p) => p.text)
      .filter(Boolean)
      .join("") ?? "";

  // Strip any accidental markdown fences
  const jsonText = rawText.replace(/```(?:json)?/gi, "").trim();

  try {
    const parsed = JSON.parse(jsonText);
    return {
      score: Math.min(10, Math.max(0, Number(parsed.score) || 0)),
      summary: String(parsed.summary ?? ""),
      suggestions: Array.isArray(parsed.suggestions)
        ? parsed.suggestions.map(String)
        : [],
      colorHarmony: String(parsed.colorHarmony ?? ""),
      styleMatch: String(parsed.styleMatch ?? ""),
      estimatedCoverage: String(parsed.estimatedCoverage ?? ""),
    };
  } catch {
    throw createError({
      statusCode: 502,
      statusMessage: "Failed to parse AI analysis response",
    });
  }
});
