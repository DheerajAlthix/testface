from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from .base import BaseModel

def validate_file_size(value):
    filesize = value.size
    if filesize > 5 * 1024 * 1024:  # 5MB limit
        raise ValidationError("Maximum file size is 5MB")

class HealthRecord(BaseModel):
    REPORT_TYPES = [
        ('blood_test', 'Blood Test'),
        ('x_ray', 'X-Ray'),
        ('mri', 'MRI'),
        ('ct_scan', 'CT Scan'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(User, models.DO_NOTHING, db_column='user_id')
    file = models.FileField(
        upload_to='health_records/',
        max_length=255,
        validators=[
            FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png']),
            validate_file_size
        ]
    )
    report_type = models.CharField(max_length=50, choices=REPORT_TYPES)
    sample_collection = models.DateTimeField(default=timezone.now)
    uploaded_by = models.CharField(max_length=50)
    checked_by = models.CharField(max_length=50)

    class Meta:
        indexes = [
            models.Index(fields=['user', 'report_type']),
            models.Index(fields=['sample_collection']),
        ]

    def __str__(self):
        return f"Health Record {self.user} - {self.report_type}"

    def clean(self):
        if self.sample_collection and self.sample_collection > timezone.now():
            raise ValidationError("Sample collection date cannot be in the future")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs) 