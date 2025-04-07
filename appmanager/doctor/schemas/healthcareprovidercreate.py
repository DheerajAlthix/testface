from pydantic import BaseModel
from typing import Optional, Dict
from typing import Optional
from datetime import datetime


class HealthCareProviderCreateRequest(BaseModel):
    first_name: str
    last_name: str
    dob: str
    address: Dict
    hpr_id: str
    email: str
    contact_number: str
    gender: Optional[str] = 'O'
    profile_image: Optional[str] = None
    service_type: str