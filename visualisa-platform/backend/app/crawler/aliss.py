"""
Aliss.do Crawler
"""
from typing import Any

from .base import BaseCrawler, CrawledProduct
from .utils import absolute_url, parse_dop_price


class AlissCrawler(BaseCrawler):
    name = "aliss"
    base_url = "https://aliss.do"
    fetcher_type = "stealthy"

    CATEGORY_PATHS = [
        "/hogar/decoracion",
        "/hogar/organizacion",
        "/hogar/bano",
        "/hogar/cocina",
        "/hogar/iluminacion",
        "/hogar/muebles",
        "/hogar/textiles",
        "/hogar/cortinas",
        "/hogar/alfombras",
    ]

    def get_category_urls(self) -> list[str]:
        override: list[str] | None = self.config.get("categories_to_crawl")
        paths = override if override else self.CATEGORY_PATHS
        return [f"{self.base_url}{path}" for path in paths]

    def parse_product_list(self, page: Any) -> list[dict[str, Any]]:
        products: list[dict[str, Any]] = []
        cards = page.css(
            ".product-card, .product-item, [data-product]", auto_save=True
        )
        for card in cards:
            name = card.css_first(
                ".product-name::text, .product-title::text, h3::text"
            )
            price = card.css_first(".product-price::text, .price::text")
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
        name = page.css_first("h1::text, .product-detail-name::text")
        price_text = page.css_first(".product-price::text, .price-current::text")
        orig_price_text = page.css_first(
            ".price-original::text, .price-was::text"
        )
        description = page.css_first(
            ".product-description, .product-detail-description"
        )
        images = page.css("img.product-image::attr(src), .gallery img::attr(src)")
        sku = page.css_first("[data-sku]::attr(data-sku), .product-sku::text")

        specs: dict[str, str] = {}
        for row in page.css(".specs-table tr, .product-specs li"):
            key = row.css_first("th::text, .spec-label::text")
            val = row.css_first("td::text, .spec-value::text")
            if key and val:
                specs[str(key).strip()] = str(val).strip()

        return CrawledProduct(
            source_url=url,
            source_sku=str(sku).strip() if sku else None,
            name=str(name).strip() if name else "",
            name_es=str(name).strip() if name else "",
            price=parse_dop_price(str(price_text)) if price_text else None,
            original_price=parse_dop_price(str(orig_price_text))
            if orig_price_text
            else None,
            currency="DOP",
            description=description.text if description else None,
            description_es=description.text if description else None,
            images=[
                absolute_url(self.base_url, str(img)) for img in images.getall()
            ]
            if images
            else [],
            specifications=specs,
            tags=["aliss", "hogar"],
        )

    def get_next_page_url(self, page: Any) -> str | None:
        next_link = page.css_first(
            "a.pagination-next::attr(href), "
            'a[rel="next"]::attr(href), '
            ".pagination a:last-child::attr(href)"
        )
        if next_link:
            return absolute_url(self.base_url, str(next_link))
        return None
