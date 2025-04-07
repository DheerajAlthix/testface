from pydantic import BaseModel, validator
from typing import Optional, List
from datetime import datetime, date

class HealthRecordSchema(BaseModel):
    id: int
    user_id: int
    file: str
    report_type: str
    sample_collection: datetime
    uploaded_by: str
    checked_by: str
    created_at: datetime
    updated_at: datetime

    @validator('sample_collection')
    def validate_sample_collection(cls, v):
        if v > datetime.now():
            raise ValueError("Sample collection date cannot be in the future")
        return v

    class Config:
        from_attributes = True