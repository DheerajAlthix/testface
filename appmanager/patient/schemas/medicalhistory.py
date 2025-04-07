from pydantic import BaseModel, validator
from typing import Optional, List
from datetime import datetime, date


class MedicalHistorySchema(BaseModel):
    id: int
    patient_id: int
    condition: str
    diagnosis_date: date
    symptoms: str
    treatment: str
    medications: Optional[str] = None
    is_ongoing: bool
    severity: str
    healthcare_provider_id: int
    created_at: datetime
    updated_at: datetime

    @validator('diagnosis_date')
    def validate_diagnosis_date(cls, v):
        if v > datetime.now().date():
            raise ValueError("Diagnosis date cannot be in the future")
        return v

    class Config:
        from_attributes = True