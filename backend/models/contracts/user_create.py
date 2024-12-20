from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    username: str