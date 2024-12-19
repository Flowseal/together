from uuid import uuid4
from typing import Optional

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import HTMLResponse

from models import Room
from dependencies.auth import get_current_user_id
from database.local_storage import Storage

router = APIRouter(
    prefix="/room",
    tags=["room"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[Room])
def list_rooms():
    storage = Storage()
    return [room for room in storage.get_rooms().values() if not room.is_private]


@router.post("/")
def create_room(name: str, is_private: bool, user_id: str = Depends(get_current_user_id)):
    storage = Storage()

    room_id = str(uuid4())
    room = Room(id=room_id, name=name, admin_id=user_id, is_private=is_private, members=[user_id])
    storage.insert_room(room)

    return HTMLResponse(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/{room_id}", response_model=Room)
def get_room(room_id: str, user_id: str = Depends(get_current_user_id)):
    storage = Storage()
    room = storage.get_room(room_id)

    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
    if user_id not in room.members:
        room.members.append(user_id)

    return room


@router.patch("/{room_id}", response_model=Room)
def edit_room(room_id: str, name: Optional[str] = None, is_private: Optional[bool] = None, user_id: str = Depends(get_current_user_id)):
    storage = Storage()
    room = storage.get_room(room_id)

    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
    if room.admin_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    
    new_room = room.model_copy()
    if name is not None:
        new_room.name = name
    if is_private is not None:
        new_room.is_private = is_private

    Room.model_validate(new_room)
    storage.update_room(room_id, new_room)

    return new_room