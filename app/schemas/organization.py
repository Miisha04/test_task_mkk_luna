from pydantic import BaseModel, ConfigDict

from ..schemas.phone import PhoneBase
from ..schemas.activity import ActivityBase


class OrganizationBase(BaseModel):
    name: str
    building_id: int
    phones: list[PhoneBase]
    activities: list[ActivityBase]

    model_config = ConfigDict(from_attributes=True)

class OrganizationCreate(OrganizationBase):
    pass

class OrganizationResponse(OrganizationBase):
    id: int
