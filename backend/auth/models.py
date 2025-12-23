from pydantic import BaseModel, EmailStr
from typing import Optional, Literal


class UserRegister(BaseModel):
    email: EmailStr
    password: str
    role: Optional[Literal["user", "admin"]] = "user"


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: str
    email: str
    role: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
