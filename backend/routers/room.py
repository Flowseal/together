from uuid import uuid4
from typing import Optional

from fastapi import APIRouter, Depends, status, HTTPException

from models import Room, RoomSettings
from models.contracts import RoomCreate, RoomEdit
from utils import dump_model, update_model_from
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
    return [room for room in storage.get_rooms().values() if not room.settings.private]


@router.post("/", response_model=Room)
def create_room(room_create: RoomCreate, user_id: str = Depends(get_current_user_id)):
    storage = Storage()

    room_settings = RoomSettings(**dump_model(room_create.settings))

    room_id = str(uuid4())
    room = Room(
        id=room_id, 
        name=room_create.name, 
        settings=room_settings,
        admin_id=user_id, 
        members=[user_id]
    )

    Room.model_validate(room)
    storage.insert_room(room)

    return room


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
def edit_room(room_id: str, room_edit: RoomEdit, user_id: str = Depends(get_current_user_id)):
    storage = Storage()
    room = storage.get_room(room_id)

    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
    if room.admin_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    
    new_room = room.model_copy()
    update_model_from(new_room, room_edit)

    Room.model_validate(new_room)
    storage.update_room(room_id, new_room)

    return new_room