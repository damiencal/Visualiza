import { createApi, type Product, type BoMRequest } from "./api";
import { WIDGET_STYLES } from "./styles";
import { t, type Lang } from "./i18n";

type Step = "upload" | "surfaces" | "bom";

export class VisualisaWidget extends HTMLElement {
  private shadow: ShadowRoot;
  private apiKey = "";
  private lang: Lang = "es";
  private step: Step = "upload";
  private api!: ReturnType<typeof createApi>;

  // State
  private sessionId: string | null = null;
  private uploadedImageUrl: string | null = null;
  private selectedSurface: string | null = null;
  private surfaceProducts: Product[] = [];
  private bomSelections: Map<string, { product: Product; areaMx: number }> =
    new Map();
  private loading = false;

  static get observedAttributes() {
    return ["api-key", "lang"];
  }

  constructor() {
    super();
    this.shadow = this.attachShadow({ mode: "open" });
  }

  attributeChangedCallback(
    name: string,
    _old: string | null,
    value: string | null,
  ) {
    if (name === "api-key" && value) {
      this.apiKey = value;
      this.api = createApi(this.apiKey);
      this.validateAndInit();
    }
    if (name === "lang" && value) {
      this.lang = (value as Lang) || "es";
    }
  }

  connectedCallback() {
    this.render();
  }

  private async validateAndInit() {
    try {
      await this.api.validate(window.location.origin);
      this.render();
    } catch {
      this.renderError("Invalid API key or unauthorized domain.");
    }
  }

  // ── Rendering ──────────────────────────────────────────────────────────

  private render() {
    this.shadow.innerHTML = `
      <style>${WIDGET_STYLES}</style>
      <div class="vz-widget" id="vz-root">
        ${this.renderStep()}
      </div>
    `;
    this.attachEventListeners();
  }

  private renderStep(): string {
    if (this.loading) return this.renderLoader();
    if (this.step === "upload") return this.renderUpload();
    if (this.step === "surfaces") return this.renderSurfaces();
    if (this.step === "bom") return this.renderBoM();
    return "";
  }

  private renderLoader(): string {
    return `<div class="vz-loader"><div class="vz-spinner"></div><p>${t(this.lang, "loading")}</p></div>`;
  }

  private renderUpload(): string {
    return `
      <div class="vz-step vz-upload">
        <div class="vz-header">
          <h2>${t(this.lang, "uploadTitle")}</h2>
          <p>${t(this.lang, "uploadSubtitle")}</p>
        </div>
        <label class="vz-dropzone" id="vz-dropzone">
          ${
            this.uploadedImageUrl
              ? `<img src="${this.uploadedImageUrl}" alt="room" class="vz-preview-img" />`
              : `
              <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4"/>
                <polyline points="17 8 12 3 7 8"/>
                <line x1="12" y1="3" x2="12" y2="15"/>
              </svg>
              <p>${t(this.lang, "dropzone")}</p>
            `
          }
          <input type="file" id="vz-file" accept="image/*" hidden />
        </label>
        <button class="vz-btn vz-btn-primary" id="vz-next-btn" ${!this.uploadedImageUrl ? "disabled" : ""}>
          ${t(this.lang, "next")} →
        </button>
      </div>
    `;
  }

