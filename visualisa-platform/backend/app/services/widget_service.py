"""
Widget Service: API key validation, origin checking, embed code generation
"""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import generate_api_key, hash_password
from app.models.professional import ProfessionalProfile, WidgetDeployment


class WidgetService:
    CDN_BASE = "https://cdn.visualisa.web.do/widget/v1"
    APP_BASE = "https://app.visualisa.web.do"

    @classmethod
    async def validate_widget_access(
        cls, api_key: str, origin: str, db: AsyncSession
    ) -> dict:
        result = await db.execute(
            select(ProfessionalProfile).where(ProfessionalProfile.api_key == api_key)
        )
        profile = result.scalar_one_or_none()
        if not profile:
            return {"valid": False}

        # Check origin against authorized domains
        domain = origin.replace("https://", "").replace("http://", "").rstrip("/")
        deployments_result = await db.execute(
            select(WidgetDeployment).where(
                WidgetDeployment.professional_id == profile.id,
                WidgetDeployment.is_active.is_(True),
            )
        )
        deployments = deployments_result.scalars().all()
        authorized_domains = [d.domain for d in deployments]

        # In development: allow any origin
        is_authorized = not authorized_domains or any(
            domain.endswith(d) for d in authorized_domains
        )

        if not is_authorized:
            return {"valid": False, "reason": "domain_not_authorized"}

        widget_config = profile.widget_config or {}
        # Merge deployment-specific config if found
        matching_deployment = next(
            (d for d in deployments if domain.endswith(d.domain)), None
        )
        if matching_deployment:
            widget_config = {
                **widget_config,
                "button_text": matching_deployment.button_text,
                "button_position": matching_deployment.button_position,
                "custom_css": matching_deployment.custom_css,
            }

        return {"valid": True, "widget_config": widget_config}

    @classmethod
    def generate_embed_snippet(cls, api_key: str, config: dict) -> str:
        button_text = config.get("button_text", "Redecorar")
        accent_color = config.get("accent_color", "#F43F5E")
        position = config.get("button_position", "bottom-right")

        return (
            f'<!-- Visualisa Widget — pegar antes de </body> -->\n'
            f'<script\n'
            f'  src="{cls.CDN_BASE}/visualisa-widget.js"\n'
            f'  data-api-key="{api_key}"\n'
            f'  data-lang="es"\n'
            f'  data-accent-color="{accent_color}"\n'
            f'  data-button-text="{button_text}"\n'
            f'  data-button-position="{position}"\n'
            f'  async\n'
            f'></script>'
        )

    @classmethod
    async def regenerate_api_key(
        cls, profile: ProfessionalProfile, db: AsyncSession
    ) -> str:
        new_key = generate_api_key()
        profile.api_key = new_key
        await db.flush()
        return new_key
