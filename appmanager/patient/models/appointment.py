from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from appmanager.doctor.models.models import HealthCareProvider
from .base import BaseModel
from .service import PersonalCareService

class Appointment(BaseModel):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]

    patient = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='patient_appointments')
    healthcare_provider = models.ForeignKey(HealthCareProvider, on_delete=models.DO_NOTHING, related_name='provider_appointments')
    service = models.ForeignKey(PersonalCareService, on_delete=models.DO_NOTHING, related_name='appointments')
    appointment_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['appointment_date']
        indexes = [
            models.Index(fields=['patient', 'status']),
            models.Index(fields=['healthcare_provider', 'status']),
            models.Index(fields=['appointment_date']),
        ]
        unique_together = ['patient', 'healthcare_provider', 'appointment_date']

    def __str__(self):
        return f"Appointment: {self.patient.username} with {self.healthcare_provider} on {self.appointment_date}"

    def clean(self):
        if self.appointment_date and self.appointment_date < timezone.now():
            raise ValidationError("Appointment date cannot be in the past")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs) 