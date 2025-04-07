from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from appmanager.doctor.models.models import HealthCareProvider
from .base import BaseModel

class MedicalHistory(BaseModel):
    """
    Model to store patient's medical history
    """
    CONDITIONS = [
        ('diabetes', 'Diabetes'),
        ('hypertension', 'Hypertension'),
        ('heart_disease', 'Heart Disease'),
        ('asthma', 'Asthma'),
        ('arthritis', 'Arthritis'),
        ('cancer', 'Cancer'),
        ('other', 'Other'),
    ]

    patient = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='medical_history')
    condition = models.CharField(max_length=50, choices=CONDITIONS)
    diagnosis_date = models.DateField(default=timezone.now)
    symptoms = models.TextField()
    treatment = models.TextField()
    medications = models.TextField(blank=True, null=True)
    healthcare_provider = models.ForeignKey(
        HealthCareProvider,
        on_delete=models.DO_NOTHING,
        related_name='diagnosed_conditions'
    )
    is_ongoing = models.BooleanField(default=True)
    severity = models.CharField(
        max_length=20,
        choices=[
            ('mild', 'Mild'),
            ('moderate', 'Moderate'),
            ('severe', 'Severe'),
            ('critical', 'Critical')
        ]
    )

    class Meta:
        verbose_name_plural = "Medical Histories"
        ordering = ['-diagnosis_date']
        indexes = [
            models.Index(fields=['patient', 'condition']),
            models.Index(fields=['healthcare_provider', 'condition']),
            models.Index(fields=['diagnosis_date']),
        ]

    def __str__(self):
        return f"{self.patient.username}'s {self.condition} - Diagnosed on {self.diagnosis_date}"

    def clean(self):
        if self.diagnosis_date and self.diagnosis_date > timezone.now().date():
            raise ValidationError("Diagnosis date cannot be in the future")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs) 