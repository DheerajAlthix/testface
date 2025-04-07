from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, Dict
from datetime import date
from .user import UserData

class LoginRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=150)
    password: str = Field(..., min_length=5)

class LoginResponse(BaseModel):
    refresh: str
    access: str
    user: UserData

class GoogleLoginRequest(BaseModel):
    token: str = Field(..., description="Google ID token")

class GoogleLoginResponse(BaseModel):
    refresh: str
    access: str

class DoctorSignupRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=150)
    email: EmailStr
    password: str = Field(..., min_length=8)
    first_name: str = Field(..., min_length=2, max_length=100)
    last_name: str = Field(..., min_length=2, max_length=100)
    dob: date
    address: Dict = Field(..., description="Address details as a JSON object")
    hpr_id: str = Field(..., min_length=5, max_length=50)
    contact_number: str = Field(..., min_length=10, max_length=15)
    gender: str = Field(..., pattern="^(Male|Female|Other)$")
    service_type: str = Field(..., min_length=2, max_length=100)

    @validator('contact_number')
    def validate_contact_number(cls, v):
        if not v.isdigit():
            raise ValueError('Contact number must contain only digits')
        return v

class PatientSignupRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=150)
    email: EmailStr
    password: str = Field(..., min_length=8)
    first_name: str = Field(..., min_length=2, max_length=100)
    last_name: str = Field(..., min_length=2, max_length=100)