from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any

class ReqCreateUser(BaseModel):
    user_name: str
    user_email: str
    user_pswd: str
    verification_code: str

class ReqVercode(BaseModel):
    email: EmailStr