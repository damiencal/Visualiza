"""
BoM router
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_professional, get_db
from app.models.professional import ProfessionalProfile
from app.models.user import User
from app.schemas.bom import BomGenerateRequest, BomResponse, BomShareResponse
from app.services.bom_service import BomService

router = APIRouter(prefix="/bom", tags=["Bill of Materials"])


@router.post("/generate", response_model=BomResponse, status_code=201)
async def generate_bom(
    data: BomGenerateRequest,
    auth: tuple[User, ProfessionalProfile] = Depends(get_current_professional),
    db: AsyncSession = Depends(get_db),
):
    _, profile = auth
    return await BomService.generate_bom(data, db, professional_id=str(profile.id))


@router.get("/{bom_id}", response_model=BomResponse)
async def get_bom(
    bom_id: str,
    db: AsyncSession = Depends(get_db),
):
    return await BomService.get_bom(bom_id, db)


@router.post("/{bom_id}/share", response_model=BomShareResponse)
async def share_bom(
    bom_id: str,
    auth: tuple[User, ProfessionalProfile] = Depends(get_current_professional),
    db: AsyncSession = Depends(get_db),
):
    bom = await BomService.share_bom(bom_id, db)
    return BomShareResponse(
        share_url=f"https://app.visualiza.do/bom/shared/{bom.share_token}",
        share_token=bom.share_token or "",
    )
