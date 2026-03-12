import { defineEventHandler, readBody, createError } from "h3";

const ROOM_LABELS: Record<string, string> = {
  "living-room": "living room",
  bedroom: "bedroom",
  kitchen: "kitchen",
  bathroom: "bathroom",
  "dining-room": "dining room",
  office: "home office",
  balcony: "balcony",
  exterior: "exterior facade",
  other: "room",
};

interface GenerateBody {
  roomType: string;
  products: Array<{ name: string; category: string; colors: string[] }>;
  style?: string;
  base64Image?: string;
}

function buildPrompt(body: GenerateBody): string {
  const room = ROOM_LABELS[body.roomType] ?? "room";

  const productDescriptions = body.products.map((p) => {
    const colorHint = p.colors.length
      ? ` in ${p.colors.slice(0, 2).join(" and ")}`
      : "";
    return `${p.name}${colorHint} (${p.category})`;
  });

  const materialsList =
    productDescriptions.length > 0
      ? `featuring ${productDescriptions.join(", ")}`
      : "with modern finishes";

  const style = body.style ?? "modern Caribbean";

  if (body.base64Image && productDescriptions.length > 0) {
    return `This is a room interior of a ${room}. I have roughly pasted new materials and products onto specific areas (${materialsList}). Please refine this image to make the new elements look completely photorealistic and naturally blended into the room. Ensure the lighting, shadows, reflections, and perspective of the new elements perfectly match the surrounding environment, keeping the underlying shape intact. Do not change the rest of the room.`;
  }

  return (
    `A beautiful, photorealistic interior design of a ${room} ${materialsList}. ` +
    `${style} style, warm natural lighting, high-end real estate photography, ` +
    `sharp details, 4K quality, no people.`
  );
}

export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig(event);
  const apiKey = config.imagenApiKey;

  if (!apiKey) {
    throw createError({
      statusCode: 500,
      statusMessage: "Imagen API key not configured",
    });
  }

  const body = await readBody<GenerateBody>(event);

  if (!body?.roomType) {
    throw createError({
      statusCode: 400,
      statusMessage: "roomType is required",
    });
  }

  const prompt = buildPrompt(body);

  const parts: Array<{
    inlineData?: { mimeType: string; data: string };
    text?: string;
  }> = [];

  if (body.base64Image) {
    parts.push({
      inlineData: {
        data: body.base64Image,
        mimeType: "image/jpeg",
      },
    });
  }

  parts.push({ text: prompt });

  const response = await $fetch<{
    candidates: Array<{
      content: {
        parts: Array<{
          inlineData?: { mimeType: string; data: string };
          text?: string;
        }>;
      };
    }>;
  }>(
    `https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image-preview:generateContent?key=${apiKey}`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: {
        contents: [{ parts }],
        generationConfig: {
          responseModalities: ["IMAGE", "TEXT"],
        },
      },
    },
  );

  const responseParts = response.candidates?.[0]?.content?.parts ?? [];
  const imagePart = responseParts.find((p) => p.inlineData?.data);
  if (!imagePart?.inlineData) {
    throw createError({
      statusCode: 502,
      statusMessage: "No image returned from Gemini API",
    });
  }

  return {
    imageDataUrl: `data:${imagePart.inlineData.mimeType};base64,${imagePart.inlineData.data}`,
    prompt,
  };
});