  private renderSurfaces(): string {
    const surfaces = [
      { id: "floor", icon: "▭", label: t(this.lang, "floor") },
      { id: "wall", icon: "◫", label: t(this.lang, "wall") },
      { id: "ceiling", icon: "⬚", label: t(this.lang, "ceiling") },
      { id: "countertop", icon: "⬛", label: t(this.lang, "countertop") },
    ];
    return `
      <div class="vz-step vz-surfaces">
        <div class="vz-header">
          <button class="vz-back" id="vz-back">← ${t(this.lang, "back")}</button>
          <h2>${t(this.lang, "selectSurface")}</h2>
        </div>
        <div class="vz-surface-grid">
          ${surfaces
            .map(
              (s) => `
            <button
              class="vz-surface-btn ${this.selectedSurface === s.id ? "vz-surface-btn--active" : ""}"
              data-surface="${s.id}"
            >
              <span class="vz-surface-icon">${s.icon}</span>
              <span>${s.label}</span>
            </button>
          `,
            )
            .join("")}
        </div>

        ${
          this.selectedSurface
            ? `
          <div class="vz-products" id="vz-products">
            ${
              this.surfaceProducts.length === 0
                ? `<p class="vz-empty">${t(this.lang, "loading")}</p>`
                : this.surfaceProducts
                    .map(
                      (p) => `
                <div class="vz-product-card ${this.bomSelections.has(p.id) ? "vz-product-card--selected" : ""}" data-product-id="${p.id}">
                  <div class="vz-product-img" ${p.texture_url ? `style="background-image:url(${p.texture_url})"` : ""}></div>
                  <div class="vz-product-info">
                    <p class="vz-product-name">${p.name}</p>
                    <p class="vz-product-price">${formatDOP(p.price_dop)}/m²</p>
                  </div>
                  ${
                    this.bomSelections.has(p.id)
                      ? `<div class="vz-area-input">
                        <label>${t(this.lang, "areaLabel")}</label>
                        <input type="number" class="vz-area" data-product-id="${p.id}" min="0.1" step="0.1" value="${this.bomSelections.get(p.id)?.areaMx ?? ""}" />
                      </div>`
                      : ""
                  }
                </div>
              `,
                    )
                    .join("")
            }
          </div>
          <button class="vz-btn vz-btn-primary vz-mt" id="vz-calc-btn" ${this.bomSelections.size === 0 ? "disabled" : ""}>
            ${t(this.lang, "calculate")} →
          </button>
        `
            : ""
        }
      </div>
    `;
  }

  private renderBoM(): string {
    // Collect selections as array for display
    const items = [...this.bomSelections.entries()];
    return `
      <div class="vz-step vz-bom">
        <div class="vz-header">
          <button class="vz-back" id="vz-back">← ${t(this.lang, "back")}</button>
          <h2>${t(this.lang, "bomTitle")}</h2>
        </div>
        <div id="vz-bom-content">
          <div class="vz-loader"><div class="vz-spinner"></div></div>
        </div>
      </div>
    `;
  }

  private renderBoMContent(bom: {
    line_items: BomLineItem[];
    total_before_tax: number;
    tax_amount: number;
    total_with_tax: number;
    share_url?: string;
  }) {
    const content = this.shadow.getElementById("vz-bom-content");
    if (!content) return;
    content.innerHTML = `
      <div class="vz-bom-items">
        ${bom.line_items
          .map(
            (item) => `
          <div class="vz-bom-row">
            <span class="vz-bom-name">${item.product_name}</span>
            <span class="vz-bom-qty">${item.quantity_needed} ${item.unit}</span>
            <span class="vz-bom-price">${formatDOP(item.subtotal_dop)}</span>
          </div>
        `,
          )
          .join("")}
      </div>
      <div class="vz-bom-totals">
        <div class="vz-bom-total-row">
          <span>${t(this.lang, "subtotal")}</span>
          <span>${formatDOP(bom.total_before_tax)}</span>
        </div>
        <div class="vz-bom-total-row">
          <span>ITBIS (18%)</span>
          <span>${formatDOP(bom.tax_amount)}</span>
        </div>
        <div class="vz-bom-total-row vz-bom-grand-total">
          <span>${t(this.lang, "total")}</span>
          <span>${formatDOP(bom.total_with_tax)}</span>
        </div>
      </div>
      ${
        bom.share_url
          ? `
        <a href="${bom.share_url}" target="_blank" class="vz-btn vz-btn-outline vz-mt">
          ${t(this.lang, "share")} ↗
        </a>
      `
          : ""
      }
      <button class="vz-btn vz-btn-primary vz-mt" id="vz-restart">
        ${t(this.lang, "restart")}
      </button>
    `;
    this.shadow
      .getElementById("vz-restart")
      ?.addEventListener("click", () => this.restart());
  }

  // ── Event listeners ────────────────────────────────────────────────────

