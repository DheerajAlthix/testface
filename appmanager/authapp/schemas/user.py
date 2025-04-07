from pydantic import BaseModel
from typing import Optional, Dict
from datetime import date

class UserData(BaseModel):
    id: int
    username: str
    email: str
    is_staff: bool
    is_superuser: bool
    role: Optional[str] = None
    role_data: Optional[Dict] = None

class UserProfileUpdateRequest(BaseModel):
    dob: Optional[date] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    zipcode: Optional[str] = None
    adharnumber: Optional[str] = None
    abhaid: Optional[str] = None
    contactnumber: Optional[str] = None
    gender: Optional[str] = None
    profile: Optional[str] = None

class UserProfileResponse(BaseModel):
    id: int
    user_id: int
    dob: Optional[date]
    address: Optional[str]
    city: Optional[str]
    state: Optional[str]
    country: Optional[str]
    zipcode: Optional[str]
    adharnumber: Optional[str]
    abhaid: Optional[str]
    contactnumber: Optional[str]
    gender: Optional[str]
    profile: Optional[str]
    created_at: str
    updated_at: str