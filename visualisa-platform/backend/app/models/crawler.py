"""
Web Crawler Models: CrawlSource, CrawlJob, CrawlResult
"""
import uuid
from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import Boolean, DateTime, Enum, Float, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin, UUIDMixin


class CrawlStatus(str, PyEnum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    PAUSED = "paused"


class CrawlSource(Base, UUIDMixin, TimestampMixin):
    """Represents a crawlable website source (Aliss, Ochoa, IKEA DR)."""
    __tablename__ = "crawl_sources"

    name: Mapped[str] = mapped_column(String(255))
    slug: Mapped[str] = mapped_column(String(100), unique=True)
    base_url: Mapped[str] = mapped_column(String(500))
    brand_id: Mapped[uuid.UUID | None] = mapped_column(
        CHAR(36), ForeignKey("brands.id"), nullable=True
    )
    crawler_class: Mapped[str] = mapped_column(String(100))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    config: Mapped[dict] = mapped_column(JSON, default=dict)
    schedule: Mapped[str | None] = mapped_column(String(50), nullable=True)

    jobs: Mapped[list["CrawlJob"]] = relationship(back_populates="source", lazy="dynamic")
    brand: Mapped["Brand | None"] = relationship(lazy="selectin")  # type: ignore[name-defined]


class CrawlJob(Base, UUIDMixin, TimestampMixin):
    """An individual crawl execution."""
    __tablename__ = "crawl_jobs"

    source_id: Mapped[uuid.UUID] = mapped_column(CHAR(36), ForeignKey("crawl_sources.id"))
    status: Mapped[CrawlStatus] = mapped_column(Enum(CrawlStatus), default=CrawlStatus.PENDING)
    triggered_by: Mapped[str] = mapped_column(String(50))
    triggered_by_user_id: Mapped[uuid.UUID | None] = mapped_column(
        CHAR(36), ForeignKey("users.id"), nullable=True
    )

    # Progress tracking
    pages_crawled: Mapped[int] = mapped_column(Integer, default=0)
    products_found: Mapped[int] = mapped_column(Integer, default=0)
    products_new: Mapped[int] = mapped_column(Integer, default=0)
    products_updated: Mapped[int] = mapped_column(Integer, default=0)
    products_failed: Mapped[int] = mapped_column(Integer, default=0)
    errors: Mapped[list] = mapped_column(JSON, default=list)

    # Timing
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    duration_seconds: Mapped[float | None] = mapped_column(Float, nullable=True)
    log: Mapped[str | None] = mapped_column(Text, nullable=True)

    source: Mapped["CrawlSource"] = relationship(back_populates="jobs", lazy="selectin")
    results: Mapped[list["CrawlResult"]] = relationship(
        back_populates="job", cascade="all, delete-orphan"
    )


class CrawlResult(Base, UUIDMixin, TimestampMixin):
    """Individual product extracted from a crawl, pending review."""
    __tablename__ = "crawl_results"

    job_id: Mapped[uuid.UUID] = mapped_column(CHAR(36), ForeignKey("crawl_jobs.id"))
    product_id: Mapped[uuid.UUID | None] = mapped_column(
        CHAR(36), ForeignKey("products.id"), nullable=True
    )

    # Raw extracted data
    raw_data: Mapped[dict] = mapped_column(JSON)
    source_url: Mapped[str] = mapped_column(String(1000))
    source_sku: Mapped[str | None] = mapped_column(String(100), nullable=True)

    # Normalized fields (pipeline output)
    normalized_name: Mapped[str | None] = mapped_column(String(500), nullable=True)
    normalized_price: Mapped[float | None] = mapped_column(Float, nullable=True)
    normalized_currency: Mapped[str | None] = mapped_column(String(3), nullable=True)
    normalized_category: Mapped[str | None] = mapped_column(String(100), nullable=True)
    normalized_images: Mapped[list] = mapped_column(JSON, default=list)

    # Review status
    is_approved: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    reviewed_by: Mapped[uuid.UUID | None] = mapped_column(
        CHAR(36), ForeignKey("users.id"), nullable=True
    )
    review_notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Deduplication
    is_duplicate: Mapped[bool] = mapped_column(Boolean, default=False)
    matched_product_id: Mapped[uuid.UUID | None] = mapped_column(CHAR(36), nullable=True)
    dedup_hash: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)

    job: Mapped["CrawlJob"] = relationship(back_populates="results")
