from sqlalchemy import Column, Integer, String, DECIMAL, Text
from sqlalchemy_file import FileField

from sql_app.base_class import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)


class MP3Transcriber(Base):
    __tablename__ = "mp3_transcriber"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    content = Column(FileField)
    plain_text = Column(Text)
    sentiment_analysis = Column(String(100))
