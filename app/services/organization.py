from sqlalchemy.ext.asyncio import AsyncSession 

from ..repositories import organization as organization_repos
from ..models.organization import Organization
from ..schemas.organization import OrganizationCreate, OrganizationResponse
from ..schemas.activity import ActivityBase
from ..schemas.phone import PhoneBase

async def get_organizations(
    db: AsyncSession,
    building_id: int
) -> list[OrganizationResponse]:
    organizations_obj = await organization_repos.get_organizations_by_building(db, building_id)

    organizations = [
        OrganizationResponse.model_validate(obj)
        for obj in organizations_obj
    ]

    # for obj in organizations_obj:
    #     phones_validated = [
    #         PhoneBase.model_validate(phone)
    #         for phone in obj.phones
    #     ]

    #     activities_validated = [
    #         ActivityBase.model_validate(activity)
    #         for activity in obj.activities
    #     ]

    #     org_response = OrganizationResponse.model_validate({
    #         **obj.__dict__,
    #         "phones": phones_validated,
    #         "activities": activities_validated
    #     })

    #     organizations.append(org_response)

    return organizations
    

    
    