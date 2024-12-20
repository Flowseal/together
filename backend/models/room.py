from datetime import datetime, timezone
from pydantic import BaseModel, Field, ConfigDict


def datetime_now() -> datetime:
    return datetime.now(timezone.utc)


class RoomSettings(BaseModel):
    private: bool = Field(default=False)
    only_host_can_skip: bool = Field(default=False)
    percent_skips_needed: int = Field(default=25, ge=0, le=100)  # [0; 100]

    model_config = ConfigDict(revalidate_instances='always')


class Room(BaseModel):
    id: str
    name: str = Field(min_length=3)
    admin_id: str
    created_at: datetime = Field(default_factory=datetime_now)
    settings: RoomSettings = Field(default_factory=RoomSettings)
    members: list[str]

    model_config = ConfigDict(revalidate_instances='always')
