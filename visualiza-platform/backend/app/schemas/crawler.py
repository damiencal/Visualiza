"""
Crawler schemas
"""
from datetime import datetime

from pydantic import BaseModel


class CrawlSourceResponse(BaseModel):
    id: str
    name: str
    slug: str
    base_url: str
    crawler_class: str
    is_active: bool
    config: dict
    schedule: str | None = None
    model_config = {"from_attributes": True}


class CrawlSourceUpdate(BaseModel):
    is_active: bool | None = None
    config: dict | None = None
    schedule: str | None = None


class CrawlJobResponse(BaseModel):
    id: str
    source_id: str
    status: str
    triggered_by: str
    pages_crawled: int
    products_found: int
    products_new: int
    products_updated: int
    products_failed: int
    errors: list
    started_at: datetime | None = None
    completed_at: datetime | None = None
    duration_seconds: float | None = None
    created_at: datetime
    source: CrawlSourceResponse | None = None
    model_config = {"from_attributes": True}


class CrawlResultResponse(BaseModel):
    id: str
    job_id: str
    source_url: str
    source_sku: str | None = None
    normalized_name: str | None = None
    normalized_price: float | None = None
    normalized_currency: str | None = None
    normalized_category: str | None = None
    normalized_images: list
    raw_data: dict
    is_approved: bool | None = None
    is_duplicate: bool
    review_notes: str | None = None
    created_at: datetime
    model_config = {"from_attributes": True}


class ReviewCrawlResult(BaseModel):
    approved: bool
    notes: str | None = None


class TriggerCrawlRequest(BaseModel):
    source_id: str
