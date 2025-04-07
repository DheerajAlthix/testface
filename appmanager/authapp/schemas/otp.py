from pydantic import BaseModel
from .user import UserData  # Import UserData from user.py

class OTPRequest(BaseModel):
    contact: str

class OTPResponse(BaseModel):
    message: str
    txn_id: str

class OTPVerifyRequest(BaseModel):
    txn_id: str
    otp: str

class OTPVerifyResponse(BaseModel):
    message: str
    access_token: str
    refresh_token: str
    user: UserData