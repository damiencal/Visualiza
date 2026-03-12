"""Crawler package init"""
from .base import BaseCrawler, CrawledProduct  # noqa: F401
from .aliss import AlissCrawler  # noqa: F401
from .ochoa import OchoaCrawler  # noqa: F401
from .ikea_dr import IkeaDRCrawler  # noqa: F401
from .pipeline import ProductPipeline  # noqa: F401
