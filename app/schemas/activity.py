from pydantic import BaseModel, ConfigDict


class ActivityBase(BaseModel):
    name: str
    level: int
    parent_id: int

    model_config = ConfigDict(from_attributes=True)