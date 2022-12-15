from fastapi import APIRouter
from users import route_users, api_route as api_route_user
from mp3_transcriber import route_mp3_transcriber, api_route as api_route_mp3_transcriber

from sql_app.session import engine
from sql_app import models

models.Base.metadata.create_all(bind=engine)

api_router = APIRouter()
api_router.include_router(route_mp3_transcriber.router, prefix="", tags=["mp3-transcribers"])
api_router.include_router(route_users.router, prefix="", tags=["users"])
api_router.include_router(api_route_mp3_transcriber.router, prefix="", tags=["api-mp3-transcribers"])
api_router.include_router(api_route_user.router, prefix="", tags=["api-users"])
