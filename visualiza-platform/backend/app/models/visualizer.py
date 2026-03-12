"""
Visualizer Session Models
"""
import uuid

from sqlalchemy import ForeignKey, JSON, String, Text
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin, UUIDMixin


class VisualizerSession(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "visualizer_sessions"

    professional_id: Mapped[uuid.UUID | None] = mapped_column(
        CHAR(36), ForeignKey("professional_profiles.id"), nullable=True
    )
    # Originating room image
    room_image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    room_type: Mapped[str | None] = mapped_column(String(50), nullable=True)

    # AI-segmented surfaces with mask data
    surfaces: Mapped[dict] = mapped_column(JSON, default=dict)
    # { "floor": {"mask_url": "...", "area_m2": 20.0}, "wall": {...} }

    # Applied layers (product per surface)
    layers: Mapped[list] = mapped_column(JSON, default=list)
    # [{"surface": "floor", "product_id": "...", "texture_url": "...", "opacity": 1.0}]

    # Undo/redo history snapshots
    history: Mapped[list] = mapped_column(JSON, default=list)
    current_history_index: Mapped[int] = mapped_column(default=0)

    # Latest render
    rendered_image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # Widget session tracking
    widget_api_key: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    origin_domain: Mapped[str | None] = mapped_column(String(255), nullable=True)
    property_url: Mapped[str | None] = mapped_column(String(1000), nullable=True)
