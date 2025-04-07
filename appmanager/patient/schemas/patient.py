from pydantic import BaseModel
from datetime import datetime

class PatientSchema(BaseModel):
    id: int
    username: str
    email: str
    first_name: str
    last_name: str
    date_joined: datetime
    is_active: bool
    is_staff: bool

    class Config:
        from_attributes = True 