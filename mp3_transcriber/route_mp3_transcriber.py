from typing import Optional
from sql_app.crud import list_mp3_transcriber, search_mp3_transcriber
from sql_app.session import get_db
from fastapi import APIRouter, HTTPException
from fastapi import Depends
from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi.security.utils import get_authorization_scheme_param
from sqlalchemy.orm import Session

from users.api_route import get_current_user_from_token


templates = Jinja2Templates(directory="templates")
router = APIRouter(include_in_schema=False)


@router.get("/")
async def home(
    request: Request,
    db: Session = Depends(get_db),
    msg: str = None
):
    mp3_transcribers = list_mp3_transcriber(db=db)
    authorization: str = request.cookies.get(
        "access_token", None
    )
    scheme, token = get_authorization_scheme_param(authorization)
    if not authorization or scheme.lower() != "bearer":
        user = None
        mp3_transcribers = []
    else :
        try:
            user = get_current_user_from_token(token, db)
        except HTTPException:
            user = None
            mp3_transcribers = []
    return templates.TemplateResponse(
        "general_pages/homepage.html",
        {"request": request, "mp3_transcribers": mp3_transcribers, "user": user, "msg": msg}
    )


@router.get("/search/")
def search(
    request: Request,
    db: Session = Depends(get_db),
    query: Optional[str] = None
):
    mp3_transcribers = search_mp3_transcriber(query, db=db)
    authorization: str = request.cookies.get(
        "access_token", None
    )
    scheme, token = get_authorization_scheme_param(authorization)
    if not authorization or scheme.lower() != "bearer":
        user = None
        mp3_transcribers = []
    else :
        try:
            user = get_current_user_from_token(token, db)
        except HTTPException:
            user = None
            mp3_transcribers = []
    return templates.TemplateResponse(
        "general_pages/homepage.html", {"request": request, "user": user, "mp3_transcribers": mp3_transcribers}
    )
