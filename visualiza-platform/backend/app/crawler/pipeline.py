"""
Data normalization pipeline: clean, categorize, deduplicate crawled products
"""
import hashlib
import re
from typing import Any

from slugify import slugify

from .base import CrawledProduct

CATEGORY_KEYWORDS: dict[str, list[str]] = {
    "flooring": ["piso", "floor", "vinyl", "lamina", "porcelanato", "ceramica", "ceramic"],
    "paint": ["pintura", "paint", "barniz", "esmalte", "primer", "latex"],
    "tile": ["azulejo", "tile", "ceramica", "porcelain", "mosaico"],
    "furniture": ["mueble", "sofa", "mesa", "silla", "cama", "estante", "armario", "gabinete"],
    "lighting": ["lampara", "luz", "iluminacion", "foco", "chandelier", "led", "bombilla"],
    "fixtures": ["grifo", "ducha", "inodoro", "lavamanos", "faucet", "sanitario"],
    "textiles": ["cortina", "alfombra", "cojin", "sabana", "toalla", "rug", "tapete"],
    "appliances": ["refrigerador", "estufa", "microondas", "lavadora", "secadora"],
    "countertops": ["encimera", "countertop", "mesada", "granito", "marmol", "cuarzo"],
    "wallpaper": ["papel tapiz", "wallpaper", "papel mural"],
}

SURFACE_MAP: dict[str, list[str]] = {
    "flooring": ["floor"],
    "paint": ["wall", "ceiling"],
    "tile": ["floor", "wall"],
    "furniture": [],
    "lighting": [],
    "fixtures": [],
    "textiles": ["floor"],
    "countertops": ["countertop"],
    "wallpaper": ["wall"],
}


class ProductPipeline:
    """Normalize, clean, deduplicate, and categorize crawled products."""

    def process(self, product: CrawledProduct, brand_name: str) -> dict[str, Any]:
        """Normalize a crawled product into a dict ready for DB insertion."""
        cleaned_name = self._clean_text(product.name)
        category = self._infer_category(cleaned_name, product.category_hint)
        surfaces = SURFACE_MAP.get(category, [])

        return {
            "source_url": product.source_url,
            "source_sku": product.source_sku,
            "normalized_name": cleaned_name,
            "normalized_price": product.price,
            "normalized_currency": product.currency or "DOP",
            "normalized_category": category,
            "normalized_images": product.images[:10],
            "raw_data": {
                "name": product.name,
                "name_es": product.name_es,
                "description": product.description,
                "description_es": product.description_es,
                "price": product.price,
                "original_price": product.original_price,
                "currency": product.currency,
                "price_unit": product.price_unit,
                "specifications": product.specifications,
                "colors": product.colors,
                "materials": product.materials,
                "dimensions": product.dimensions,
                "in_stock": product.in_stock,
                "tags": product.tags,
                "images": product.images,
            },
            "slug": slugify(f"{brand_name}-{cleaned_name}"),
            "surface_types": surfaces,
            "dedup_hash": self._dedup_hash(
                brand_name, product.source_sku or cleaned_name
            ),
        }

    def _clean_text(self, text: str) -> str:
        if not text:
            return ""
        text = re.sub(r"\s+", " ", text).strip()
        text = re.sub(r"[^\w\s\-.,/()áéíóúñüÁÉÍÓÚÑÜ]", "", text)
        return text

    def _infer_category(self, name: str, hint: str | None) -> str:
        search_text = f"{name} {hint or ''}".lower()
        for category, keywords in CATEGORY_KEYWORDS.items():
            if any(kw in search_text for kw in keywords):
                return category
        return "other"

    def _dedup_hash(self, brand: str, identifier: str) -> str:
        return hashlib.sha256(f"{brand}:{identifier}".encode()).hexdigest()[:32]
