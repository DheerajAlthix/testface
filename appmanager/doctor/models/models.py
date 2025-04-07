from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Lookup(models.Model):
    lookup_value = models.CharField(max_length=225)
    lookup_type = models.CharField(max_length=225)
    lookup_label = models.CharField(max_length=225)
    lookup_desc = models.CharField(max_length=225, blank=True, null=True)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  

    def __str__(self):
        return f"{self.lookup_label} ({self.lookup_type})"
     

class HealthCareProvider(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="doctor_profile") 
    first_name = models.CharField(max_length=225)
    last_name = models.CharField(max_length=225)
    dob = models.DateField()
    address = models.JSONField()
    HPR_ID = models.CharField(max_length=50, unique=True) 
    email = models.EmailField(unique=True) 
    contact_number = models.CharField(max_length=15)
    gender = models.CharField(max_length=10, choices=[("Male", "Male"), ("Female", "Female"), ("Other", "Other")])
    profile_image = models.ImageField(upload_to="profile_images/", blank=True, null=True)
    service_type = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.service_type}"


class PersonalCare(models.Model):
    healthcare_provider = models.ForeignKey(HealthCareProvider, on_delete=models.CASCADE, related_name="healthcare_provider")
    experience = models.IntegerField()
    description = models.TextField(blank=True, null=True)  
    price_rate = models.DecimalField(max_digits=10, decimal_places=2) 
    personal_care_type = models.CharField(max_length=225)
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)  

    def __str__(self):
        return f"{self.personal_care_type} - {self.experience} years"
