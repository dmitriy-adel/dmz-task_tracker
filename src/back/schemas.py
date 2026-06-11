from pydantic import BaseModel, EmailStr

class ReqCreateUser(BaseModel):
    user_name: str
    user_email: str
    user_pswd: str
    verification_code: str

class ReqVercode(BaseModel):
    email: EmailStr

class ReqLoginUser(BaseModel):
    user_email: str
    user_pswd: str
