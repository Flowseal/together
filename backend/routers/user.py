from typing import Optional

from fastapi import APIRouter, Depends

from models import Room, User
from dependencies.auth import get_current_user_id
from database.local_storage import Storage

router = APIRouter(
    prefix="/user",
    tags=["user"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=User)
def user_info(user_id: str = Depends(get_current_user_id)):
    storage = Storage()
    user = storage.get_user(user_id)
    return user


@router.patch("/", response_model=User)
def edit_user(username: Optional[str], user_id: str = Depends(get_current_user_id)):
    storage = Storage()
    user = storage.get_user(user_id)
    new_user = user.model_copy()

    if username is not None:
        new_user.username = username
    
    User.model_validate(new_user)
    storage.update_user(user_id, new_user)

    return new_user


@router.get("/rooms", response_model=list[Room])
def my_rooms(user_id: str = Depends(get_current_user_id)):
    storage = Storage()
    joined_rooms = [room for room in storage.get_rooms().values() if user_id in room.members]
    return joined_rooms