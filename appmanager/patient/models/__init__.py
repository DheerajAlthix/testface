# my_app/models/__init__.py
from .base import BaseModel
from .health_record import HealthRecord
from .medical_history import MedicalHistory
from .appointment import Appointment
from .service import PersonalCareService
from .rating import Rating

__all__ = [
    'BaseModel',
    'HealthRecord',
    'MedicalHistory',
    'Appointment',
    'PersonalCareService',
    'Rating',
]
