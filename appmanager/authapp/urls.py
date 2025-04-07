from django.urls import path
from .views import (
    ABHAUserView, VerifyOTPView, OTPRequestView, ProfileAPIView,
    GoogleLoginView, UserProfileView, Welcome, LoginView,
    DoctorSignupView, PatientSignupView
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("", Welcome.as_view(), name="welcome"),
    path("api/auth/login/", LoginView.as_view(), name="login"),
    path("api/auth/signup/doctor/", DoctorSignupView.as_view(), name="doctor-signup"),
    path("api/auth/signup/patient/", PatientSignupView.as_view(), name="patient-signup"),
    path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/auth/user-profile/", UserProfileView.as_view(), name="user_profile_view"),
    path("api/auth/auth/google/login/", GoogleLoginView.as_view(), name="google_login"),
    path("api/auth/session/", ABHAUserView.as_view(), name="session"),
    path("api/auth/otp-sender/", OTPRequestView.as_view(), name="verify_phone_user"),
    path("api/auth/otp-validate/", VerifyOTPView.as_view(), name="validate_token"),
    path("api/auth/profile/", ProfileAPIView.as_view(), name="profile"),
]