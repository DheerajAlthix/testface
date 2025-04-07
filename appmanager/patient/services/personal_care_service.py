from ..models import PersonalCareService
from ..schemas import PersonalCareServiceSchema
from appmanager.patient.models import Rating
from django.db.models import Avg
from appmanager.doctor.models import HealthCareProvider

class PersonalCareServiceService:
    def list_services(self):
        services = PersonalCareService.objects.filter(is_active=True, availability=True)
        service_data = []
        for service in services:
            # Get provider details
            provider = HealthCareProvider.objects.filter(user_id=service.provider_id).first()
            provider_name = f"{provider.first_name} {provider.last_name}" if provider else None
            
            # Get ratings for the provider
            ratings = Rating.objects.filter(healthcare_provider_id=provider.id) if provider else Rating.objects.none()
            avg_rating = ratings.aggregate(Avg('rating'))['rating__avg']
            total_reviews = ratings.count()
            latest_review = ratings.order_by('-review_date').first()
            
            # Create a dictionary with all fields
            data = {
                'id': service.id,
                'name': service.name,
                'description': service.description,
                'price': float(service.price),
                'image': service.image.url if service.image else None,
                'availability': service.availability,
                'provider_id': service.provider_id,
                'created_at': service.created_at,
                'updated_at': service.updated_at,
                'average_rating': round(avg_rating, 1) if avg_rating else None,
                'total_reviews': total_reviews,
                'latest_review': latest_review.review if latest_review else None,
                'provider_name': provider_name
            }
            # Validate and serialize with Pydantic
            schema = PersonalCareServiceSchema(**data)
            service_data.append(schema.dict())
        return service_data