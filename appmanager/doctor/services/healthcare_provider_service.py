from django.db import IntegrityError
from ..models import HealthCareProvider
from ..schemas import HealthCareProviderSchema, HealthCareProviderCreateRequest

class HealthCareProviderService:
    def _convert_profile_image(self, provider):
        """Helper method to convert profile image to URL if it exists"""
        if provider.profile_image and hasattr(provider.profile_image, 'url'):
            return provider.profile_image.url
        return None

    def _prepare_provider_data(self, provider):
        """Helper method to prepare provider data for schema"""
        data = {
            'id': provider.id,
            'user_id': provider.user_id,
            'first_name': provider.first_name,
            'last_name': provider.last_name,
            'dob': provider.dob,
            'address': provider.address,
            'HPR_ID': provider.HPR_ID,
            'email': provider.email,
            'contact_number': provider.contact_number,
            'gender': provider.gender,
            'service_type': provider.service_type,
            'created_at': provider.created_at,
            'updated_at': provider.updated_at,
            'profile_image': self._convert_profile_image(provider)
        }
        return data

    def get(self, user):
        try:
            # First check if user exists
            if not user:
                return {"success": False, "message": "User not found"}
            
            print(f"Looking for provider with user_id: {user.id}")
            print(f"User email: {user.email}")
            
            # Try to get the provider using the user object directly
            provider = HealthCareProvider.objects.get(user=user)
            print(f"Found provider: {provider.id}, {provider.email}")
            
            # Prepare data and create schema
            provider_data = self._prepare_provider_data(provider)
            provider_dict = HealthCareProviderSchema(**provider_data).dict()
            return {"success": True, "data": provider_dict}
        except HealthCareProvider.DoesNotExist:
            # Check if any providers exist
            all_providers = HealthCareProvider.objects.all()
            print(f"Total providers in database: {all_providers.count()}")
            print(f"Provider emails: {[p.email for p in all_providers]}")
            
            # Check if there's a provider with matching email
            matching_provider = HealthCareProvider.objects.filter(email=user.email).first()
            if matching_provider:
                return {"success": False, "message": f"Provider found with email {user.email} but not linked to your user account. Please contact support."}
            
            return {"success": False, "message": "Health Care Provider profile not found. Please create your profile first."}
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            return {"success": False, "message": str(e)}

    def list_all(self):
        try:
            providers = HealthCareProvider.objects.all()
            provider_data = []
            for provider in providers:
                provider_dict = self._prepare_provider_data(provider)
                provider_data.append(HealthCareProviderSchema(**provider_dict).dict())
            return {
                "success": True,
                "data": provider_data
            }
        except Exception as e:
            return {"success": False, "message": str(e)}

    def create(self, user, data: HealthCareProviderCreateRequest):
        try:
            provider = HealthCareProvider.objects.create(
                user_id=user,
                **data.dict()
            )
            return {
                "success": True,
                "data": {"message": "Health Care Provider created successfully", "provider_id": provider.id}
            }
        except IntegrityError:
            return {"success": False, "message": "Duplicate entry detected. Please check HPR ID or email."}
        except Exception as e:
            return {"success": False, "message": str(e)}