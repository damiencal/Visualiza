/**
 * Visualiza Widget — entry point.
 *
 * Usage (end-user HTML):
 *   <script src="https://cdn.visualiza.do/widget.js"></script>
 *   <visualiza-widget api-key="vz_live_..." lang="es"></visualiza-widget>
 */

import { VisualizaWidget } from "./Widget";

// Register the custom element if not already registered
if (!customElements.get("visualiza-widget")) {
  customElements.define("visualiza-widget", VisualizaWidget);
}

// Also auto-init any existing DOM elements with data-visualiza-key attribute
// (alternative mounting pattern: <div data-visualiza-key="vz_live_...">)
document.addEventListener("DOMContentLoaded", () => {
  document
    .querySelectorAll<HTMLElement>("[data-visualiza-key]")
    .forEach((el) => {
      const apiKey = el.dataset.visualizaKey;
      if (apiKey && !el.shadowRoot) {
        const widget = document.createElement(
          "visualiza-widget",
        ) as VisualizaWidget;
        widget.setAttribute("api-key", apiKey);
        const lang = el.dataset.lang ?? "es";
        widget.setAttribute("lang", lang);
        el.appendChild(widget);
      }
    });
});
