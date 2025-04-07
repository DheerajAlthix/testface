import random
import uuid
from django.contrib.auth.models import User
from django.db import models

class OTPRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link OTP to a user
    txn_id = models.UUIDField(default=uuid.uuid4, unique=True)
    otp = models.CharField(max_length=6)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def generate_otp(self):
        """Generates a 6-digit OTP and saves it to the model."""
        self.otp = str(random.randint(1000, 9999))
        self.is_verified = False  # Reset verification on new OTP
        self.save()

    def __str__(self):
        return f"OTP for {self.user.username}: {self.otp}"
