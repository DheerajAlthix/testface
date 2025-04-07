from pydantic import BaseModel
from typing import Optional, Dict
from typing import Optional
from datetime import datetime


class LookupSchema(BaseModel):
    id: int
    lookup_label: str
    lookup_type: str
    lookup_value: str
    lookup_desc: Optional[str] = None
    created_at: datetime  # Changed from str to datetime
    updated_at: datetime  # Changed from str to datetime

    class Config:
        from_attributes = True  # Enables mapping from ORM objects