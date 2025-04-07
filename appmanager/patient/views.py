from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from pydantic import ValidationError
from .schemas.appointment import AppointmentSchema
from .schemas.medicalhistory import MedicalHistorySchema
from .schemas.healthcare import HealthRecordSchema
from .schemas.personalcareservices import PersonalCareServiceSchema
from .schemas.rating import RatingSchema
from .services.appointment_service import AppointmentService
from .services.rating_service import RatingService
from .services.health_record_service import HealthRecordService
from .services.medical_history_service import MedicalHistoryService
from .services.personal_care_service import PersonalCareServiceService
from .services.patient_service import PatientService
from appmanager.utils.response_status import ResponseStatus



class PatientView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        service = PatientService()
        result = service.get_patient(request.user)
        if result["success"]:
            return Response(result["data"])
        return Response({"error": result["message"]}, status=404 if "not found" in result["message"] else 500)

class AppointmentViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        service = AppointmentService()
        data = service.list_appointments(request.user, is_staff=request.user.is_staff)
        return Response(data)

    def create(self, request):
        try:
            data = request.data
            data['healthcare_provider_id'] = int(data['healthcare_provider_id'])
            data['service_id'] = int(data['service_id'])
            AppointmentSchema(**data)  # Validate data
        except ValidationError as e:
            return Response({"error": str(e)}, status=400)
        service = AppointmentService()
        result = service.create_appointment(data, request.user)
        if result["success"]:
            return Response(result["data"], status=201)
        return Response({"error": result["message"]}, status=400)

    def cancel(self, request, pk=None):
        service = AppointmentService()
        result = service.cancel_appointment(pk)
        if result["success"]:
            return Response({"status": result["message"]})
        return Response({"error": result["message"]}, status=400)
#rating code 
class RatingListAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        service = RatingService()
        healthcare_provider_id = request.data.get('healthcare_provider_id')
        if healthcare_provider_id:
            try:
                healthcare_provider_id = int(healthcare_provider_id)
            except ValueError:
                return ResponseStatus.error("Invalid healthcare_provider_id format")
        data = service.list_ratings(healthcare_provider_id)
        return ResponseStatus.success(data)
    
    def post(self, request):
        try:
            service = RatingService()
            if not request.data:
                return ResponseStatus.not_data(RatingSchema.schema())
            
            # Add the patient_id from the authenticated user
            data = request.data.copy()
            data['patient_id'] = request.user.id
            
            result = service.save_rating(data)
            if result:
                return ResponseStatus.created(result)
            return ResponseStatus.error("Failed to save rating")
        except ValidationError as e:
            return ResponseStatus.error(str(e))
        except Exception as e:
            return ResponseStatus.error(f"An error occurred: {str(e)}")

class HealthRecordViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        service = HealthRecordService()
        data = service.list_health_records(request.user, is_staff=request.user.is_staff)
        return Response(data)

    def create(self, request):
        try:
            data = request.data
            HealthRecordSchema(**data)  # Validate data
        except ValidationError as e:
            return Response({"error": str(e)}, status=400)
        service = HealthRecordService()
        result = service.create_health_record(data, request.user)
        if result["success"]:
            return Response(result["data"], status=201)
        return Response({"error": result["message"]}, status=400)

class MedicalHistoryViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        service = MedicalHistoryService()
        data = service.list_medical_history(request.user, is_staff=request.user.is_staff)
        return Response(data)

    def create(self, request):
        try:
            data = request.data
            data['healthcare_provider_id'] = int(data['healthcare_provider_id'])
            MedicalHistorySchema(**data)  # Validate data
        except ValidationError as e:
            return Response({"error": str(e)}, status=400)
        service = MedicalHistoryService()
        result = service.create_medical_history(data, request.user)
        if result["success"]:
            return Response(result["data"], status=201)
        return Response({"error": result["message"]}, status=400)

class PersonalCareServiceViewSet(viewsets.ViewSet):
    def list(self, request):
        service = PersonalCareServiceService()
        data = service.list_services()
        return Response(data)

    def retrieve(self, request, pk=None):
        service = PersonalCareServiceService()
        result = service.get_service(pk)
        if result["success"]:
            return Response(result["data"])
        return Response({"error": result["message"]}, status=404)

    def book_appointment(self, request, pk=None):
        try:
            data = request.data
            data['service_id'] = int(pk)
            data['healthcare_provider_id'] = int(data['healthcare_provider_id'])
            AppointmentSchema(**data)  # Validate data
        except ValidationError as e:
            return Response({"error": str(e)}, status=400)
        service = AppointmentService()
        result = service.create_appointment(data, request.user)
        if result["success"]:
            return Response(result["data"], status=201)
        return Response({"error": result["message"]}, status=400)