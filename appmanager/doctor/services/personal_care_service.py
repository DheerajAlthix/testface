from ..models import PersonalCare
from ..schemas import PersonalCareSchema
from django.db.models import Avg, Count
from appmanager.patient.models import Rating

class PersonalCareService:
    def list(self, personal_care_type=None, sort_by='experience', order='asc'):
        queryset = PersonalCare.objects.all()
        if personal_care_type:
            queryset = queryset.filter(personal_care_type=personal_care_type)
        if order == 'desc':
            sort_by = f"-{sort_by}"
        queryset = queryset.order_by(sort_by)
        
        # Get ratings for each personal care service
        result = []
        for pc in queryset:
            # Get ratings for the healthcare provider
            ratings = Rating.objects.filter(healthcare_provider_id=pc.healthcare_provider_id)
            avg_rating = ratings.aggregate(Avg('rating'))['rating__avg']
            total_reviews = ratings.count()
            latest_review = ratings.order_by('-review_date').first()
            
            # Create service data with rating information
            service_data = PersonalCareSchema.from_orm(pc).dict()
            service_data['average_rating'] = round(avg_rating, 1) if avg_rating else None
            service_data['total_reviews'] = total_reviews
            service_data['review'] = latest_review.review if latest_review else None
            
            result.append(service_data)
        
        return result