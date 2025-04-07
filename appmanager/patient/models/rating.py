from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from appmanager.doctor.models.models import HealthCareProvider
from .base import BaseModel
from django.contrib.auth.models import User
from django.utils import timezone

class Rating(BaseModel):
    healthcare_provider = models.OneToOneField(
        HealthCareProvider,
        on_delete=models.CASCADE,
        db_column='healthcareprovider_id',
        related_name='rating'
    )
    patient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='ratings',
        null=True,
        blank=True
    )
    rating = models.IntegerField(
        validators=[
            MinValueValidator(1, message="Rating must be at least 1"),
            MaxValueValidator(5, message="Rating cannot exceed 5")
        ]
    )
    review = models.TextField()
    review_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.healthcare_provider} - {self.rating} ⭐: {self.review}"

    class Meta:
        ordering = ['-rating']