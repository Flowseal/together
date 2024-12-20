from pydantic import BaseModel


class RoomSettingsCreate(BaseModel):
    private: bool | None = None
    only_host_can_skip: bool | None = None
    percent_skips_needed: int | None = None


class RoomCreate(BaseModel):
    name: str
    settings: RoomSettingsCreate | None = None