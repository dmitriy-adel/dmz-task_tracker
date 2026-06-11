import secrets
from datetime import datetime
from fastapi import FastAPI, HTTPException, status, Depends, Response, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from time import time

from tools import Tools
from db_connection import DBConnection
from email_sender import EmailSender
from schemas import (ReqCreateUser, ReqVercode)
from redis_logic import RedisClient


tls: Tools = Tools()
es: EmailSender = EmailSender()
dbc: DBConnection = DBConnection()
rc: RedisClient = RedisClient()

app: FastAPI = FastAPI(lifespan=rc.lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://localhost",
        "http://127.0.0.1"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

def get_redis(request: Request):
    if not hasattr(request.app.state, "redis"):
        raise RuntimeError("Redis client wasnt initialized yet")
    
    return request.app.state.redis

async def get_current_user_id_from_redis(request: Request, redis_client = Depends(get_redis)):
    session_id = request.cookies.get("session_id")
    if not session_id:
        raise HTTPException(status_code=401, detail="Not autorizedd")

    user_id = await rc.get_session(session_id, redis_client)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Session expired")

    return user_id

@app.get("/health")
def health() -> dict[str, int]:
    return {"status": 200}

@app.post("/send_vercode")  
async def send_email_with_code(request_body: ReqVercode, redis_client = Depends(get_redis)):
    email: str = request_body.email.strip().lower()\
    
    if dbc.check_if_user_exists_by_email(email=email):
        print(f"[app.py->send_email_with_code]. user with email {email} already exists")
        raise HTTPException(status_code=406, detail="user already exists")
    
    code: str = tls.generate_verification_code()
    await rc.create_email_verification_code(email, code, redis_client)
    success: bool = es.send_vercode(code=code, to_email=email)
    
    if success:
        print(f"[app.py->send_email_with_code]. Successfuly sended code {code} to {email}")
        return {"status": True}
    
    else:
        print(f"[app.py->send_email_with_code]. can't send ver. code to {email}")
        raise HTTPException(status_code=500, detail="Server error")
    
@app.post("/check_vercode_and_add_user")  
async def check_vercode_and_add_user(request: ReqCreateUser, redis_client = Depends(get_redis)):
    try:
        if await rc.verify_email_code(email=request.user_email, input_code=request.verification_code, redis_client=redis_client):
            hashed_pswd: str = tls.hash_password(request.user_pswd)
            dbc.add_user(
                name=request.user_name,
                email=request.user_email,
                hash_password=hashed_pswd,
            )
            await rc.delete_email_vercode(email=request.user_email, redis_client=redis_client)
            return {"status": True}

        return {"status": False}

    except Exception as _ex:
        print(f"[app.py->add_user]. Error :: {_ex}")
        raise HTTPException(status_code=500, detail="Server error")