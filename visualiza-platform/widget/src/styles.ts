export const WIDGET_STYLES = `
  :host {
    display: block;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    --vz-primary: #7c3aed;
    --vz-primary-hover: #6d28d9;
    --vz-bg: #ffffff;
    --vz-border: #e5e7eb;
    --vz-text: #111827;
    --vz-muted: #6b7280;
    --vz-radius: 12px;
  }

  * { box-sizing: border-box; margin: 0; padding: 0; }

  .vz-widget {
    background: var(--vz-bg);
    border: 1px solid var(--vz-border);
    border-radius: var(--vz-radius);
    overflow: hidden;
    max-width: 480px;
    width: 100%;
  }

  .vz-step { padding: 24px; }

  .vz-header { margin-bottom: 20px; }
  .vz-header h2 { font-size: 18px; font-weight: 700; color: var(--vz-text); }
  .vz-header p { font-size: 14px; color: var(--vz-muted); margin-top: 4px; }

  .vz-back {
    background: none; border: none; cursor: pointer;
    font-size: 13px; color: var(--vz-muted); margin-bottom: 8px;
    display: inline-flex; align-items: center; gap: 4px;
  }
  .vz-back:hover { color: var(--vz-text); }

  /* Dropzone */
  .vz-dropzone {
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    border: 2px dashed var(--vz-border); border-radius: 8px;
    padding: 40px 20px; cursor: pointer; gap: 12px;
    color: var(--vz-muted); text-align: center; font-size: 14px;
    margin-bottom: 16px; transition: border-color 0.2s;
    min-height: 180px; overflow: hidden;
  }
  .vz-dropzone:hover { border-color: var(--vz-primary); }
  .vz-preview-img { width: 100%; height: 200px; object-fit: cover; border-radius: 6px; }

  /* Buttons */
  .vz-btn {
    display: inline-flex; align-items: center; justify-content: center;
    padding: 10px 20px; border-radius: 8px; font-size: 14px; font-weight: 600;
    cursor: pointer; border: none; transition: all 0.2s; width: 100%;
  }
  .vz-btn:disabled { opacity: 0.5; cursor: not-allowed; }
  .vz-btn-primary { background: var(--vz-primary); color: #fff; }
  .vz-btn-primary:hover:not(:disabled) { background: var(--vz-primary-hover); }
  .vz-btn-outline { background: transparent; border: 1px solid var(--vz-border); color: var(--vz-text); }
  .vz-btn-outline:hover { background: #f3f4f6; }
  .vz-mt { margin-top: 16px; }

  /* Surface grid */
  .vz-surface-grid {
    display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; margin-bottom: 20px;
  }
  .vz-surface-btn {
    display: flex; flex-direction: column; align-items: center; gap: 8px;
    padding: 16px 12px; border: 2px solid var(--vz-border); border-radius: 8px;
    background: transparent; cursor: pointer; font-size: 13px; font-weight: 500;
    color: var(--vz-text); transition: all 0.2s;
  }
  .vz-surface-btn:hover { border-color: var(--vz-primary); background: #f5f3ff; }
  .vz-surface-btn--active { border-color: var(--vz-primary); background: #f5f3ff; color: var(--vz-primary); }
  .vz-surface-icon { font-size: 24px; }

  /* Products */
  .vz-products { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; margin-bottom: 16px; }
  .vz-product-card {
    border: 2px solid var(--vz-border); border-radius: 8px; overflow: hidden;
    cursor: pointer; transition: all 0.2s;
  }
  .vz-product-card:hover { border-color: var(--vz-primary); }
  .vz-product-card--selected { border-color: var(--vz-primary); background: #f5f3ff; }
  .vz-product-img {
    width: 100%; height: 72px; background: #f3f4f6;
    background-size: cover; background-position: center;
  }
  .vz-product-info { padding: 8px; }
  .vz-product-name { font-size: 12px; font-weight: 600; line-height: 1.3; color: var(--vz-text); }
  .vz-product-price { font-size: 11px; color: var(--vz-muted); margin-top: 2px; }
  .vz-area-input { padding: 0 8px 8px; }
  .vz-area-input label { font-size: 11px; color: var(--vz-muted); display: block; margin-bottom: 2px; }
  .vz-area {
    width: 100%; padding: 4px 8px; border: 1px solid var(--vz-border);
    border-radius: 4px; font-size: 12px; background: #fff;
  }

  /* BoM */
  .vz-bom-items { border: 1px solid var(--vz-border); border-radius: 8px; overflow: hidden; margin-bottom: 16px; }
  .vz-bom-row {
    display: flex; align-items: center; padding: 10px 14px;
    border-bottom: 1px solid var(--vz-border); font-size: 13px;
  }
  .vz-bom-row:last-child { border-bottom: none; }
  .vz-bom-name { flex: 1; font-weight: 500; }
  .vz-bom-qty { color: var(--vz-muted); margin-right: 16px; font-size: 12px; }
  .vz-bom-price { font-weight: 600; font-family: monospace; }

  .vz-bom-totals { border-top: 2px solid var(--vz-border); padding-top: 12px; }
  .vz-bom-total-row {
    display: flex; justify-content: space-between; padding: 4px 0; font-size: 13px; color: var(--vz-muted);
  }
  .vz-bom-grand-total { font-size: 16px; font-weight: 700; color: var(--vz-text); padding-top: 8px; }

  /* Loader */
  .vz-loader { display: flex; flex-direction: column; align-items: center; gap: 12px; padding: 40px 24px; color: var(--vz-muted); font-size: 14px; }
  .vz-spinner {
    width: 32px; height: 32px; border: 3px solid var(--vz-border);
    border-top-color: var(--vz-primary); border-radius: 50%;
    animation: vz-spin 0.7s linear infinite;
  }
  @keyframes vz-spin { to { transform: rotate(360deg); } }

  /* Error / empty */
  .vz-error { color: #dc2626; font-size: 13px; padding: 16px; text-align: center; }
  .vz-empty { color: var(--vz-muted); font-size: 13px; padding: 16px; text-align: center; }
`;
