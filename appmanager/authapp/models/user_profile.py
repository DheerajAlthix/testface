from django.db import models
from django.contrib.auth.models import User
from typing import Optional


class UserProfile(models.Model):
    user: User = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    dob: Optional[models.DateField] = models.DateField(null=True, blank=True)
    address: str = models.TextField()
    city: str = models.CharField(max_length=100)
    state: str = models.CharField(max_length=100)
    country: str = models.CharField(max_length=100)
    zipcode: str = models.CharField(max_length=6)
    adharnumber: str = models.CharField(max_length=12, unique=False)
    abhaid: str = models.CharField(max_length=12, unique=False)
    contactnumber: str = models.CharField(max_length=12, unique=False)
    gender: str = models.CharField(
        max_length=10,
        choices=[("Male", "Male"), ("Female", "Female"), ("Other", "Other")]
    )
    profile: Optional[str] = models.URLField(max_length=255, blank=True, null=True)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.user.username
