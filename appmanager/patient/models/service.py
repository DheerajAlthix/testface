from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.conf import settings
from .base import BaseModel

def validate_file_size(value):
    filesize = value.size
    if filesize > 5 * 1024 * 1024:  # 5MB
        raise ValidationError("Maximum file size is 5MB")

class PersonalCareService(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    image = models.ImageField(
        upload_to='services/',
        null=True,
        blank=True,
        validators=[validate_file_size]
    )
    availability = models.BooleanField(default=True)
    provider = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='services'
    )

    class Meta:
        indexes = [
            models.Index(fields=['provider', 'availability']),
            models.Index(fields=['price']),
        ]
        ordering = ['name']

    def __str__(self):
        return f"{self.name} - {self.provider.get_full_name()}"

    def clean(self):
        super().clean()
        if self.price < 0:
            raise ValidationError("Price cannot be negative")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs) 