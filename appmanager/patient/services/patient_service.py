from django.contrib.auth.models import User
from ..schemas.patient import PatientSchema

class PatientService:
    def get_patient(self, user):
        try:
            if not user:
                return {"success": False, "message": "User not found"}
            
            # Get user data
            user_data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'date_joined': user.date_joined,
                'is_active': user.is_active,
                'is_staff': user.is_staff
            }
            
            return {"success": True, "data": user_data}
        except Exception as e:
            return {"success": False, "message": str(e)} 