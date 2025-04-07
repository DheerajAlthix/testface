from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime, date

class HealthCareProviderSchema(BaseModel):
    id: int
    user_id: int
    first_name: str
    last_name: str
    dob: date
    address: dict
    HPR_ID: str
    email: str
    contact_number: str
    gender: str
    profile_image: Optional[str] = None
    service_type: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
        json_encoders = {
            date: lambda v: v.isoformat(),
            datetime: lambda v: v.isoformat()
        }