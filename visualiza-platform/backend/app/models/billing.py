"""
Billing Models: Plan, Subscription, Invoice, Usage
"""
import uuid
from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import Boolean, DateTime, Enum, Float, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin, UUIDMixin


class PlanTier(str, PyEnum):
    STARTER = "starter"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"


class SubscriptionStatus(str, PyEnum):
    TRIALING = "trialing"
    ACTIVE = "active"
    PAST_DUE = "past_due"
    CANCELLED = "cancelled"
    UNPAID = "unpaid"


class Plan(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "plans"

    name: Mapped[str] = mapped_column(String(100))
    name_es: Mapped[str] = mapped_column(String(100))
    tier: Mapped[PlanTier] = mapped_column(Enum(PlanTier), unique=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    description_es: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Pricing (USD)
    price_monthly_usd: Mapped[float] = mapped_column(Float)
    price_yearly_usd: Mapped[float] = mapped_column(Float)
    stripe_price_id_monthly: Mapped[str] = mapped_column(String(255), default="")
    stripe_price_id_yearly: Mapped[str] = mapped_column(String(255), default="")

    # Limits
    max_visualizations_per_month: Mapped[int] = mapped_column(Integer)
    max_bom_exports_per_month: Mapped[int] = mapped_column(Integer)
    max_domains: Mapped[int] = mapped_column(Integer)
    max_api_calls_per_day: Mapped[int] = mapped_column(Integer)
    includes_analytics: Mapped[bool] = mapped_column(Boolean, default=False)
    includes_custom_branding: Mapped[bool] = mapped_column(Boolean, default=False)
    includes_priority_support: Mapped[bool] = mapped_column(Boolean, default=False)

    features: Mapped[list] = mapped_column(JSON, default=list)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)

    subscriptions: Mapped[list["Subscription"]] = relationship(back_populates="plan")


class Subscription(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "subscriptions"

    user_id: Mapped[uuid.UUID] = mapped_column(CHAR(36), ForeignKey("users.id"))
    plan_id: Mapped[uuid.UUID] = mapped_column(CHAR(36), ForeignKey("plans.id"))
    status: Mapped[SubscriptionStatus] = mapped_column(Enum(SubscriptionStatus))
    billing_cycle: Mapped[str] = mapped_column(String(10))  # "monthly" | "yearly"

    # Stripe references
    stripe_subscription_id: Mapped[str] = mapped_column(String(255), unique=True)
    stripe_customer_id: Mapped[str] = mapped_column(String(255))

    # Usage tracking (current billing period)
    visualizations_used: Mapped[int] = mapped_column(Integer, default=0)
    bom_exports_used: Mapped[int] = mapped_column(Integer, default=0)
    api_calls_today: Mapped[int] = mapped_column(Integer, default=0)

    current_period_start: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    current_period_end: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    trial_end: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    cancelled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    user: Mapped["User"] = relationship(back_populates="subscriptions")  # type: ignore[name-defined]
    plan: Mapped["Plan"] = relationship(back_populates="subscriptions", lazy="selectin")
