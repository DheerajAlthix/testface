from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.authentication import JWTAuthentication
from pydantic import ValidationError
from .schemas.auth import (
    LoginRequest, LoginResponse, GoogleLoginRequest, GoogleLoginResponse,
    DoctorSignupRequest, PatientSignupRequest
)
from .schemas.user import UserData, UserProfileUpdateRequest, UserProfileResponse
from .schemas.abha import ABHAUserResponse, ProfileResponse
from .schemas.otp import OTPRequest, OTPResponse, OTPVerifyRequest, OTPVerifyResponse
from .services.auth_service import AuthService
from .services.user_service import UserService
from .services.otp_service import OTPService
from .services.abha_service import ABHAService
from rest_framework import status

class Welcome(APIView):
    def get(self, request):
        return Response({"message": "Welcome to Althix Backend!", "username": "admin", "password": "admin"})


class LoginView(APIView):
    def post(self, request):
        try:
            data = LoginRequest(**request.data)
            auth_service = AuthService()
            result = auth_service.login(data.username, data.password)
            if result["success"]:
                return Response(result["data"])
            return Response({"error": result["message"]}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class DoctorSignupView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        try:
            data = DoctorSignupRequest(**request.data)
            auth_service = AuthService()
            result = auth_service.doctor_signup(data)
            if result["success"]:
                return Response(result["data"], status=status.HTTP_201_CREATED)
            return Response({"error": result["message"]}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PatientSignupView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        try:
            data = PatientSignupRequest(**request.data)
            auth_service = AuthService()
            result = auth_service.patient_signup(data)
            if result["success"]:
                return Response(result["data"], status=status.HTTP_201_CREATED)
            return Response({"error": result["message"]}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserProfileView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    def put(self, request):
        try:
            profile_data = UserProfileUpdateRequest(**request.data)
        except ValidationError as e:
            return Response({"success": False, "message": str(e)}, status=400)
        
        user_service = UserService()
        result = user_service.update_profile(request.user, profile_data.dict(exclude_unset=True), request.FILES)
        if result["success"]:
            return Response(result["data"])
        return Response({"success": False, "message": "Profile update failed"}, status=400)

class GoogleLoginView(APIView):
    def post(self, request):
        try:
            data = GoogleLoginRequest(**request.data)
            auth_service = AuthService()
            result = auth_service.google_login(data.token)
            if result["success"]:
                return Response(result["data"])
            return Response({"error": result["message"]}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ABHAUserView(APIView):
    def get(self, request):
        client_id = request.query_params.get('client_id')
        if not client_id:
            return Response({"success": False, "message": "client_id is required"}, status=400)
        
        abha_service = ABHAService()
        result = abha_service.get_abha_user(client_id)
        if result["success"]:
            return Response(result["data"])
        return Response({"success": False, "message": "User not found"}, status=404)

class ProfileAPIView(APIView):
    def get(self, request):
        client_id = request.query_params.get('clientId')
        if not client_id:
            return Response({"success": False, "message": "clientId is required"}, status=400)
        
        abha_service = ABHAService()
        result = abha_service.get_profile(client_id)
        if result["success"]:
            return Response(result["data"])
        return Response({"success": False, "message": result["message"]}, status=result.get("status_code", 400))

class OTPRequestView(APIView):
    def post(self, request):
        try:
            otp_data = OTPRequest(**request.data)
        except ValidationError as e:
            return Response({"success": False, "message": str(e)}, status=400)
        
        otp_service = OTPService()
        result = otp_service.generate_otp(otp_data.contact)
        if result["success"]:
            return Response(result["data"])
        return Response({"success": False, "message": result["message"]}, status=400)

class VerifyOTPView(APIView):
    def post(self, request):
        try:
            verify_data = OTPVerifyRequest(**request.data)
        except ValidationError as e:
            return Response({"success": False, "message": str(e)}, status=400)
        
        otp_service = OTPService()
        result = otp_service.verify_otp(verify_data.txn_id, verify_data.otp)
        if result["success"]:
            return Response(result["data"])
        return Response({"success": False, "message": result["message"]}, status=400)