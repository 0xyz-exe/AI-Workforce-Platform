from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class IDModel(ORMModel):
    id: int


class TimestampedModel(IDModel):
    created_at: datetime
    updated_at: datetime
