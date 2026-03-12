export interface Product {
  id: string;
  name: string;
  price_dop: number;
  surface_type: string;
  texture_url?: string;
  brand_name?: string;
  unit: string;
}

export interface BoMRequest {
  items: Array<{ product_id: string; area_m2: number }>;
}

export interface BoMResponse {
  id: string;
  line_items: Array<{
    product_name: string;
    quantity_needed: number;
    unit: string;
    subtotal_dop: number;
  }>;
  total_before_tax: number;
  tax_amount: number;
  total_with_tax: number;
  share_url?: string;
}

const BASE_URL =
  (import.meta as Record<string, unknown>).env?.VITE_API_URL ??
  "https://api.visualisa.web.do";

export function createApi(apiKey: string) {
  const headers = {
    "Content-Type": "application/json",
    "X-API-Key": apiKey,
  };

  async function request<T>(
    method: string,
    path: string,
    body?: unknown,
  ): Promise<T> {
    const res = await fetch(`${BASE_URL}${path}`, {
      method,
      headers,
      body: body ? JSON.stringify(body) : undefined,
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: res.statusText }));
      throw new Error(err.detail || `HTTP ${res.status}`);
    }
    return res.json() as Promise<T>;
  }

  return {
    validate: (origin: string) =>
      request<{ valid: boolean }>("POST", "/public/validate", { origin }),

    getProducts: (surfaceType: string) =>
      request<Product[]>("GET", `/public/catalog?surface_type=${surfaceType}`),

    generateBoM: (payload: BoMRequest) =>
      request<BoMResponse>("POST", "/public/bom/generate", payload),
  };
}
