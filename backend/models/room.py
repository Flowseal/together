from datetime import datetime, timezone
from pydantic import BaseModel, Field, ConfigDict


def datetime_now() -> datetime:
    return datetime.now(timezone.utc)


class Room(BaseModel):
    id: str
    name: str = Field(min_length=3)
    admin_id: str
    created_at: datetime = Field(default_factory=datetime_now)
    is_private: bool = Field()
    members: list[str]

    model_config = ConfigDict(revalidate_instances='always')