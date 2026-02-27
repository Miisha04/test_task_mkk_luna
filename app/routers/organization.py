from fastapi import APIRouter, HTTPException, Depends, Query
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
    building_id: int | None = Query(None, description="ID здания"),
    activity_id: int | None = Query(None, description="ID деятельности"),
    activity: str | None = Query(None, description="Название деятельности"),
    db: AsyncSession = Depends(get_db),
) -> list[OrganizationResponse]:
    return await organization_service.get_organizations(db, building_id, activity_id, activity)


@router.get(
    "/organization",
    response_model=OrganizationResponse,
    status_code=200
)
async def get_organization(
    name: str | None = Query(None, description="Название организации"),
    id: int | None = Query(None, description="ID организации"),
    db: AsyncSession = Depends(get_db),
) -> OrganizationResponse:

    response = await organization_service.get_organization(db, name, id)

    if not response:
        raise HTTPException(
            status_code=404,
            detail="Organization not found"
        )
    
    return response


@router.get(
    "/in_area",
    response_model=list[OrganizationResponse],
    status_code=200
)
async def get_organizations_in_area(
    radius: int = Query(..., description="Радиус в метрах"),
    lat: float = Query(..., description="Сев широта"),
    lon: float = Query(..., description="Вос долгота"),
    db: AsyncSession = Depends(get_db)
) -> list[OrganizationResponse]:
    
    response = await organization_service.get_organizations_in_radius(db, radius, lat, lon)

    if not response:
        raise HTTPException(
            status_code=404,
            detail="Organizations not found in area"
        )
    
    return response 


@router.get(
    "/in_square",
    response_model=list[OrganizationResponse],
    status_code=200
)
async def get_organizations_in_square(
    min_lat: float = Query(..., description="Мин сев широта (от)"),
    min_lon: float = Query(..., description="Мин вос долгота (от)"),
    max_lat: float = Query(..., description="Макс сев широта (до)"),
    max_lon: float = Query(..., description="Макс вост долгота (до)"),
    db: AsyncSession = Depends(get_db)
) -> list[OrganizationResponse]:
    
    response = await organization_service.get_organizations_in_square(db, min_lat, min_lon, max_lat, max_lon)

    if not response:
        raise HTTPException(
            status_code=404,
            detail="Organizations not found in square"
        )
    
    return response 