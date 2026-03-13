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
      ? productDescriptions.join(", ")
      : "modern finishes";

  const style = body.style ?? "modern Caribbean";

  const furnitureProducts = body.products.filter(
    (p) => p.category === "furniture",
  );
  const surfaceProducts = body.products.filter(
    (p) => p.category !== "furniture",
  );

  if (body.base64Image && productDescriptions.length > 0) {
    const parts: string[] = [];

    if (furnitureProducts.length > 0) {
      const furnitureList = furnitureProducts
        .map((p) => {
          const colorHint = p.colors.length
            ? ` in ${p.colors.slice(0, 2).join(" and ")}`
            : "";
          return `${p.name}${colorHint}`;
        })
        .join(", ");
      parts.push(
        `Replace the existing furniture in this ${room} with the following new pieces: ${furnitureList}. ` +
          `The new furniture has been roughly placed in the scene. Integrate it photorealistically — ` +
          `match the room's lighting direction, cast natural shadows, adjust perspective and scale so the ` +
          `furniture sits convincingly on the floor. Remove the original furniture that is being replaced.`,
      );
    }

    if (surfaceProducts.length > 0) {
      const surfaceList = surfaceProducts
        .map((p) => {
          const colorHint = p.colors.length
            ? ` in ${p.colors.slice(0, 2).join(" and ")}`
            : "";
          return `${p.name}${colorHint} (${p.category})`;
        })
        .join(", ");
      parts.push(
        `Also apply these surface materials: ${surfaceList}. ` +
          `Make them look completely photorealistic with correct lighting, reflections, and texture detail.`,
      );
    }

    parts.push(
      `Keep all other room elements — architecture, remaining furniture, windows, ceiling, ` +
        `and background — completely unchanged. Output a single photorealistic interior photograph.`,
    );

    return parts.join(" ");
  }

  return (
    `A beautiful, photorealistic interior design of a ${room} featuring ${materialsList}. ` +
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
