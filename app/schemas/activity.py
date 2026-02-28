from pydantic import BaseModel, ConfigDict


class ActivityBase(BaseModel):
    id: int
    name: str
    level: int
    parent_id: int | None = None

    model_config = ConfigDict(from_attributes=True)