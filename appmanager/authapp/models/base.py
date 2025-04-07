from django.db import models
from typing import Optional

class BaseModel(models.Model):
    """
    Abstract base model with common fields and methods
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True

    def soft_delete(self) -> None:
        """Soft delete the model instance"""
        self.is_active = False
        self.save()

    def restore(self) -> None:
        """Restore a soft-deleted model instance"""
        self.is_active = True
        self.save() 