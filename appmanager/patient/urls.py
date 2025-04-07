from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PersonalCareServiceViewSet,
    AppointmentViewSet,
    RatingListAPIView,
    HealthRecordViewSet,
    MedicalHistoryViewSet,
    PatientView
)

router = DefaultRouter()
router.register(r'healthcare-services', PersonalCareServiceViewSet, basename='service')
router.register(r'appointments', AppointmentViewSet, basename='appointment')
router.register(r'health-records', HealthRecordViewSet, basename='health-record')
router.register(r'medical-history', MedicalHistoryViewSet, basename='medical-history')

urlpatterns = [
    path('', include(router.urls)),
    path('patient-details/', PatientView.as_view(), name='patient-detail'),
    path('ratings/', RatingListAPIView.as_view(), name='rating-list'),
]