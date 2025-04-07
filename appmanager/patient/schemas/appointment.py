from pydantic import BaseModel, validator
from typing import Optional, List
from datetime import datetime, date


class AppointmentSchema(BaseModel):
    id: int
    patient_id: int
    healthcare_provider_id: int
    service_id: int
    appointment_date: datetime
    status: str
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    @validator('appointment_date')
    def validate_appointment_date(cls, v):
        if v < datetime.now():
            raise ValueError("Appointment date cannot be in the past")
        return v

    class Config:
        from_attributes = True