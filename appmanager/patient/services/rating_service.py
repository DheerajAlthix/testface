from appmanager.doctor.models import HealthCareProvider
from ..models import Rating
from ..schemas import RatingSchema
from django.db.models import Avg, Count
from django.core.exceptions import ValidationError

class RatingService:
    def list_ratings(self, healthcare_provider_id=None):
        if healthcare_provider_id:
            ratings = Rating.objects.filter(healthcare_provider_id=healthcare_provider_id)
        else:
            ratings = Rating.objects.all()
        return [RatingSchema.from_orm(rating).dict() for rating in ratings]
    
    def save_rating(self, data):       
        try:
            # Validate healthcare provider exists
            if not HealthCareProvider.objects.filter(id=data['healthcare_provider_id']).exists():
                raise ValueError("Healthcare provider not found")

            # Create and validate rating schema
            rating_schema = RatingSchema(**data)
            
            # Create and save rating
            rating = Rating.objects.create(
                healthcare_provider_id=data['healthcare_provider_id'],
                patient_id=data['patient_id'],
                rating=data['rating'],
                review=data.get('review')
            )
            
            return RatingSchema.from_orm(rating).dict()
        except ValidationError as e:
            raise e
        except Exception as e:
            print(f"Error saving rating: {str(e)}")
            return None