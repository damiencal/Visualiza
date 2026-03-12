"""
Professional Portal router
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_professional, get_db
from app.models.professional import ProfessionalProfile, WidgetDeployment
from app.models.user import User
from app.schemas.common import MessageResponse
from app.schemas.widget import (
    EmbedCodeResponse, ProfessionalProfileResponse, ProfessionalProfileUpdate,
    WidgetConfigUpdate, WidgetDeploymentCreate, WidgetDeploymentResponse,
)
from app.services.bom_service import BomService
from app.services.widget_service import WidgetService

router = APIRouter(prefix="/professional", tags=["Professional Portal"])


@router.get("/profile", response_model=ProfessionalProfileResponse)
async def get_profile(
    auth: tuple[User, ProfessionalProfile] = Depends(get_current_professional),
):
    _, profile = auth
    return profile


@router.put("/profile", response_model=ProfessionalProfileResponse)
async def update_profile(
    data: ProfessionalProfileUpdate,
    auth: tuple[User, ProfessionalProfile] = Depends(get_current_professional),
    db: AsyncSession = Depends(get_db),
):
    _, profile = auth
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(profile, key, value)
    await db.flush()
    return profile


@router.get("/widget/config")
async def get_widget_config(
    auth: tuple[User, ProfessionalProfile] = Depends(get_current_professional),
):
    _, profile = auth
    return profile.widget_config or {}


@router.put("/widget/config", response_model=MessageResponse)
async def update_widget_config(
    data: WidgetConfigUpdate,
    auth: tuple[User, ProfessionalProfile] = Depends(get_current_professional),
    db: AsyncSession = Depends(get_db),
):
    _, profile = auth
    existing = profile.widget_config or {}
    profile.widget_config = {**existing, **data.model_dump(exclude_unset=True, exclude_none=True)}
    await db.flush()
    return MessageResponse(message="Configuración del widget actualizada")


@router.post("/widget/regenerate-key", response_model=MessageResponse)
async def regenerate_api_key(
    auth: tuple[User, ProfessionalProfile] = Depends(get_current_professional),
    db: AsyncSession = Depends(get_db),
):
    _, profile = auth
    new_key = await WidgetService.regenerate_api_key(profile, db)
    return MessageResponse(message=f"Nueva API key generada: {new_key}")


@router.get("/widget/embed-code", response_model=EmbedCodeResponse)
async def get_embed_code(
    auth: tuple[User, ProfessionalProfile] = Depends(get_current_professional),
):
    _, profile = auth
    snippet = WidgetService.generate_embed_snippet(
        profile.api_key, profile.widget_config or {}
    )
    return EmbedCodeResponse(snippet=snippet, api_key=profile.api_key)


@router.get("/widget/deployments", response_model=list[WidgetDeploymentResponse])
async def list_deployments(
    auth: tuple[User, ProfessionalProfile] = Depends(get_current_professional),
):
    _, profile = auth
    return profile.widget_deployments


@router.post("/widget/deployments", response_model=WidgetDeploymentResponse, status_code=201)
async def add_deployment(
    data: WidgetDeploymentCreate,
    auth: tuple[User, ProfessionalProfile] = Depends(get_current_professional),
    db: AsyncSession = Depends(get_db),
):
    _, profile = auth
    deployment = WidgetDeployment(
        professional_id=profile.id,
        **data.model_dump(),
    )
    db.add(deployment)
    await db.flush()
    return deployment


@router.delete("/widget/deployments/{deployment_id}", response_model=MessageResponse)
async def remove_deployment(
    deployment_id: str,
    auth: tuple[User, ProfessionalProfile] = Depends(get_current_professional),
    db: AsyncSession = Depends(get_db),
):
    from sqlalchemy import select
    from app.core.exceptions import NotFoundError
    result = await db.execute(
        select(WidgetDeployment).where(
            WidgetDeployment.id == deployment_id,
            WidgetDeployment.professional_id == auth[1].id,
        )
    )
    dep = result.scalar_one_or_none()
    if not dep:
        raise NotFoundError("Despliegue")
    await db.delete(dep)
    return MessageResponse(message="Dominio eliminado")


@router.get("/bom")
async def list_boms(
    auth: tuple[User, ProfessionalProfile] = Depends(get_current_professional),
    db: AsyncSession = Depends(get_db),
):
    _, profile = auth
    boms = await BomService.list_boms(str(profile.id), db)
    return boms


@router.get("/bom/{bom_id}")
async def get_bom(
    bom_id: str,
    auth: tuple[User, ProfessionalProfile] = Depends(get_current_professional),
    db: AsyncSession = Depends(get_db),
):
    bom = await BomService.get_bom(bom_id, db)
    return bom