  private attachEventListeners() {
    const root = this.shadow.getElementById("vz-root");
    if (!root) return;

    // File upload
    const fileInput = this.shadow.getElementById(
      "vz-file",
    ) as HTMLInputElement | null;
    const dropzone = this.shadow.getElementById("vz-dropzone");
    fileInput?.addEventListener("change", (e) => {
      const file = (e.target as HTMLInputElement).files?.[0];
      if (file) this.handleFileSelect(file);
    });
    dropzone?.addEventListener("dragover", (e) => {
      e.preventDefault();
    });
    dropzone?.addEventListener("drop", (e) => {
      e.preventDefault();
      const file = (e as DragEvent).dataTransfer?.files[0];
      if (file) this.handleFileSelect(file);
    });
    dropzone?.addEventListener("click", () => fileInput?.click());

    // Next button
    this.shadow
      .getElementById("vz-next-btn")
      ?.addEventListener("click", () => this.goToSurfaces());

    // Back button
    this.shadow
      .getElementById("vz-back")
      ?.addEventListener("click", () => this.goBack());

    // Surface buttons
    this.shadow.querySelectorAll("[data-surface]").forEach((btn) => {
      btn.addEventListener("click", () => {
        this.selectedSurface = (btn as HTMLElement).dataset.surface ?? null;
        this.loadProducts();
      });
    });

    // Product card click (toggle select)
    this.shadow.querySelectorAll(".vz-product-card").forEach((card) => {
      card.addEventListener("click", (e) => {
        const el = e.currentTarget as HTMLElement;
        const id = el.dataset.productId!;
        if (this.bomSelections.has(id)) {
          this.bomSelections.delete(id);
        } else {
          const product = this.surfaceProducts.find((p) => p.id === id)!;
          this.bomSelections.set(id, { product, areaMx: 10 });
        }
        this.render();
      });
    });

    // Area inputs
    this.shadow
      .querySelectorAll<HTMLInputElement>(".vz-area")
      .forEach((input) => {
        input.addEventListener("change", () => {
          const id = input.dataset.productId!;
          const existing = this.bomSelections.get(id);
          if (existing) existing.areaMx = parseFloat(input.value) || 1;
        });
        input.addEventListener("click", (e) => e.stopPropagation());
      });

    // Calculate BoM
    this.shadow
      .getElementById("vz-calc-btn")
      ?.addEventListener("click", () => this.calculateBoM());
  }

  // ── Business logic ─────────────────────────────────────────────────────

  private handleFileSelect(file: File) {
    const reader = new FileReader();
    reader.onload = (e) => {
      this.uploadedImageUrl = e.target?.result as string;
      this.render();
    };
    reader.readAsDataURL(file);
  }

  private goToSurfaces() {
    this.step = "surfaces";
    this.render();
  }

  private goBack() {
    if (this.step === "surfaces") {
      this.step = "upload";
    } else if (this.step === "bom") {
      this.step = "surfaces";
    }
    this.render();
  }

  private async loadProducts() {
    if (!this.selectedSurface) return;
    this.loading = true;
    this.render();
    try {
      this.surfaceProducts = await this.api.getProducts(this.selectedSurface);
    } finally {
      this.loading = false;
      this.render();
    }
  }

  private async calculateBoM() {
    this.step = "bom";
    this.render();

    const items = [...this.bomSelections.entries()].map(([productId, sel]) => ({
      product_id: productId,
      area_m2: sel.areaMx,
    }));

    try {
      const bom = await this.api.generateBoM({ items });
      this.renderBoMContent(bom);
    } catch (err) {
      const content = this.shadow.getElementById("vz-bom-content");
      if (content)
        content.innerHTML = `<p class="vz-error">Failed to generate BoM. Please try again.</p>`;
    }
  }

  private restart() {
    this.step = "upload";
    this.uploadedImageUrl = null;
    this.selectedSurface = null;
    this.surfaceProducts = [];
    this.bomSelections.clear();
    this.render();
  }

  private renderError(message: string) {
    this.shadow.innerHTML = `<style>${WIDGET_STYLES}</style><div class="vz-widget"><p class="vz-error">${message}</p></div>`;
  }
}

// ── Helpers ──────────────────────────────────────────────────────────────

function formatDOP(v: number): string {
  return new Intl.NumberFormat("es-DO", {
    style: "currency",
    currency: "DOP",
    maximumFractionDigits: 0,
  }).format(v);
}

interface BomLineItem {
  product_name: string;
  quantity_needed: number;
  unit: string;
  subtotal_dop: number;
}
