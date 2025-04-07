import requests
from django.shortcuts import get_object_or_404
from ..models import ABHAUser
from ..utils import get_base_headers
from django.conf import settings
from ..schemas import ABHAUserResponse, ProfileResponse

class ABHAService:
    def get_abha_user(self, client_id: str) -> dict:
        user = get_object_or_404(ABHAUser, client_id=client_id)
        return {
            "success": True,
            "data": ABHAUserResponse(
                id=user.id,
                client_id=user.client_id,
                access_token=user.access_token,
                created_at=user.created_at.isoformat(),
                updated_at=user.updated_at.isoformat()
            ).dict()
        }

    def get_profile(self, client_id: str) -> dict:
        user = get_object_or_404(ABHAUser, client_id=client_id)
        if not user.access_token:
            return {"success": False, "message": "Access token not found"}
        
        url = f"{getattr(settings, 'ABDM_PROFILE_URL', 'https://abhasbx.abdm.gov.in/abha')}/api/v3/profile/public/certificate"
        headers = get_base_headers()
        headers["Authorization"] = f"Bearer {user.access_token}"
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            abha_data = ABHAUserResponse(
                id=user.id,
                client_id=user.client_id,
                access_token=user.access_token,
                created_at=user.created_at.isoformat(),
                updated_at=user.updated_at.isoformat()
            )
            return {
                "success": True,
                "data": ProfileResponse(
                    profile=abha_data,
                    certificate=response.json()
                ).dict()
            }
        return {"success": False, "message": response.json(), "status_code": response.status_code}