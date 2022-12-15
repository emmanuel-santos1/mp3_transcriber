import logging
import os
import sys
from loguru import logger
import redis.asyncio as redis
from core.config import settings
from sql_app.base import Base
from sql_app.session import engine
from sql_app.utils import check_db_connected
from sql_app.utils import check_db_disconnected
from fastapi import FastAPI, Request
from fastapi_limiter import FastAPILimiter
from base import api_router as web_app_router
from starlette.routing import Match
from sqlalchemy_file.storage import StorageManager
from libcloud.storage.drivers.local import LocalStorageDriver


logger.remove()
logger.add(sys.stdout, colorize=True, format="<green>{time:HH:mm:ss}</green> | {level} | <level>{message}</level>")
logging.basicConfig(filename='mp3_transcriber.log', encoding='utf-8', level=logging.DEBUG)

def include_router(app):
    app.include_router(web_app_router)


def define_storage():
    os.makedirs("/tmp/storage/mp3_transcriber", 0o777, exist_ok=True)
    container = LocalStorageDriver("/tmp/storage").get_container("mp3_transcriber")
    StorageManager.add_storage("default", container)


def create_tables():
    Base.metadata.create_all(bind=engine)


def start_application():
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    include_router(app)
    define_storage()
    create_tables()
    return app


app = start_application()


@app.middleware("http")
async def log_middle(request: Request, call_next):
    logger.debug(f"{request.method} {request.url}")
    routes = request.app.router.routes
    logger.debug("Params:")
    for route in routes:
        match, scope = route.matches(request)
        if match == Match.FULL:
            for name, value in scope["path_params"].items():
                logger.debug(f"\t{name}: {value}")
    logger.debug("Headers:")
    for name, value in request.headers.items():
        logger.debug(f"\t{name}: {value}")

    response = await call_next(request)
    return response


@app.on_event("startup")
async def app_startup():
    await check_db_connected()
    r = redis.from_url("redis://127.0.0.1", encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(redis=r)


@app.on_event("shutdown")
async def app_shutdown():
    await check_db_disconnected()
