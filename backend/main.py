import os
from dotenv import load_dotenv
load_dotenv()

import threading

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from colorama import init as colorama_init

from routers.api import router as router_api_v1
from routers.handlers import http_error_handler
from tasks.clean_expired_rooms import clean_expired_rooms

API_PREFIX = "/api"


def get_application() -> FastAPI:
    application = FastAPI()

    ## Mapping api routes
    application.include_router(router_api_v1, prefix=API_PREFIX)

    ## Add exception handlers
    application.add_exception_handler(HTTPException, http_error_handler)

    ## Allow cors
    origins = [
        os.getenv("HOST", "https://example.com"),
        "http://localhost:5173",
        "http://localhost:8080",
    ]
    
    application.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return application


## Force colorama init for WinOS
colorama_init()

## Background tasks
threading.Thread(target=clean_expired_rooms, daemon=True).start()

## Main app
app = get_application()