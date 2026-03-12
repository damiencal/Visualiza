"""
BoM Service: calculate quantities, wastage, pricing, ITBIS tax
"""
import secrets

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.core.exceptions import NotFoundError
from app.models.bom import BillOfMaterials, BomLineItem
from app.models.product import Product
from app.schemas.bom import BomGenerateRequest


# Wastage defaults by surface type
WASTAGE_DEFAULTS: dict[str, float] = {
    "floor": 10.0,
    "wall": 10.0,
    "ceiling": 5.0,
    "countertop": 5.0,
    "exterior": 12.0,
    "cabinet": 5.0,
}

# Default wastage for paint: 5%
PAINT_WASTAGE: float = 5.0


class BomService:
    @staticmethod
    async def generate_bom(
        data: BomGenerateRequest,
        db: AsyncSession,
        professional_id: str | None = None,
    ) -> BillOfMaterials:
        line_items: list[BomLineItem] = []
        subtotal = 0.0

        for item_req in data.line_items:
            result = await db.execute(
                select(Product).where(Product.id == item_req.product_id)
            )
            product = result.scalar_one_or_none()
            if not product:
                raise NotFoundError(f"Producto {item_req.product_id}")

            wastage = item_req.wastage_percent / 100
            quantity_with_wastage = round(item_req.quantity * (1 + wastage), 3)
            unit_price = product.price
            line_total = round(quantity_with_wastage * unit_price, 2)
            subtotal += line_total

            line_items.append(
                BomLineItem(
                    product_id=item_req.product_id,
                    surface_type=item_req.surface_type,
                    quantity=item_req.quantity,
                    unit=item_req.unit,
                    unit_price=unit_price,
                    line_total=line_total,
                    wastage_percent=item_req.wastage_percent,
                    quantity_with_wastage=quantity_with_wastage,
                    notes=item_req.notes,
                )
            )

        tax_rate = settings.DR_ITBIS_RATE
        tax_amount = round(subtotal * tax_rate, 2)
        total = round(subtotal + tax_amount, 2)

        bom = BillOfMaterials(
            professional_id=professional_id,
            session_id=data.session_id,
            room_type=data.room_type,
            room_image_url=data.room_image_url,
            measurements=data.measurements,
            subtotal=subtotal,
            tax_rate=tax_rate,
            tax_amount=tax_amount,
            total=total,
            notes=data.notes,
            currency="DOP",
        )
        db.add(bom)
        await db.flush()

        for item in line_items:
            item.bom_id = bom.id
            db.add(item)

        await db.flush()
        await db.refresh(bom, attribute_names=["line_items"])
        return bom

    @staticmethod
    async def get_bom(bom_id: str, db: AsyncSession) -> BillOfMaterials:
        result = await db.execute(
            select(BillOfMaterials).where(BillOfMaterials.id == bom_id)
        )
        bom = result.scalar_one_or_none()
        if not bom:
            raise NotFoundError("Presupuesto")
        return bom

    @staticmethod
    async def share_bom(bom_id: str, db: AsyncSession) -> BillOfMaterials:
        bom = await BomService.get_bom(bom_id, db)
        if not bom.share_token:
            bom.share_token = secrets.token_urlsafe(42)
        bom.is_shared = True
        await db.flush()
        return bom

    @staticmethod
    async def list_boms(
        professional_id: str, db: AsyncSession, limit: int = 20, offset: int = 0
    ) -> list[BillOfMaterials]:
        result = await db.execute(
            select(BillOfMaterials)
            .where(BillOfMaterials.professional_id == professional_id)
            .order_by(BillOfMaterials.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return result.scalars().all()
