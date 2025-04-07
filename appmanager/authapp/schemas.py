from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any

class LoginRequest(BaseModel):
    username: str
    password: str

class GoogleLoginRequest(BaseModel):
    token: str

class UserData(BaseModel):
    id: int
    username: str
    email: str
    is_staff: bool
    is_superuser: bool
    role: Optional[str] = None
    role_data: Optional[Dict[str, Any]] = None 