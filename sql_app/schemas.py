from fastapi import UploadFile
from pydantic import BaseModel, EmailStr
from typing import Optional


class Token(BaseModel):
    access_token: str
    token_type: str

class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    name: str
    last_name: str
    password: str


class User(UserBase):
    id: int
    name: str
    last_name: str

    class Config:
        orm_mode = True


class MP3Transcriber(BaseModel):
    id: int
    name: str
    content: UploadFile
    plain_text: Optional[str] = ""
    sentiment_analysis: Optional[str] = "Unidentified"
