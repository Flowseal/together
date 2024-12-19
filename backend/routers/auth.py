from uuid import uuid4

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from models import User
from database.local_storage import Storage
from utils import create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.post("/login", response_model=dict)
def login(username: str):
    storage = Storage()

    user_id = str(uuid4())
    user = User(id=user_id, username=username)
    storage.insert_user(user)

    token = create_access_token({"sub": user.id})
    response = JSONResponse(content={"message": "Login successful"})
    response.set_cookie(
        key="jwt",
        value=token,
        httponly=True,
        secure=True,
        samesite="lax",
        path="/"
    )

    return response