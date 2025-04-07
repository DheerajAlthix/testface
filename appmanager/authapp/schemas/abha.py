from pydantic import BaseModel
from typing import Optional, Dict

class ABHAUserResponse(BaseModel):
    id: int
    client_id: str
    access_token: Optional[str]
    created_at: str
    updated_at: str

class ProfileResponse(BaseModel):
    profile: ABHAUserResponse
    certificate: Dict