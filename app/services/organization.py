from sqlalchemy.ext.asyncio import AsyncSession 

from ..repositories import organization as organization_repos
from ..models.organization import Organization
from ..schemas.organization import OrganizationCreate, OrganizationResponse
from ..schemas.activity import ActivityBase
from ..schemas.phone import PhoneBase

async def get_organizations(
    db: AsyncSession,
    building_id: int | None = None,
    activity_id: int | None = None,
    activity: str | None = None
) -> list[OrganizationResponse]:
    
    if building_id:
        organizations_obj = await organization_repos.get_organizations_by_building(db, building_id)
    
    if activity_id:
        organizations_obj = await organization_repos.get_organizations_by_activity_id(db, activity_id)
    
    if activity:
        organizations_obj = await organization_repos.get_organizations_by_activity_name(db, activity)


    organizations = [
        OrganizationResponse.model_validate(obj)
        for obj in organizations_obj
    ]

    return organizations
    

async def get_organization(
    db: AsyncSession,
    name: str | None = None,
    id: int | None = None
) -> OrganizationResponse | None:
    if name:
        org_obj = await organization_repos.get_organization_by_name(db, name)
    
    if id:
        org_obj = await organization_repos.get_organization_by_id(db, id)

    if not org_obj:
        return None
    
    return OrganizationResponse.model_validate(org_obj)


async def get_organizations_in_radius(
    db: AsyncSession,
    radius: int,
    lat: float,
    lon: float
) -> list[OrganizationResponse]:
    
    org_orbj = await organization_repos.get_organizations_in_radius(db, radius, lat, lon)

    organizations = [
        OrganizationResponse.model_validate(obj)
        for obj in org_orbj
    ]

    return organizations


async def get_organizations_in_square(
    db: AsyncSession,
    min_lat: float,
    min_lon: float,
    max_lat: float,
    max_lon: float,
) -> list[OrganizationResponse]:
    
    org_orbj = await organization_repos.get_organizations_in_square(db, min_lat, min_lon, max_lat, max_lon)

    organizations = [
        OrganizationResponse.model_validate(obj)
        for obj in org_orbj
    ]

    return organizations
