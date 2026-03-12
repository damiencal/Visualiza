"""
IKEA DR Crawler
"""
from typing import Any

from .base import BaseCrawler, CrawledProduct
from .utils import absolute_url, parse_dop_price


class IkeaDRCrawler(BaseCrawler):
    name = "ikea_dr"
    base_url = "https://www.ikea.com.do/es"
    fetcher_type = "stealthy"

    CATEGORY_PATHS = [
        "/cat/muebles-de-salon",
        "/cat/muebles-de-dormitorio",
        "/cat/cocina",
        "/cat/bano",
        "/cat/iluminacion",
        "/cat/textiles",
        "/cat/decoracion",
        "/cat/almacenaje",
        "/cat/mesas-y-escritorios",
        "/cat/estanterias",
    ]

    def get_category_urls(self) -> list[str]:
        override: list[str] | None = self.config.get("categories_to_crawl")
        paths = override if override else self.CATEGORY_PATHS
        return [f"{self.base_url}{path}" for path in paths]

    def parse_product_list(self, page: Any) -> list[dict[str, Any]]:
        products: list[dict[str, Any]] = []
        cards = page.css(
            ".plp-fragment-wrapper, .product-compact, "
            "[data-testid='plp-product'], .range-catalog-product",
            auto_save=True,
        )
        for card in cards:
            name = card.css_first(
                ".plp-product-name::text, "
                ".range-revamp-header-section__title--small::text, "
                "h3 span::text"
            )
            price = card.css_first(
                ".plp-price__integer::text, "
                ".range-revamp-price__integer::text, "
                ".product-price::text"
            )
            link = card.css_first("a::attr(href)")
            image = card.css_first("img::attr(src), img::attr(data-src)")

            if link:
                products.append(
                    {
                        "name": str(name).strip() if name else "",
                        "price_text": str(price).strip() if price else "",
                        "url": absolute_url(self.base_url, str(link)),
                        "image": str(image) if image else None,
                    }
                )
        return products

    def parse_product_detail(self, page: Any, url: str) -> CrawledProduct:
        name = page.css_first(
            ".product-header h1::text, "
            ".pip-header-section__title--big::text, "
            "h1 .range-revamp-header-section__title--big::text"
        )
        description_el = page.css_first(
            ".pip-header-section__description::text, .product-description::text"
        )
        price_integer = page.css_first(
            ".pip-price__integer::text, .range-revamp-price__integer::text"
        )
        article_number = page.css_first(
            ".pip-product-identifier__value::text, "
            "[data-testid='article-number']::text"
        )
        images = page.css(
            ".pip-image img::attr(src), .product-pictures img::attr(src)"
        )

        dimensions: dict[str, str] = {}
        for item in page.css(".pip-product-dimensions__list-item"):
            label = item.css_first(".pip-product-dimensions__label::text")
            value = item.css_first(".pip-product-dimensions__value::text")
            if label and value:
                dimensions[str(label).strip()] = str(value).strip()

        return CrawledProduct(
            source_url=url,
            source_sku=str(article_number).strip() if article_number else None,
            name=str(name).strip() if name else "",
            name_es=str(name).strip() if name else "",
            price=parse_dop_price(str(price_integer)) if price_integer else None,
            currency="DOP",
            description=str(description_el).strip() if description_el else None,
            description_es=str(description_el).strip() if description_el else None,
            images=[str(img) for img in images.getall()] if images else [],
            dimensions=dimensions or None,
            tags=["ikea", "muebles"],
        )

    def get_next_page_url(self, page: Any) -> str | None:
        next_btn = page.css_first(
            'a[data-testid="pagination-next"]::attr(href), '
            ".plp-load-more a::attr(href), "
            "a.show-more::attr(href)"
        )
        if next_btn:
            return absolute_url(self.base_url, str(next_btn))
        return None
