import os
import jwt

from typing import Optional
from fastapi import HTTPException, Cookie, status
from database.local_storage import Storage

SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

def get_current_user_id(token: Optional[str] = Cookie(default=None, alias="jwt")) -> str:
    storage = Storage()

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")

        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        
        if not storage.get_user(user_id):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        
        return user_id
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)