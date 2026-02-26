from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.organization import Organization

async def get_organizations_by_building(
    db: AsyncSession,
    building_id: int 
) -> list[Organization]:
    result = await db.execute(
        select(Organization)
        .options(
            selectinload(Organization.phones),
            selectinload(Organization.activities),
        )
        .where(Organization.building_id == building_id)
    )

    return result.scalars().all()

