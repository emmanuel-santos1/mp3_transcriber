# MP3Transcriber Board - Fastapi
A mp3 transcriber board app using fastapi

## Technology Stack:
* FastAPI
* Uvicorn (server)
* Pytest
* Sqlalchemy
* SQLite


## How to start the app ?
```
git clone https://github.com/
cd .\mp3_transcriber\
mkvirtualenv -p python3.10 -a mp3_transcriber mp3_transcriber  #create a virtual environment
pip install -r .\requirements.txt
docker run -d --name redis-stack -p 6379:6379 -p 8001:8001 redis/redis-stack:latest
uvicorn main:app --host 0.0.0.0 --port 8000 --reload  #start server
visit  127.0.0.1:8000/
```

## How to run tests ?
```
pytest
```

## How to create new user ?
```
visit  127.0.0.1:8000/register/
Complete form
```

Features:
 - ✔️ Serving Template
 - ✔️ Schemas
 - ✔️ Dependency Injection
 - ✔️ Password Hashing
 - ✔️ Unit Testing (What makes an app stable)
 - ✔️ Authentication login/create user/get token
 - ✔️ Authorization/Permissions 
 - ✔️ Logging
 - ✔️ Throttling
