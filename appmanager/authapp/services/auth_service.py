from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from appmanager.doctor.models import HealthCareProvider, PersonalCare
from google.oauth2 import id_token
from django.conf import settings
import google.auth.transport.requests
from ..schemas.auth import DoctorSignupRequest, PatientSignupRequest
from ..schemas.user import UserData

class AuthService:
    def login(self, username: str, password: str) -> dict:
        user = authenticate(username=username.strip().lower(), password=password)
        if user is not None and user.is_active:
            user_data = self._get_user_data(user)
            refresh = RefreshToken.for_user(user)
            return {
                "success": True,
                "data": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "user": user_data.dict()
                }
            }
        return {"success": False, "message": "Invalid credentials"}

    def doctor_signup(self, data: DoctorSignupRequest) -> dict:
        try:
            # Create user
            user = User.objects.create_user(
                username=data.username,
                email=data.email,
                password=data.password,
                first_name=data.first_name,
                last_name=data.last_name
            )
            
            # Create doctor profile
            doctor = HealthCareProvider.objects.create(
                user=user,
                first_name=data.first_name,
                last_name=data.last_name,
                dob=data.dob,
                address=data.address,
                HPR_ID=data.hpr_id,
                email=data.email,
                contact_number=data.contact_number,
                gender=data.gender,
                service_type=data.service_type
            )
            
            # Generate tokens
            refresh = RefreshToken.for_user(user)
            user_data = self._get_user_data(user)
            
            return {
                "success": True,
                "data": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "user": user_data.dict()
                }
            }
        except Exception as e:
            return {"success": False, "message": str(e)}

    def patient_signup(self, data: PatientSignupRequest) -> dict:
        try:
            # Create user
            user = User.objects.create_user(
                username=data.username,
                email=data.email,
                password=data.password,
                first_name=data.first_name,
                last_name=data.last_name
            )
            
            # Generate tokens
            refresh = RefreshToken.for_user(user)
            user_data = self._get_user_data(user)
            
            return {
                "success": True,
                "data": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "user": user_data.dict()
                }
            }
        except Exception as e:
            return {"success": False, "message": str(e)}

    def google_login(self, token: str) -> dict:
        user_info = self._validate_google_token(token)
        if not user_info:
            return {"success": False, "message": "Invalid Google token"}

        user = self._authenticate_google_user(user_info)
        if not user:
            return {"success": False, "message": "Authentication failed"}

        refresh = RefreshToken.for_user(user)
        return {
            "success": True,
            "data": {
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }
        }

    def _get_user_data(self, user: User) -> UserData:
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser,
            'role': None,
            'role_data': None
        }
        try:
            doctor = HealthCareProvider.objects.get(user=user)
            user_data['role'] = 'doctor'
            # Get the first personal care service for the doctor
            personal_care = PersonalCare.objects.filter(healthcare_provider=doctor).first()
            user_data['role_data'] = {
                'first_name': doctor.first_name,
                'last_name': doctor.last_name,
                'service_type': doctor.service_type,
                'hpr_id': doctor.HPR_ID,
                'contact_number': doctor.contact_number,
                'gender': doctor.gender,
                'profile_image': doctor.profile_image.url if doctor.profile_image else None,
                'experience': personal_care.experience if personal_care else None,
                'description': personal_care.description if personal_care else None,
                'price_rate': float(personal_care.price_rate) if personal_care else None,
                'personal_care_type': personal_care.personal_care_type if personal_care else None
            }
        except HealthCareProvider.DoesNotExist:
            # If not a doctor, treat as a patient
            user_data['role'] = 'patient'
            user_data['role_data'] = {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'date_joined': user.date_joined.strftime('%Y-%m-%d %H:%M:%S'),
                'last_login': user.last_login.strftime('%Y-%m-%d %H:%M:%S') if user.last_login else None
            }
        return UserData(**user_data)

    def _validate_google_token(self, token: str) -> dict:
        try:
            id_info = id_token.verify_oauth2_token(
                token, google.auth.transport.requests.Request(), 
                settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY
            )
            if id_info["iss"] not in ["accounts.google.com", "https://accounts.google.com"]:
                return None
            return id_info
        except ValueError:
            return None

    def _authenticate_google_user(self, user_info: dict) -> User:
        email = user_info.get("email")
        name = user_info.get("name")
        picture = user_info.get("picture", "")
        if not email:
            return None
        user, _ = User.objects.get_or_create(
            email=email,
            defaults={
                "username": email.split("@")[0],
                "first_name": name.split(" ")[0] if name else "",
                "last_name": name.split(" ")[1] if name and " " in name else ""
            }
        )
        from ..models import UserProfile
        user_profile, created = UserProfile.objects.get_or_create(
            user=user, defaults={"profile_picture": picture}
        )
        if created or not user_profile.profile_picture:
            user_profile.profile_picture = picture
            user_profile.save()
        return user