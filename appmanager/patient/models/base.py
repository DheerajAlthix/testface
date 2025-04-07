from django.db import models
from django.utils import timezone

class BaseModel(models.Model):
    """
    Base model class that provides common fields and functionality for all models
    """
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def soft_delete(self):
        """
        Soft delete the model instance
        """
        self.is_deleted = True
        self.is_active = False
        self.updated_at = timezone.now()
        self.save()

    def restore(self):
        """
        Restore a soft-deleted model instance
        """
        self.is_deleted = False
        self.is_active = True
        self.updated_at = timezone.now()
        self.save()

    def save(self, *args, **kwargs):
        """
        Override save method to handle soft delete and timestamps
        """
        if self.is_deleted:
            self.is_active = False
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        super().save(*args, **kwargs) 