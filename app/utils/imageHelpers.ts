/**
 * Resize an image file to a maximum dimension while maintaining aspect ratio.
 */
export async function resizeImage(
  file: File,
  maxWidth = 1920,
  maxHeight = 1080,
  quality = 0.85,
): Promise<Blob> {
  return new Promise((resolve, reject) => {
    const img = new Image();
    const url = URL.createObjectURL(file);
    img.onload = () => {
      URL.revokeObjectURL(url);
      let { width, height } = img;
      if (width > maxWidth || height > maxHeight) {
        const ratio = Math.min(maxWidth / width, maxHeight / height);
        width = Math.round(width * ratio);
        height = Math.round(height * ratio);
      }
      const canvas = document.createElement("canvas");
      canvas.width = width;
      canvas.height = height;
      const ctx = canvas.getContext("2d");
      if (!ctx) return reject(new Error("No canvas context"));
      ctx.drawImage(img, 0, 0, width, height);
      canvas.toBlob(
        (blob) => {
          if (blob) resolve(blob);
          else reject(new Error("Canvas toBlob failed"));
        },
        "image/webp",
        quality,
      );
    };
    img.onerror = reject;
    img.src = url;
  });
}

/**
 * Convert a File or Blob to a base64 data URL.
 */
export function fileToDataURL(file: File | Blob): Promise<string> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result as string);
    reader.onerror = reject;
    reader.readAsDataURL(file);
  });
}

/**
 * Validate an image file (type and max size).
 * Returns an error message string, or null if valid.
 */
export function validateImageFile(file: File, maxMB = 20): string | null {
  const allowed = ["image/jpeg", "image/png", "image/webp", "image/heic"];
  if (!allowed.includes(file.type)) {
    return "Formato no permitido. Usa JPG, PNG o WebP.";
  }
  if (file.size > maxMB * 1024 * 1024) {
    return `El archivo es muy grande. Máximo ${maxMB}MB.`;
  }
  return null;
}
