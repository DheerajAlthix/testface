from pydantic import BaseModel, validator
from typing import Optional, List
from datetime import datetime, date


class PersonalCareServiceSchema(BaseModel):
    id: int
    name: str
    description: str
    price: float
    image: Optional[str] = None
    availability: bool
    provider_id: int
    created_at: datetime
    updated_at: datetime
    average_rating: Optional[float] = None
    total_reviews: Optional[int] = 0
    latest_review: Optional[str] = None
    provider_name: Optional[str] = None

    @validator('price')
    def validate_price(cls, v):
        if v < 0:
            raise ValueError("Price cannot be negative")
        return v

    class Config:
        from_attributes = True