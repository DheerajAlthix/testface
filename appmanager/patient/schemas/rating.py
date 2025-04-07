
from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime, date

class RatingSchema(BaseModel):
    id: Optional[int] = None 
    healthcare_provider_id: int
    patient_id: Optional[int] = None
    rating: int
    review: Optional[str] = None
    review_date: Optional[datetime] = None 
    created_at: Optional[datetime] = None  
    updated_at: Optional[datetime] = None 

    @validator('rating')
    def validate_rating(cls, v):
        if not 1 <= v <= 5:
            raise ValueError("Rating must be between 1 and 5")
        return v

    class Config:
        from_attributes = True