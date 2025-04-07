from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LookupViewSet, PersonalCareListAPIView, HealthCareProviderListView

router = DefaultRouter()
router.register(r'lookups', LookupViewSet, basename='lookup')

urlpatterns = [
    path('', include(router.urls)),
    path('healthcare-providers/', HealthCareProviderListView.as_view(), name='providers-list'),
    path('personal-care-list/', PersonalCareListAPIView.as_view(), name='personal-care-list'),
]