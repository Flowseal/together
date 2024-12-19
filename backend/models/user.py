from pydantic import BaseModel, Field, ConfigDict


class User(BaseModel):
    id: str
    username: str = Field(min_length=3)
    
    model_config = ConfigDict(revalidate_instances='always')