from models import Room, User
from utils import Singleton


class Storage(metaclass=Singleton):
    def __init__(self):
        self.__rooms: dict[str, Room] = {}
        self.__users: dict[str, User] = {}

    def get_rooms(self) -> dict[str, Room]:
        return self.__rooms

    def get_room(self, room_id: str) -> Room:
        return self.__rooms.get(room_id, None)

    def insert_room(self, room: Room) -> None:
        self.__rooms[room.id] = room
    
    def update_room(self, room_id: str, room: Room) -> bool:
        if room_id not in self.__rooms:
            return False
        
        self.__rooms[room_id] = room
        return True
    
    def delete_room(self, room_id: str) -> bool:
        if room_id not in self.__rooms:
            return False
        
        del self.__rooms[room_id]
        return True
    
    def get_users(self) -> dict[str, User]:
        return self.__users

    def get_user(self, user_id: str) -> User:
        return self.__users.get(user_id, None)
    
    def insert_user(self, user: User) -> None:
        self.__users[user.id] = user

    def update_user(self, user_id: str, user: User) -> bool:
        if user_id not in self.__users:
            return False
        
        self.__users[user_id] = user
        return True
    
    def delete_user(self, user_id: str) -> bool:
        if user_id not in self.__users:
            return False
        
        del self.__users[user_id]
        return True