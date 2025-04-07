from pydantic import BaseModel
from typing import Optional, Dict
from typing import Optional
from datetime import datetime


class PersonalCareSchema(BaseModel):
    id: int
    healthcare_provider_id: int
    personal_care_type: str
    experience: int
    description: Optional[str] = None
    price_rate: float
    created_at: datetime
    updated_at: datetime
    average_rating: Optional[float] = None
    total_reviews: Optional[int] = 0
    review: Optional[str] = None

    class Config:
        from_attributes = True