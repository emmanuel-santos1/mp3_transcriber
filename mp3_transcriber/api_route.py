import shutil
from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.orm import Session
from core.config import settings
from sql_app.crud import get_mp3_transcriber_by_id
from sql_app.models import MP3Transcriber, User

from sql_app.session import get_db
from mp3_transcriber.utils import get_large_audio_transcription, get_sentiment
from users.api_route import get_current_user_from_token
from fastapi_limiter.depends import RateLimiter

router = APIRouter()


@router.post("/upload-mp3")
def create_upload_file(
    file: UploadFile,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
    limit_second = Depends(RateLimiter(times=1, seconds=1)),
    limit_min = Depends(RateLimiter(times=10, seconds=60))
):
    mp3_transcriber = MP3Transcriber(content=file)
    mp3_transcriber.name = file.filename
    with open(file.filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    mp3_transcriber.plain_text = get_large_audio_transcription(file.filename)
    try:
        mp3_transcriber.sentiment_analysis = get_sentiment(mp3_transcriber.plain_text)
    except:
        pass
    db.add(mp3_transcriber)
    db.commit()
    db.refresh(mp3_transcriber)
    return mp3_transcriber


@router.post("/count-words")
def count_words(
    id: int,
    word: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
    limit_second = Depends(RateLimiter(times=1, seconds=1)),
    limit_min = Depends(RateLimiter(times=10, seconds=60))
):
    mp3_transcriber = get_mp3_transcriber_by_id(id, db)
    ocurrence = mp3_transcriber.plain_text.lower().count(word.lower())
    return ocurrence
