"""
BaseCrawler: abstract base for all site-specific crawlers
"""
import abc
import logging
import time
from dataclasses import dataclass, field
from typing import Any


@dataclass
class CrawledProduct:
    """Normalized product data extracted from a crawl."""
    source_url: str
    source_sku: str | None = None
    name: str = ""
    name_es: str | None = None
    description: str | None = None
    description_es: str | None = None
    price: float | None = None
    original_price: float | None = None
    currency: str = "DOP"
    price_unit: str = "unit"
    category_hint: str | None = None
    subcategory_hint: str | None = None
    images: list[str] = field(default_factory=list)
    specifications: dict[str, Any] = field(default_factory=dict)
    colors: list[str] = field(default_factory=list)
    materials: list[str] = field(default_factory=list)
    dimensions: dict[str, Any] | None = None
    in_stock: bool = True
    tags: list[str] = field(default_factory=list)


class BaseCrawler(abc.ABC):
    """Abstract base class for all site-specific crawlers."""

    name: str = "base"
    base_url: str = ""
    fetcher_type: str = "stealthy"   # "stealthy" | "dynamic" | "standard"
    delay_seconds: float = 2.0
    max_pages: int = 500

    def __init__(self, config: dict[str, Any] | None = None) -> None:
        self.config: dict[str, Any] = config or {}
        self.logger = logging.getLogger(f"crawler.{self.name}")
        self.fetcher_type = self.config.get("fetcher", self.fetcher_type)
        self.delay_seconds = float(self.config.get("delay_seconds", self.delay_seconds))
        self.max_pages = int(self.config.get("max_pages", self.max_pages))

    def get_fetcher(self) -> Any:
        """Return the appropriate Scrapling fetcher based on config."""
        try:
            from scrapling.fetchers import StealthyFetcher, DynamicFetcher, Fetcher

            if self.fetcher_type == "stealthy":
                StealthyFetcher.auto_match = True
                return StealthyFetcher
            elif self.fetcher_type == "dynamic":
                return DynamicFetcher
            else:
                return Fetcher
        except ImportError:
            self.logger.warning("Scrapling not installed; using requests fallback")
            return None

    def fetch_page(self, url: str, **kwargs: Any) -> Any:
        """Fetch a single page using the configured fetcher."""
        fetcher = self.get_fetcher()
        if fetcher is None:
            import requests
            resp = requests.get(url, timeout=30, headers={"User-Agent": "Mozilla/5.0"})
            resp.raise_for_status()
            return resp
        if self.fetcher_type in ("stealthy", "dynamic"):
            return fetcher.fetch(url, headless=True, network_idle=True, **kwargs)
        return fetcher.get(url, stealthy_headers=True, **kwargs)

    @abc.abstractmethod
    def get_category_urls(self) -> list[str]:
        """Return list of category page URLs to crawl."""
        ...

    @abc.abstractmethod
    def parse_product_list(self, page: Any) -> list[dict[str, Any]]:
        """Extract product links/summaries from a listing page."""
        ...

    @abc.abstractmethod
    def parse_product_detail(self, page: Any, url: str) -> CrawledProduct:
        """Extract full product details from a product page."""
        ...

    @abc.abstractmethod
    def get_next_page_url(self, page: Any) -> str | None:
        """Extract the next page URL for pagination, or None if last page."""
        ...

    def crawl(self) -> list[CrawledProduct]:
        """Execute full crawl. Returns list of extracted products."""
        products: list[CrawledProduct] = []
        pages_crawled = 0

        for category_url in self.get_category_urls():
            current_url: str | None = category_url
            while current_url and pages_crawled < self.max_pages:
                self.logger.info("Crawling: %s", current_url)
                try:
                    page = self.fetch_page(current_url)
                    summaries = self.parse_product_list(page)

                    for summary in summaries:
                        detail_url = summary.get("url")
                        if detail_url:
                            try:
                                time.sleep(self.delay_seconds)
                                detail_page = self.fetch_page(detail_url)
                                product = self.parse_product_detail(detail_page, detail_url)
                                products.append(product)
                            except Exception as e:
                                self.logger.error("Product parse error on %s: %s", detail_url, e)

                    current_url = self.get_next_page_url(page)
                    pages_crawled += 1
                    time.sleep(self.delay_seconds)

                except Exception as e:
                    self.logger.error("Page error on %s: %s", current_url, e)
                    break

        self.logger.info(
            "Crawl complete: %d products from %d pages", len(products), pages_crawled
        )
        return products
