from pydantic import BaseModel


class UserEdit(BaseModel):
    username: str | None = None