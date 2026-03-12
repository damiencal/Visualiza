"""
Ochoa.com.do Crawler
"""
from typing import Any

from .base import BaseCrawler, CrawledProduct
from .utils import absolute_url, parse_dop_price

SURFACE_MAP: dict[str, str] = {
    "pisos": "floor",
    "revestimientos": "wall",
    "ceramica": "floor",
    "porcelanato": "floor",
    "pinturas": "wall",
    "pintura": "wall",
}


class OchoaCrawler(BaseCrawler):
    name = "ochoa"
    base_url = "https://ochoa.com.do"
    fetcher_type = "dynamic"

    CATEGORY_PATHS = [
        "/pisos-y-revestimientos",
        "/pinturas",
        "/banos",
        "/iluminacion",
        "/herramientas",
        "/plomeria",
        "/electricidad",
        "/ceramicas",
        "/porcelanatos",
    ]

    def get_category_urls(self) -> list[str]:
        override: list[str] | None = self.config.get("categories_to_crawl")
        paths = override if override else self.CATEGORY_PATHS
        return [f"{self.base_url}{path}" for path in paths]

    def parse_product_list(self, page: Any) -> list[dict[str, Any]]:
        products: list[dict[str, Any]] = []
        cards = page.css(".product-card, .product-item", auto_save=True)
        for card in cards:
            name = card.css_first(".product-name::text, h3::text, h2::text")
            price = card.css_first(".price::text, .product-price::text")
            link = card.css_first("a::attr(href)")
            image = card.css_first("img::attr(src), img::attr(data-src)")

            if link:
                products.append(
                    {
                        "name": str(name).strip() if name else "",
                        "price_text": str(price).strip() if price else "",
                        "url": absolute_url(self.base_url, str(link)),
                        "image": absolute_url(self.base_url, str(image))
                        if image
                        else None,
                    }
                )
        return products

    def parse_product_detail(self, page: Any, url: str) -> CrawledProduct:
        name = page.css_first("h1::text")
        price_text = page.css_first(".product-price::text, .price::text")
        description = page.css_first(".product-description, .description")
        images = page.css(".product-gallery img::attr(src), .gallery img::attr(src)")
        sku = page.css_first(".product-sku::text, [data-sku]::attr(data-sku)")

        breadcrumbs = page.css(".breadcrumb a::text, .breadcrumbs a::text")
        category_hint = (
            str(breadcrumbs.getall()[-1]).strip() if breadcrumbs else None
        )

        surface_tag: str | None = None
        if category_hint:
            for keyword, surface in SURFACE_MAP.items():
                if keyword in category_hint.lower():
                    surface_tag = surface
                    break

        tags = ["ochoa", "ferreteria"]
        if surface_tag:
            tags.append(surface_tag)

        return CrawledProduct(
            source_url=url,
            source_sku=str(sku).strip() if sku else None,
            name=str(name).strip() if name else "",
            name_es=str(name).strip() if name else "",
            price=parse_dop_price(str(price_text)) if price_text else None,
            currency="DOP",
            category_hint=category_hint,
            description=description.text if description else None,
            description_es=description.text if description else None,
            images=[
                absolute_url(self.base_url, str(img)) for img in images.getall()
            ]
            if images
            else [],
            tags=tags,
        )

    def get_next_page_url(self, page: Any) -> str | None:
        next_link = page.css_first(
            'a[rel="next"]::attr(href), .next-page::attr(href)'
        )
        if next_link:
            return absolute_url(self.base_url, str(next_link))
        return None
