from django.contrib.auth.models import User
from ..models import OTPRequest
from ..services.notification_service import NotificationService
from rest_framework_simplejwt.tokens import RefreshToken
from ..schemas import UserData
import re

class OTPService:
    def __init__(self):
        self.notification_service = NotificationService()

    def generate_otp(self, contact: str) -> dict:
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        phone_regex = r'^\+?[0-9]{10,14}$'

        if re.match(email_regex, contact):
            return self._handle_email_otp(contact)
        elif re.match(phone_regex, contact):
            return self._handle_sms_otp(contact)
        else:
            return {"success": False, "message": "Invalid contact information"}

    def verify_otp(self, txn_id: str, otp: str) -> dict:
        from django.shortcuts import get_object_or_404
        otp_request = get_object_or_404(OTPRequest, txn_id=txn_id)
        if otp_request.is_verified:
            return {"success": False, "message": "OTP already used"}
        if otp_request.otp != otp:
            return {"success": False, "message": "Invalid OTP"}
        
        otp_request.is_verified = True
        otp_request.save()
        user = otp_request.user
        refresh = RefreshToken.for_user(user)
        user_data = self._get_user_data(user)
        return {
            "success": True,
            "data": {
                "message": "OTP verified successfully",
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),
                "user": user_data.dict()
            }
        }

    def _handle_email_otp(self, email: str) -> dict:
        user, _ = User.objects.get_or_create(
            email=email, defaults={"username": email}
        )
        otp_request = OTPRequest.objects.create(user=user)
        otp_request.generate_otp()
        data = {"phone_number": email, "otp": otp_request.otp}
        if self.notification_service.send_email(data):
            return {
                "success": True,
                "data": {"message": "OTP sent via email", "txn_id": otp_request.txn_id}
            }
        return {"success": False, "message": "Failed to send OTP via email"}

    def _handle_sms_otp(self, phone_number: str) -> dict:
        username = phone_number[2:] if phone_number.startswith('91') else phone_number
        user, _ = User.objects.get_or_create(
            username=username, defaults={"email": f"{username}@placeholder.com"}
        )
        otp_request = OTPRequest.objects.create(user=user)
        otp_request.generate_otp()
        if self.notification_service.send_sms(phone_number, otp_request.otp):
            return {
                "success": True,
                "data": {"message": "OTP sent via SMS", "txn_id": otp_request.txn_id}
            }
        return {"success": False, "message": "Failed to send OTP via SMS"}

    def _get_user_data(self, user: User) -> UserData:
        from ..services.auth_service import AuthService
        return AuthService()._get_user_data(user)