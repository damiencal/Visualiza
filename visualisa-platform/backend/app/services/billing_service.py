"""
Billing Service: Stripe integration, subscriptions, webhooks
"""
import stripe
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.core.exceptions import NotFoundError
from app.models.billing import Plan, Subscription, SubscriptionStatus
from app.models.user import User
from app.schemas.billing import CheckoutRequest, CheckoutResponse

stripe.api_key = settings.STRIPE_SECRET_KEY


class BillingService:
    @staticmethod
    async def list_plans(db: AsyncSession) -> list[Plan]:
        result = await db.execute(
            select(Plan).where(Plan.is_active.is_(True)).order_by(Plan.sort_order)
        )
        return result.scalars().all()

    @staticmethod
    async def create_checkout_session(
        user: User, data: CheckoutRequest, db: AsyncSession
    ) -> CheckoutResponse:
        result = await db.execute(select(Plan).where(Plan.id == data.plan_id))
        plan = result.scalar_one_or_none()
        if not plan:
            raise NotFoundError("Plan")

        price_id = (
            plan.stripe_price_id_monthly
            if data.billing_cycle == "monthly"
            else plan.stripe_price_id_yearly
        )

        # Get or create Stripe customer
        existing_sub = await db.execute(
            select(Subscription).where(Subscription.user_id == user.id)
        )
        sub = existing_sub.scalar_one_or_none()

        customer_id = sub.stripe_customer_id if sub else None
        if not customer_id:
            customer = stripe.Customer.create(
                email=user.email,
                name=user.full_name,
                metadata={"user_id": str(user.id)},
            )
            customer_id = customer.id

        session = stripe.checkout.Session.create(
            customer=customer_id,
            payment_method_types=["card"],
            line_items=[{"price": price_id, "quantity": 1}],
            mode="subscription",
            subscription_data={"trial_period_days": 14},
            success_url=data.success_url + "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=data.cancel_url,
            metadata={
                "user_id": str(user.id),
                "plan_id": str(plan.id),
                "billing_cycle": data.billing_cycle,
            },
        )
        return CheckoutResponse(checkout_url=session.url, session_id=session.id)

    @staticmethod
    async def create_customer_portal(user: User, return_url: str, db: AsyncSession) -> str:
        result = await db.execute(
            select(Subscription).where(Subscription.user_id == user.id)
        )
        sub = result.scalar_one_or_none()
        if not sub:
            raise NotFoundError("Suscripción")

        session = stripe.billing_portal.Session.create(
            customer=sub.stripe_customer_id,
            return_url=return_url,
        )
        return session.url

    @staticmethod
    async def handle_webhook(payload: bytes, sig_header: str, db: AsyncSession) -> dict:
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
        except stripe.error.SignatureVerificationError:
            return {"error": "Invalid signature"}

        if event["type"] == "checkout.session.completed":
            await BillingService._handle_checkout_completed(event["data"]["object"], db)
        elif event["type"] == "invoice.paid":
            await BillingService._handle_invoice_paid(event["data"]["object"], db)
        elif event["type"] == "invoice.payment_failed":
            await BillingService._handle_payment_failed(event["data"]["object"], db)
        elif event["type"] == "customer.subscription.deleted":
            await BillingService._handle_subscription_deleted(event["data"]["object"], db)

        return {"received": True}

    @staticmethod
    async def _handle_checkout_completed(session_obj: dict, db: AsyncSession) -> None:
        from datetime import datetime, timezone
        import uuid

        metadata = session_obj.get("metadata", {})
        user_id = metadata.get("user_id")
        plan_id = metadata.get("plan_id")
        billing_cycle = metadata.get("billing_cycle", "monthly")

        if not user_id or not plan_id:
            return

        stripe_sub = stripe.Subscription.retrieve(session_obj["subscription"])

        sub = Subscription(
            user_id=user_id,
            plan_id=plan_id,
            status=SubscriptionStatus.TRIALING
            if stripe_sub.status == "trialing"
            else SubscriptionStatus.ACTIVE,
            billing_cycle=billing_cycle,
            stripe_subscription_id=stripe_sub.id,
            stripe_customer_id=stripe_sub.customer,
            current_period_start=datetime.fromtimestamp(
                stripe_sub.current_period_start, tz=timezone.utc
            ),
            current_period_end=datetime.fromtimestamp(
                stripe_sub.current_period_end, tz=timezone.utc
            ),
            trial_end=datetime.fromtimestamp(stripe_sub.trial_end, tz=timezone.utc)
            if stripe_sub.trial_end
            else None,
        )
        db.add(sub)
        await db.flush()

    @staticmethod
    async def _handle_invoice_paid(invoice: dict, db: AsyncSession) -> None:
        from datetime import datetime, timezone

        stripe_sub_id = invoice.get("subscription")
        if not stripe_sub_id:
            return

        result = await db.execute(
            select(Subscription).where(
                Subscription.stripe_subscription_id == stripe_sub_id
            )
        )
        sub = result.scalar_one_or_none()
        if sub:
            sub.status = SubscriptionStatus.ACTIVE
            # Reset period counters
            sub.visualisations_used = 0
            sub.bom_exports_used = 0
            sub.api_calls_today = 0
            await db.flush()

    @staticmethod
    async def _handle_payment_failed(invoice: dict, db: AsyncSession) -> None:
        stripe_sub_id = invoice.get("subscription")
        if not stripe_sub_id:
            return
        result = await db.execute(
            select(Subscription).where(
                Subscription.stripe_subscription_id == stripe_sub_id
            )
        )
        sub = result.scalar_one_or_none()
        if sub:
            sub.status = SubscriptionStatus.PAST_DUE
            await db.flush()

    @staticmethod
    async def _handle_subscription_deleted(sub_obj: dict, db: AsyncSession) -> None:
        from datetime import datetime, timezone

        result = await db.execute(
            select(Subscription).where(
                Subscription.stripe_subscription_id == sub_obj["id"]
            )
        )
        sub = result.scalar_one_or_none()
        if sub:
            sub.status = SubscriptionStatus.CANCELLED
            sub.cancelled_at = datetime.now(timezone.utc)
            await db.flush()
