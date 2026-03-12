/**
 * Visualisa Widget — entry point.
 *
 * Usage (end-user HTML):
 *   <script src="https://cdn.visualisa.web.do/widget.js"></script>
 *   <visualisa-widget api-key="vz_live_..." lang="es"></visualisa-widget>
 */

import { VisualisaWidget } from "./Widget";

// Register the custom element if not already registered
if (!customElements.get("visualisa-widget")) {
  customElements.define("visualisa-widget", VisualisaWidget);
}

// Also auto-init any existing DOM elements with data-visualisa-key attribute
// (alternative mounting pattern: <div data-visualisa-key="vz_live_...">)
document.addEventListener("DOMContentLoaded", () => {
  document
    .querySelectorAll<HTMLElement>("[data-visualisa-key]")
    .forEach((el) => {
      const apiKey = el.dataset.visualisaKey;
      if (apiKey && !el.shadowRoot) {
        const widget = document.createElement(
          "visualisa-widget",
        ) as VisualisaWidget;
        widget.setAttribute("api-key", apiKey);
        const lang = el.dataset.lang ?? "es";
        widget.setAttribute("lang", lang);
        el.appendChild(widget);
      }
    });
});
