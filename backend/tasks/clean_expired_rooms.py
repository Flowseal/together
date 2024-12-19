import os
import threading

from datetime import datetime, timezone
from database.local_storage import Storage

ROOM_LIFETIME_MINUTES = int(os.getenv("ROOM_LIFETIME_MINUTES", 1440))
TASK_DELAY_SECONDS = 60


def clean_expired_rooms():
    storage = Storage()

    while True:
        now = datetime.now(timezone.utc)
        expired_rooms = [room.id for room in storage.get_rooms().values() if 
                            (now - room.created_at).total_seconds() > ROOM_LIFETIME_MINUTES * 60]
        
        for room_id in expired_rooms:
            storage.delete_room(room_id)

        threading.Event().wait(TASK_DELAY_SECONDS)