from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from pydantic import ValidationError
from .schemas.lookup import LookupSchema
from .schemas.personalcare import PersonalCareSchema
from .services.lookup_service import LookupService
from .services.healthcare_provider_service import HealthCareProviderService
from .services.personal_care_service import PersonalCareService

class LookupViewSet(viewsets.ViewSet):
    def list(self, request):
        service = LookupService()
        data = service.list()
        return Response(data)


class HealthCareProviderListView(APIView):
    def get(self, request):
        service = HealthCareProviderService()
        result = service.list_all()
        if result["success"]:
            return Response(result["data"])
        return Response({"error": result["message"]}, status=500)


class PersonalCareListAPIView(APIView):
    def get(self, request):
        try:
            personal_care_type = request.data.get('personal_care_type')
            sort_by = request.data.get('sort_by', 'experience')
            order = request.data.get('order', 'asc')
            service = PersonalCareService()
            data = service.list(personal_care_type, sort_by, order)
            return Response(data)
        except Exception as e:
            return Response({"error": str(e)}, status=400)