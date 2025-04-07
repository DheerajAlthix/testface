from ..models import UserProfile
from ..schemas import UserProfileResponse

class UserService:
    def update_profile(self, user, data: dict, files: dict = None) -> dict:
        profile, created = UserProfile.objects.get_or_create(user=user)
        
        # Update fields from the request data
        for key, value in data.items():
            if hasattr(profile, key):
                setattr(profile, key, value)
        
        profile.save()
        
        return {
            "success": True,
            "data": UserProfileResponse(
                id=profile.id,
                user_id=user.id,
                dob=profile.dob,
                address=profile.address,
                city=profile.city,
                state=profile.state,
                country=profile.country,
                zipcode=profile.zipcode,
                adharnumber=profile.adharnumber,
                abhaid=profile.abhaid,
                contactnumber=profile.contactnumber,
                gender=profile.gender,
                profile=profile.profile,
                created_at=profile.created_at.isoformat(),
                updated_at=profile.updated_at.isoformat()
            ).dict()
        }