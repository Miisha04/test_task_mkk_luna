from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..schemas.organization import OrganizationResponse
from ..services import organization as organization_service

router = APIRouter()

@router.get(
    "/",
    response_model=list[OrganizationResponse],
    status_code=200
)
async def get_organizations(
    building_id: int,
    db: AsyncSession = Depends(get_db),
) -> list[OrganizationResponse]:
    return await organization_service.get_organizations(db, building_id)