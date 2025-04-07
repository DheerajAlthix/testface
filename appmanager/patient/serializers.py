from rest_framework import serializers
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import (
    PersonalCareService,
    Appointment,
    Rating,
    HealthRecord,
    MedicalHistory
)
from appmanager.doctor.models import HealthCareProvider,PersonalCare

class HealthCareProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthCareProvider
        fields = ['id', 'name', 'specialization', 'experience', 'rating']

class PersonalCareServiceSerializer(serializers.ModelSerializer):
    provider_details = HealthCareProviderSerializer(source='provider', read_only=True)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = PersonalCareService
        fields = [
            'id', 'name', 'description', 'price', 'image',
            'availability', 'provider', 'provider_details',
            'average_rating', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_average_rating(self, obj):
        ratings = obj.ratings.all()
        if ratings.exists():
            return ratings.aggregate(avg_rating=Avg('rating'))['avg_rating']
        return 0

    def validate_price(self, value):
        if value < 0:
            raise ValidationError("Price cannot be negative")
        return value

class AppointmentSerializer(serializers.ModelSerializer):
    service_details = PersonalCareServiceSerializer(source='service', read_only=True)
    patient_name = serializers.CharField(source='patient.get_full_name', read_only=True)

    class Meta:
        model = Appointment
        fields = [
            'id', 'appointment_date', 'status', 'notes',
            'service', 'service_details', 'patient', 'patient_name',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'patient']

    def validate_appointment_date(self, value):
        if value < timezone.now():
            raise ValidationError("Appointment date cannot be in the past")
        return value

    def validate(self, data):
        # Check if the service is available
        service = data.get('service')
        if service and not service.availability:
            raise ValidationError("This service is not available")
        
        # Check if the appointment time is available
        appointment_date = data.get('appointment_date')
        if appointment_date and service:
            existing_appointment = Appointment.objects.filter(
                service=service,
                appointment_date=appointment_date,
                status='scheduled'
            ).exists()
            if existing_appointment:
                raise ValidationError("This time slot is already booked")
        
        return data

class RatingSerializer(serializers.ModelSerializer):
    average_rating = serializers.FloatField()
    total_reviews = serializers.IntegerField()
    full_name = serializers.SerializerMethodField()
    review = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    experience = serializers.SerializerMethodField()

    class Meta:
        model = HealthCareProvider
        fields = [
            'id', 'full_name', 'service_type', 'experience',  
            'description', 'average_rating', 'total_reviews', 'review'
        ]

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    def get_review(self, obj):
        rating = getattr(obj, 'rating', None)  # Avoid exception if rating does not exist
        if rating:
            return {
                'rating': rating.rating,
                'review': rating.review,
                'patient_name': rating.patient.user.get_full_name() if rating.patient else "Anonymous",
                'review_date': rating.review_date.strftime("%Y-%m-%d %H:%M:%S")
            }
        return None

    def get_description(self, obj):
        personal_care = PersonalCare.objects.filter(healthcare_provider=obj).first()
        return personal_care.description if personal_care else None

    def get_experience(self, obj):
        personal_care = PersonalCare.objects.filter(healthcare_provider=obj).first()
        return personal_care.experience if personal_care else None

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['average_rating'] = round(data['average_rating'], 1) if data['average_rating'] is not None else 0.0
        return data

class HealthRecordSerializer(serializers.ModelSerializer):
    uploaded_by_name = serializers.CharField(source='uploaded_by.get_full_name', read_only=True)
    checked_by_name = serializers.CharField(source='checked_by.get_full_name', read_only=True)

    class Meta:
        model = HealthRecord
        fields = [
            'id', 'file', 'report_type', 'sample_collection',
            'uploaded_by', 'uploaded_by_name', 'checked_by',
            'checked_by_name', 'user', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'uploaded_by']

    def validate_sample_collection(self, value):
        if value > timezone.now():
            raise ValidationError("Sample collection date cannot be in the future")
        return value

    def validate_file(self, value):
        if value.size > 5 * 1024 * 1024:  # 5MB
            raise ValidationError("File size cannot exceed 5MB")
        return value

class MedicalHistorySerializer(serializers.ModelSerializer):
    healthcare_provider_details = HealthCareProviderSerializer(source='healthcare_provider', read_only=True)
    patient_name = serializers.CharField(source='patient.get_full_name', read_only=True)

    class Meta:
        model = MedicalHistory
        fields = [
            'id', 'condition', 'diagnosis_date', 'symptoms',
            'treatment', 'medications', 'is_ongoing', 'severity',
            'healthcare_provider', 'healthcare_provider_details',
            'patient', 'patient_name', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'patient']

    def validate_diagnosis_date(self, value):
        if value > timezone.now():
            raise ValidationError("Diagnosis date cannot be in the future")
        return value

    def validate_severity(self, value):
        if not 1 <= value <= 5:
            raise ValidationError("Severity must be between 1 and 5")
        return value
