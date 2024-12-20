from pydantic import BaseModel


class RoomSettingsEdit(BaseModel):
    private: bool | None = None
    only_host_can_skip: bool | None = None
    percent_skips_needed: int | None = None


class RoomEdit(BaseModel):
    name: str | None = None
    settings: RoomSettingsEdit | None = None