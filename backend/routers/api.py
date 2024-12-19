from fastapi import APIRouter
from . import auth, room, user

ROUTE_PREFIX_V1 = "/v1"
router = APIRouter()


def include_api_routes():
    router.include_router(auth.router, prefix=ROUTE_PREFIX_V1)
    router.include_router(room.router, prefix=ROUTE_PREFIX_V1)
    router.include_router(user.router, prefix=ROUTE_PREFIX_V1)


include_api_routes()